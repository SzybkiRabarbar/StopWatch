
# TODO naprawić w summary pasek ilości czasu (?)
#// TODO zobaczyć czy świerzo otwarty kalendarz mozna ustawić na odpowiedniej godzinie
# TODO zapisać kolory główne aplikacji w osobnym pliku json i dodać możliwosć zmiany ich w settings
    #* to samo z fontem
# TODO pomyśleć o dodawaniu nowego kalendarza do GCalendar, zamiast dodawać do głównego
    #* tworzenie kalendarza
    #* dodawania do stworzonego kalendarza
# TODO naprawić bład 500
# TODO dodać powiadomienie w timer (użytkownik może ustawić sobie budzik na np 45 minut itp) (zrobic prosty gdzie wpisuje się minuty)
# TODO wyjść z wersji testowej calendar api
# TODO zrobić ciekawe i dogłębne README do każdego folderu

import tkinter as tk
from pandas import read_sql_query
from sqlite3 import connect

from Source.TitleBar.title_bar import CreateTitleBar
from Source.Menu.menu import CreateMenu
from Source.Timer.timer import CreateTimer
from Source.Calendar.calendar import CreateCalendar
from Source.Summary.summary import CreateSummary
from Source.Event.event_toplevel import OpenEventToplevel
from Source.Settings.settings import CrateSettings
from Source.GoogleCalendar.google_cal import add_to_google_calendar

class TimerApp():
    
    EFFECTSCOLOR = '#3f3f3f' # button color effects in the title bar
    BARCOLOR = '#151515' # title bar color
    
    FONTF = 'Ariel' # main font
    BGCOLOR = '#2a2a2a' # background color
    MIDCOLOR = '#545454' # shade between bg and fg
    FGCOLOR = '#ededed' # text color
    MODESIGN = '◑'

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('Timer')
        self.window = tk.Frame(self.root, bg=TimerApp.BGCOLOR,highlightthickness=0)
        CreateTitleBar(self)
        self.root.resizable(False, False)
        
        #| Global Variables
        self.conn = connect('DB\\sqlite.db')
        """Connection with sqlite database"""
        divided_width = self.root.winfo_screenwidth() // 3
        divided_height = self.root.winfo_screenheight() // 5
        self.default_window_shift = f"+{divided_width}+{divided_height}"
        """Determines the default position of the root window """
        self.was_fullscreen = False
        """
        Bool, changed if the window was set to fullscree.
        Helps determine whether the default window position should be set
        """
        
        self.root.geometry('1x1' + self.default_window_shift)
        self.open_menu()
        
    def run(self):
        self.root.mainloop()
        self.conn.close()
        
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
    
    def open_menu(self):
        CreateMenu(self)
        
    def open_timer(self):
        CreateTimer(self)
    
    def open_calendar(self):
        CreateCalendar(self)
    
    def open_summary(self):
        CreateSummary(self)
    
    def open_event(self, arg: list[list, list]):
        OpenEventToplevel(self, arg)
    
    def change_color(self):
        """Switches the application's color scheme between light and dark modes"""
        if TimerApp.BGCOLOR == '#2a2a2a':
            #| switch to ligth mode
            TimerApp.BGCOLOR = '#ededed' # background color
            TimerApp.MIDCOLOR = '#a9a9a9'
            TimerApp.FGCOLOR = '#2a2a2a' # text color
            TimerApp.MODESIGN = '◐'
        else:
            #| switch to dark mode
            TimerApp.BGCOLOR = '#2a2a2a' # background color
            TimerApp.MIDCOLOR = '#545454'
            TimerApp.FGCOLOR = '#ededed' # text color
            TimerApp.MODESIGN = '◑'
        self.open_menu()
    
    def open_settings(self):
        CrateSettings(self)
    
    def append_to_google_calendar(self, name: str, date: str, start_time: str, duration: int, desc: str) -> tuple[int, str]:
        return add_to_google_calendar(name, date, start_time, duration, desc)

if __name__=="__main__":
    t = TimerApp()
    t.run()