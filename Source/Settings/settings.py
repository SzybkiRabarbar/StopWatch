import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from timer_app import TimerApp

class CrateSettings:
    """Creates label, separators and buttons for diffrent settings"""
    from Source.Settings.apperance_settings import change_to_default
    from Source.Settings.apperance_settings import change_app_colors, save_new_colors
    from Source.Settings.apperance_settings import change_font, create_fonts, save_new_font
    from Source.Settings.google_calendar_settings import rm_token, pick_auto_append_activities
    def __init__(self, App: 'TimerApp') -> None:
        self.App = App
        self.main()
        
    def main(self):
        self.App.clear_window()
        self.App.window.config(background=self.App.BGCOLOR)
        
        #* Appearance
        self.title('Appearance')
        self.separator()
        self.button('Change to default settings', self.change_to_default)
        self.button('Change colors of App', self.change_app_colors)
        self.button('Change font', self.change_font)
        self.separator()
        
        #* Google Calendar
        self.title('Google Calendar')
        self.separator()
        self.button("Remove Data About Used Account", self.rm_token)
        self.button("Auto Append To Calendar", self.pick_auto_append_activities)
        self.separator()
    
    def title(self, name: str):
        tk.Label(
            self.App.window,
            font = (self.App.FONTF, 20),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            text = name
        ).pack(anchor='w')
    
    def separator(self):
        tk.Frame( #| Separator
            self.App.window,
            background = self.App.FGCOLOR,
            bd = 0,
            height = 1
        ).pack(fill='x', pady=5)
    
    def button(self, text: str, method):
        tk.Button(
            self.App.window,
            font=(self.App.FONTF, 15),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            anchor = 'w',
            text = text,
            command = method
        ).pack(fill='x')