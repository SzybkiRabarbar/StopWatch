import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stop_watch import StopWatch

class CreateMenu:
    """
    Creates buttons that open other classes.
    """
    def __init__(self, App: 'StopWatch') -> None:
        self.App = App
        self.main()
    
    def main(self):
        self.App.clear_window()
        
        if self.App.was_fullscreen:
            self.App.root.geometry(self.App.default_window_shift)
            self.App.was_fullscreen = False
        elif self.App.is_in_timer:
            self.App.is_in_timer = False
            
        self.App.root.geometry('446x719')
        self.App.window.config(bg=self.App.BGCOLOR)
        
        button_to_timer = tk.Button(
            self.App.window,
            text = "Timer",
            bg = self.App.MIDCOLOR,
            fg = self.App.FGCOLOR,
            activebackground = self.App.MIDCOLOR,
            activeforeground = self.App.BGCOLOR,
            pady = 12,
            padx = 50,
            font = (self.App.FONTF, 40 , 'bold'),
            command = self.App.open_timer
        )
        button_to_timer.pack(fill='x', padx=30, pady=20)
        
        button_to_calendar = tk.Button(
            self.App.window,
            text = 'Calendar',
            bg = self.App.MIDCOLOR,
            fg = self.App.FGCOLOR,
            activebackground = self.App.MIDCOLOR,
            activeforeground = self.App.BGCOLOR,
            pady = 12,
            padx = 50,
            font = (self.App.FONTF, 40 , 'bold'),
            command = self.App.open_calendar
        )
        button_to_calendar.pack(fill='x', padx=30, pady=20)
        
        button_to_summary = tk.Button(
            self.App.window,
            text = 'Summary',
            bg = self.App.MIDCOLOR,
            fg = self.App.FGCOLOR,
            activebackground = self.App.MIDCOLOR,
            activeforeground = self.App.BGCOLOR,
            pady = 12,
            padx = 50,
            font = (self.App.FONTF, 40 , 'bold'),
            command = self.App.open_summary
        )
        button_to_summary.pack(fill='x', padx=30, pady=20)

        lowest_button = tk.Frame(self.App.window)
        lowest_button.pack(fill='x', padx=30, pady=20)
                
        button_change_mode = tk.Button(
            lowest_button,
            text = self.App.MODESIGN,
            bg = self.App.MIDCOLOR,
            fg = self.App.FGCOLOR,
            activebackground = self.App.MIDCOLOR,
            activeforeground = self.App.BGCOLOR,
            pady = 12,
            padx = 25,
            font = (self.App.FONTF, 40 , 'bold'),
            command=self.App.change_color
        )
        button_change_mode.pack(side='left', fill='y')
        
        button_to_settings = tk.Button(
            lowest_button,
            text = 'Settings',
            bg = self.App.MIDCOLOR,
            fg = self.App.FGCOLOR,
            activebackground = self.App.MIDCOLOR,
            activeforeground = self.App.BGCOLOR,
            pady = 18.5,
            font = (self.App.FONTF, 30, 'bold'),
            command = self.App.open_settings
        )
        button_to_settings.pack(side='right', fill='both', expand=True)
