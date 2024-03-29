import os
import shutil

APPDATA = os.getenv('appdata')
LOCALAPPDATA = os.getenv('localappdata')
PROGRAMDATA = os.getenv('programdata')

paths = [
    f"{PROGRAMDATA}\\NVIDIA Corporation\\Downloader",
    f"{LOCALAPPDATA}\\CrashDumps",
    f"{LOCALAPPDATA}\\Temp",
    f"{LOCALAPPDATA}\\pip\\cache",
    f"{LOCALAPPDATA}\\npm-cache",
    f"{LOCALAPPDATA}\\NVIDIA\\DXCache",
    f"{LOCALAPPDATA}Low\\Temp",
    f"{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\Cache",
    f"{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\Code Cache",
    f"{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\Service Worker\\CacheStorage",
    f"{LOCALAPPDATA}\\Microsoft\\Windows\\WebCache",
    f"{LOCALAPPDATA}\\Google\\Chrome\\User Data\\Default\\Cache",
    f"{LOCALAPPDATA}\\Google\\Chrome\\User Data\\Default\\Code Cache",
    f"{LOCALAPPDATA}\\Google\\Chrome\\User Data\\Default\\Service Worker\\CacheStorage",
    f"{LOCALAPPDATA}\\NVIDIA Corporation\\NVIDIA GeForce Experience\\CefCache\\Cache",
    f"{APPDATA}\\discord\\Cache",
    f"{APPDATA}\\discord\\Code Cache",
    f"{APPDATA}\\discord\\GPUCache",
    f"{APPDATA}\\RStudio\\Cache",
    f"{APPDATA}\\RStudio\\Code Cache",
    f"{APPDATA}\\Code\\Cache",
    f"{APPDATA}\\Code\\CachedData",
    f"{APPDATA}\\Code\\CachedExtensions",
    f"{APPDATA}\\Code\\Code Cache",
    f"{APPDATA}\\Code\\Service Worker\\CacheStorage",
    f"{APPDATA}\\Microsoft\\Teams\\Cache",
    f"{APPDATA}\\Microsoft\\Teams\\Code Cache",
    f"{APPDATA}\\Microsoft\\Teams\\Partitions\\msa\\Service Worker\\CacheStorage",
    f"{APPDATA}\\Microsoft\\Teams\\Partitions\\msa\\Cache",
    f"{APPDATA}\\Microsoft\\Teams\\Partitions\\msa\\Code Cache",
    f"{APPDATA}\\Microsoft\\Teams\\Service Worker\\CacheStorage"
]

paths.sort()

print("Deleting...")
for path in paths:
    if os.path.exists(path):
        print(path)
    shutil.rmtree(path, ignore_errors=True)
    
input("\nPC cleaned...")