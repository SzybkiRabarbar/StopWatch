import os
from pathlib import Path

def get_appdata_folder() -> Path:
    """Return path to StopWatch folder in appdata (if doesnt exist creates one)"""
    appdata_path = os.getenv('APPDATA')
    
    new_folder_name = 'StopWatch'
    ### Only in StopWatchExample.exe
    # new_folder_name = 'StopWatchExample'
    appdata_folder = Path(appdata_path) / new_folder_name
    appdata_folder.mkdir(parents=True, exist_ok=True)
    return appdata_folder