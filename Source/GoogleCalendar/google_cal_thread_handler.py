import threading
from tkinter import messagebox
from os.path import exists

from Source.GoogleCalendar.google_cal import add_to_google_calendar

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stop_watch import StopWatch

class ThreadHandler:
    """
    Makes thread that appends data to the Google Calendar
    """
    def __init__(self, App: 'StopWatch') -> None:
        self.App = App
    
    def append_data(self, name: str, date: str, start_time: str, duration: int, desc: str, ancestor):
        """
        Appends data to the Google Calendar\n
        IF a thread.is_alive THEN\n
            Shows a warning message
        ELSE
            Launches a new thread using the launch_thread method
        """
        try:
            if self.t.is_alive():
                messagebox.showwarning(
                    'Wait', 'The previous save still hasn\'t been executed. Wait some time before trying again. '
                    'If this window continues to appear after some time, restart the program.',
                    parent = ancestor
                ) 
            else:
                self.t = self.launch_thread(name, date, start_time, duration, desc, ancestor)
                
        except AttributeError:
            self.t = self.launch_thread(name, date, start_time, duration, desc, ancestor)
            
    def launch_thread(self, name: str, date: str, start_time: str, duration: int, desc: str, ancestor) -> threading.Thread:
        """Creates and starts a new thread with the target function being self.thread and returns the thread"""
        t = threading.Thread(target=self.thread, args=(name, date, start_time, duration, desc, ancestor))
        t.daemon = True
        t.start()
        return t
    
    def thread(self, name: str, date: str, start_time: str, duration: int, desc: str, ancestor):
        """
        It asks the user if they want to add an event to their Google Calendar. 
        If the user agrees, it attempts to add the event using the add_to_google_calendar function and shows a success or error message based on the result.
        """
        s = '' if exists(self.App.db_path / 'token.json') else 'After clicking yes, log in to your Google account in newly opened browser window.'
        
        if messagebox.askyesno(f"{name}", f"Do you want to add {name} to google calendar? {s}", parent = ancestor):
            is_succes, res = add_to_google_calendar(self.App.db_path, self.App.static_path ,name, date, start_time, duration, desc)
            if not ancestor.winfo_exists():
                ancestor = self.App.root
            if is_succes:
                messagebox.showinfo(name, f"{name} was succesful added to your calendar", parent = ancestor)
            else:
                messagebox.showerror(name, res, parent = ancestor)