import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from tqdm import tqdm


SITE = "https://www.indiacode.nic.in/"
LAWS_SAVEPATH = "dataset/all_indian_laws.json"
LAWS = {}

"""LAWS structure: LAWS['State_Name']['Act_Name, Year']['Section_No'] = 'Description'"""


def get_browser() -> WebDriver:
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--headless")
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    options.add_argument("--disable-cache")
    options.add_argument("--start-maximized")
    options.add_argument("--enable-automation");
    options.add_argument("--window-size=1920,1080");
    options.add_argument("--no-sandbox");
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-extensions");
    options.add_argument("--dns-prefetch-disable");
    options.add_argument("--disable-gpu");

    browser = webdriver.Chrome(options)
    browser.implicitly_wait(60)
    return browser


def get_url(browser: WebDriver, url: str) -> WebDriver:
    """Retries getting the url if required"""
    retries = 5
    while True:
        try:
            browser.get(url)
            return browser
        except TimeoutException as e:
            if retries == 0:
                raise e
            retries -= 1
            continue


def scrape_from_acts_table(browser: WebDriver, url: str) -> dict[str, dict[str, str]]:
    """
    Takes the url of a indiacode Acts table page and scrapes all the data
    about all the Acts and their corresponding sections.
    """
    browser = get_url(browser, url)
    body = browser.find_element(By.TAG_NAME, "tbody")

    acts_dict = {}
    for row in body.find_elements(By.TAG_NAME, "tr")[1:]:
        td = row.find_elements(By.TAG_NAME, "td")
        act_name = td[2].get_property("innerText").strip()
        act_link = td[3].find_element(By.TAG_NAME, "a")
        acts_dict[act_name] = act_link.get_attribute("href")

    for act_name, act_link in tqdm(acts_dict.items()):
        try:
            acts_dict[act_name] = scrape_from_act_page(browser, act_link)
        except Exception as e:
            print("Act:", act_name, "->", act_link)
            raise e

    return acts_dict


def scrape_from_act_page(browser: WebDriver, url: str) -> dict[str, str]:
    """Takes URL of an Act's section page and scrapes the description of all the sections."""
    browser = get_url(browser, url)

    if "No data available in table" in browser.find_element(By.TAG_NAME, "html").get_property("innerText"):
        return {}

    retries = 5
    while True:
        try:
            WebDriverWait(browser, 10).until(
                lambda d: d.execute_script(
                    "return typeof $ !== 'undefined' && typeof $('#myTableActSection').DataTable !== 'undefined'"
                )
            )
            break

        except TimeoutException as e:
            if retries == 0:
                raise e
            retries -= 1
            browser = get_url(browser, url)
            continue

    # expands the DataTable to maximum no. of rows
    browser.execute_script("$('#myTableActSection').DataTable({destroy: true, iDisplayLength: -1});")
    tbody = browser.find_element(By.ID, "myTableActSection").find_element(By.TAG_NAME, "tbody")

    sec_dict = {}
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        sec_name = tr.find_element(By.TAG_NAME, "a").get_property("innerText")
        sec_name = sec_name.replace("\xa0", "").strip().split(".")
        sec_no = sec_name[0].replace("Section ", "").strip()
        sec_name[1] = " " + sec_name[1]
        sec_name = ".".join(sec_name)
        sec_dict[sec_no] = {
            "heading": sec_name,
            "href": tr.find_element(By.TAG_NAME, "a").get_attribute("href"),
        }

    for sec_no, sec in sec_dict.items():
        try:
            sec_dict[sec_no] = scrape_section_page(browser, sec["href"], sec["heading"])
        except Exception as e:
            print("Secion No.:", sec_no, "->", sec["href"])
            raise e

    return sec_dict


def scrape_section_page(browser: WebDriver, url: str, heading: str) -> str:
    """Scrapes a section's webpage and returns all the relevant text content in it."""
    retries = 5
    while True:
        try:
            browser = get_url(browser, url)

            error_strings = ["Invalid URL or Argument", "404 Page Not Found"]
            body_text = browser.find_element(By.TAG_NAME, "body").get_property("innerText").strip()
            if not body_text or any([x in body_text for x in error_strings]):
                return heading

            p_list = browser.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "p")
            p1 = p_list[1].get_property("innerText").strip()
            p2 = p_list[2].get_property("innerText").strip()
            return f"{heading}\n{p1}\n{p2}"

        except NoSuchElementException as e:
            if retries == 0:
                raise e
            retries -= 1
            continue


def main():
    global LAWS

    if os.path.exists(LAWS_SAVEPATH):
        with open(LAWS_SAVEPATH, 'r') as f:
            LAWS = json.load(f)

    browser = get_browser()
    query_string = "?rpp=99999"

    if not LAWS:
        browser = get_url(browser, SITE)

        e = browser.find_element(By.XPATH, "/html/body/header/div[4]/div/nav/ul[1]/li[4]/ul/li/a")
        url = e.get_attribute("href")
        LAWS["Central"] = url[:url.index("?")] + query_string

        e = browser.find_element(By.XPATH, "/html/body/header/div[4]/div/nav/ul[1]/li[5]/div")
        for div in e.find_elements(By.TAG_NAME, "div"):
            for a in div.find_elements(By.TAG_NAME, "a"):
                LAWS[a.get_property("innerText").strip()] = a.get_property("href") + "browse" + query_string

    for k, v in LAWS.items():
        if not isinstance(v, str):
            continue
        print(f"Scraping {k} laws...")
        LAWS[k] = scrape_from_acts_table(browser, v)

        with open(LAWS_SAVEPATH, "w") as f:
            json.dump(LAWS, f, indent=4)

    print("Scraping complete!")


if __name__ == "__main__":
    main()
