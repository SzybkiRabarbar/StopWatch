import os
from pathlib import Path

def get_appdata_folder() -> Path:
    """Return path to TimerApp folder in appdata (if doesnt exist creates one)"""
    appdata_path = os.getenv('APPDATA')
    
    new_folder_name = 'TimerApp'
    ### Only in TimerWithExampleData.exe
    # new_folder_name = 'TimerAppExample'
    appdata_folder = Path(appdata_path) / new_folder_name
    appdata_folder.mkdir(parents=True, exist_ok=True)
    return appdata_folder