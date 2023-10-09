import sys
from pathlib import Path
from os import path, makedirs
import json
import tkinter as tk
from tkinter import messagebox
from pandas import read_sql_query
from sqlite3 import connect

from Source.CreateDB.create_appdata import get_appdata_folder
from Source.CreateDB.create_palette import create_json_palette
from Source.CreateDB.create_sqlite import create_db_sqlite
from Source.TitleBar.title_bar import CreateTitleBar
from Source.Menu.menu import CreateMenu
from Source.Timer.timer import CreateTimer
from Source.Calendar.calendar import CreateCalendar
from Source.Summary.summary import CreateSummary
from Source.Event.event_toplevel import OpenEventToplevel
from Source.Settings.settings import CrateSettings
from Source.GoogleCalendar.google_cal_thread_handler import ThreadHandler

class TimerApp():
    
    MODESIGN = '◑'

    def __init__(self) -> None:
        self.get_paths()
        self.load_pallete()
        self.google_calendar = ThreadHandler(self)
        self.conn = connect(self.sqlite_path)
        self.build_tk_root()
        self.open_menu()
    
    def run(self):
        self.root.mainloop()
        self.conn.close()
    
    def build_tk_root(self):
        """Creates and configures tk.Tk() and creates variables associated with it"""
        self.root = tk.Tk()
        self.root.title('Timer')
        self.root.iconbitmap(self.static_path / 'icon.ico')
        self.window = tk.Frame(self.root, bg=self.BGCOLOR,highlightthickness=0)
        CreateTitleBar(self)
        self.root.resizable(False, False)
        
        ### Global Variables
        divided_width = self.root.winfo_screenwidth() // 3
        divided_height = self.root.winfo_screenheight() // 5
        #| Determines the default position of the root window
        self.default_window_shift = f"+{divided_width}+{divided_height}"
        #| Changes then the window is set to fullscreen.
        #| Helps determine whether the default window position (geometry) should be set
        self.was_fullscreen = False
        #| Bool, changes to True then timer is initialized or to False then menu is initalized
        #| Allows to determine whether the back and close buttons should ask for confirmation
        self.is_in_timer = False
        
        self.root.geometry('1x1' + self.default_window_shift)
        
    def get_paths(self):
        """
        Gets paths to statics and databases, if databases dont exists create them.\n
        IF app is .exe THEN\n
            sets db_path to folder in appdata and static_path to temporary folder\n
        ELSE\n
            sets db_path and static_path to path of the directory that the current script is in
        """
        if getattr(sys, 'frozen', False):
            self.db_path = get_appdata_folder() / 'DB'
            self.static_path = Path(sys._MEIPASS, 'Static') 
        else:
            self.db_path =  Path(path.dirname(path.abspath(__file__)), 'DB')
            self.static_path = Path(path.dirname(path.abspath(__file__)), 'Static')
        
        self.sqlite_path = self.db_path / 'sqlite.db'
        self.palette_json_path = self.db_path / 'palette.json'
        self.default_json_path = self.static_path / 'default.json'
        self.font_names_path = self.static_path / 'font_names.csv'
        
        if not path.exists(self.db_path):
            makedirs(self.db_path)
            
        if not path.isfile(self.sqlite_path):
            create_db_sqlite(self.sqlite_path)
            
        if not path.isfile(self.palette_json_path):
            create_json_palette(self.default_json_path, self.palette_json_path)
    
    def load_pallete(self):
        """Fetchs data and sets colors and font"""
        with open(self.palette_json_path, 'r') as file:
            palette = json.load(file)
        
        self.BARFGC = palette['BARFGC']    
        self.EFFECTSCOLOR = palette['EFFECTSCOLOR']
        self.BARBGC = palette['BARBGC']
        self.FONTF = palette['FONTF']
        
        self.PREVIOUS = palette['PREVIOUS']
        self.BGCOLOR = palette[self.PREVIOUS]['BGCOLOR']
        self.MIDCOLOR = palette[self.PREVIOUS]['MIDCOLOR']
        self.FGCOLOR = palette[self.PREVIOUS]['FGCOLOR']
    
    def clear_window(self):
        """Destroy all widgets from window(Frame)"""
        for widget in self.window.winfo_children(): 
            widget.destroy()
        try:
            self.window.after_cancel(self.loop_id)
        except AttributeError:
            pass
    
    def fetch_dfs(self):
        """
        Fetchs db, store results in instance variable.
        df_data[
            data.date, data.start_time, data.main_time,
            data.break_time, data.desc, activities.name AS activity
        ]
        df_activity[activities.name, activities.bg, activities.fg, activities.id]
        """
        self.df_data = read_sql_query(
            'SELECT data.date, data.start_time, data.main_time, '
            'data.break_time, data.desc, activities.name AS activity '
            'FROM data '
            'JOIN activities ON data.activity = activities.id',
            self.conn
        )
        self.df_activity = read_sql_query('SELECT name, bg, fg, id FROM activities', self.conn)
    
    def change_color(self):
        """Switches the application's color scheme between light and dark modes"""
        if self.PREVIOUS == '1':
            #| switch to ligth mode
            self.PREVIOUS = '0'
            self.MODESIGN = '◐'
        else:
            #| switch to dark mode
            self.PREVIOUS = '1'
            self.MODESIGN = '◑'
        
        with open(self.palette_json_path, 'r') as file:
            palette = json.load(file)
        
        self.BGCOLOR = palette[self.PREVIOUS]['BGCOLOR']
        self.MIDCOLOR = palette[self.PREVIOUS]['MIDCOLOR']
        self.FGCOLOR = palette[self.PREVIOUS]['FGCOLOR']
        palette['PREVIOUS'] = self.PREVIOUS
        
        with open(self.palette_json_path, 'w') as file:
            json.dump(palette, file, ensure_ascii=False, indent=4)
        
        self.open_menu()
    
    def confirm_execution(self):
        messagebox.showinfo('Changes saved', 'Your changes have been successfully saved')
    
    def open_menu(self):
        """Calls CreateMenu"""
        CreateMenu(self)
        
    def open_timer(self):
        """Calls CreateTimer"""
        CreateTimer(self)
    
    def open_calendar(self):
        """Calls CreateCalendar"""
        CreateCalendar(self)
    
    def open_summary(self):
        """Calls CreateSummary"""
        CreateSummary(self)
    
    def open_event(self, arg: list[list, list]):
        """Calls OpenEventToplevel"""
        OpenEventToplevel(self, arg)
    
    def open_settings(self):
        """Calls CrateSettings"""
        CrateSettings(self)
    
    def append_to_google_calendar(self, name: str, date: str, start_time: str, duration: int, desc: str, ancestor: tk.Toplevel = None):
        """Starts the process of adding data to Google Calendar"""
        if not ancestor:
            ancestor = self.root
        self.google_calendar.append_data(name, date, start_time, duration, desc, ancestor)

if __name__=="__main__":
    t = TimerApp()
    t.run()