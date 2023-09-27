import tkinter as tk
from tkinter import font
import json
import csv

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Source.Settings.settings import CrateSettings
    
def change_app_colors(self: 'CrateSettings'):
    pass

def change_font(self: 'CrateSettings'):
    """Creates scrollable canvas, when calls create fonts"""
    self.App.clear_window()
    
    tk.Button(
        self.App.window,
        font = (self.App.FONTF, 10),
        foreground = self.App.BGCOLOR,
        background = self.App.FGCOLOR,
        activeforeground = self.App.MIDCOLOR,
        activebackground = self.App.MIDCOLOR,
        text = 'Cancel',
        command = self.main
    ).pack(fill='x')
    
    #| Stores canvas
    canvas_container = tk.Frame(self.App.window)
    canvas_container.pack(fill='both', expand=True)
    
    #| Canvas contains scrollable content
    calendar_canvas = tk.Canvas(canvas_container)
    self.content = tk.Frame(calendar_canvas, background=self.App.MIDCOLOR)
    scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=calendar_canvas.yview)
    calendar_canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    calendar_canvas.pack(side="left", fill="both", expand=True)
    canvas_frame = calendar_canvas.create_window((0, 0), window=self.content, anchor="nw")
    
    #| Links scroll with content
    def on_frame_configure(event):
        calendar_canvas.configure(scrollregion=calendar_canvas.bbox("all"))
    self.content.bind("<Configure>", on_frame_configure)
    
    #| Changes width of canvas
    def frame_width(event):
        canvas_width = event.width
        calendar_canvas.itemconfig(canvas_frame, width = canvas_width)
    calendar_canvas.bind('<Configure>', frame_width)
    
    #| Enables mousewheel
    def on_mousewheel(event):
        calendar_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    calendar_canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    self.App.window.update_idletasks()
    self.create_fonts()
    
def create_fonts(self: 'CrateSettings'):
    """Creates buttons, each button represent diffrent font from system. On button click calls modify_json_font"""
    
    with open('DB\\font_names.csv', 'r') as file:
        reader = csv.DictReader(file)
        valid = {x['FONTNAME'] for x in reader}
    
    for font_name in font.families():
        if font_name in valid:
            tk.Button(
                self.content,
                font = (font_name, 15),
                anchor = 'w',
                background = self.App.BGCOLOR,
                foreground = self.App.FGCOLOR,
                activeforeground = self.App.BGCOLOR,
                activebackground = self.App.FGCOLOR,
                text = font_name,
                command = lambda x = font_name: self.modify_json_font(x)
            ).pack(expand=True, fill='x')

def modify_json_font(self: 'CrateSettings', font_name):
    """Modify palette.json with new font for app"""
    with open('DB\\palette.json', 'r') as file:
        palette = json.load(file)
    
    palette['FONTF'] = font_name
    self.App.FONTF = font_name
    
    with open('DB\\palette.json', 'w') as file:
        json.dump(palette, file, ensure_ascii=False, indent=4)
    
    self.App.open_menu()