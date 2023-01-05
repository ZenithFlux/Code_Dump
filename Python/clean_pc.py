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
    f"{LOCALAPPDATA}Low\\Temp",
    f"{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\Cache",
    f"{LOCALAPPDATA}\\Microsoft\\Edge\\User Data\\Default\\Code Cache",
    f"{APPDATA}\\discord\\Cache",
    f"{APPDATA}\\discord\\Code Cache",
    f"{APPDATA}\\discord\\GPUCache",
    f"{APPDATA}\\Code\\Cache",
    f"{APPDATA}\\Code\\CachedData",
    f"{APPDATA}\\Code\\CachedExtensions",
    f"{APPDATA}\\Code\\Code Cache"
]

paths.sort()

print("Deleting...")
for path in paths:
    if os.path.exists(path):
        print(path)
    shutil.rmtree(path, ignore_errors=True)
    
input("\nPC cleaned...")