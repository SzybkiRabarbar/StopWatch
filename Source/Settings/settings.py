import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from timer_app import TimerApp

class CrateSettings:
    """
    TODO
    """
    from Source.Settings.google_calendar_settings import rm_token, pick_auto_append_activities
    def __init__(self, App: 'TimerApp') -> None:
        self.App = App
        self.main()
        
    def main(self):
        self.App.clear_window()
            
        tk.Label(
            self.App.window,
            font = (self.App.FONTF, 20),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            text = 'Google Calendar'
        ).pack(anchor='w')
        
        tk.Frame( #| Separator
            self.App.window,
            background = self.App.FGCOLOR,
            bd = 0,
            height = 1
        ).pack(fill='x', pady=5)
        
        tk.Button(
            self.App.window,
            font = (self.App.FONTF, 10),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            anchor = 'w',
            text = "Remove Data About Used Account",
            command = self.rm_token
        ).pack(fill='x')
        
        tk.Button(
            self.App.window,
            font=(self.App.FONTF, 10),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            anchor = 'w',
            text = "Auto Append To Calendar",
            command = self.pick_auto_append_activities
        ).pack(fill='x')
        
        tk.Frame( #| Separator
            self.App.window,
            background = self.App.FGCOLOR,
            bd = 0,
            height = 1
        ).pack(fill='x', pady=5)
        