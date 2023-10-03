# from os import path
import tkinter as tk
from tkinter import font
import json
from tkinter.colorchooser import askcolor
from tkinter import messagebox
import csv
import string

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Source.Settings.settings import CrateSettings

def change_to_default(self: 'CrateSettings'):
    """Change palette.json responsible for App apperance to defult values"""
    with open(self.App.default_json_path, 'r') as file:
        palette = json.load(file)

    self.App.BARFGC = palette['BARFGC']    
    self.App.EFFECTSCOLOR = palette['EFFECTSCOLOR']
    self.App.BARBGC = palette['BARBGC']
    self.App.FONTF = palette['FONTF']
    
    self.App.PREVIOUS = palette['PREVIOUS']
    self.App.BGCOLOR = palette['1']['BGCOLOR']
    self.App.MIDCOLOR = palette['1']['MIDCOLOR']
    self.App.FGCOLOR = palette['1']['FGCOLOR']
    
    with open(self.App.palette_json_path, 'w') as file:
        json.dump(palette, file, ensure_ascii=False, indent=4)
    messagebox.showinfo('Changed to default', 'Apperence settings have been hanged to default', parent=self.App.window)
    self.main()
    
def change_app_colors(self: 'CrateSettings'):
    """Creates two new frames. For each frame, it calls the create_dummy_view function to create a view with color changing options"""
    self.App.clear_window()
    frame_zero = tk.Frame(self.App.window)
    frame_one = tk.Frame(self.App.window)
    for i, frame in enumerate((frame_zero, frame_one)):
        create_dummy_view(self.App.palette_json_path, self.main, self.save_new_colors, str(i), frame)
    frame_zero.pack(fill='both', expand=True)
    frame_one.pack(fill='both', expand=True)

def create_dummy_view(path, main, return_colors, theme: str, frame: tk.Frame, changed_colors: None | list[str] = None): 
    """
    Creates a dummy view in a given frame with buttons to change the background, mid, and foreground colors.
    If colors are provided, it uses them; otherwise, it loads the colors from a JSON file.
    It also provides Save and Back buttons
    """
    def change_bg():
        new_color = askcolor(title='')[1]
        create_dummy_view(path, main, return_colors, theme, frame, [new_color, mid, fg, fontf])
        
    def change_mid():
        new_color = askcolor(title='')[1]
        create_dummy_view(path, main, return_colors, theme, frame, [bg, new_color, fg, fontf])
        
    def change_fg():
        new_color = askcolor(title='')[1]
        create_dummy_view(path, main, return_colors, theme, frame, [bg, mid, new_color, fontf])
    
    if changed_colors:
        bg, mid, fg, fontf = changed_colors
        for widget in frame.winfo_children():
            widget.destroy()
    else:
        with open(path, 'r') as file:
            palette = json.load(file)
        bg = palette[theme]['BGCOLOR']
        mid = palette[theme]['MIDCOLOR']
        fg = palette[theme]['FGCOLOR']
        fontf = palette['FONTF']
    
    frame.config(background=bg)
    
    change_color_buttons = tk.Frame(frame, background=bg)
    change_color_buttons.pack(fill='x', side='top')
    for name, func in zip(('Background', 'Between MID', 'Foreground'), (change_bg, change_mid, change_fg)):
        tk.Button(
            change_color_buttons,
            font = (fontf, 15),
            background = bg,
            foreground = fg,
            activebackground = fg,
            activeforeground = bg,
            text = name,
            command = func
        ).pack(side='left', fill='x', expand=True)
    
    middle_frame = tk.Frame(frame, background=bg)
    middle_frame.pack(fill='both', expand=True)
    
    tk.Label(
        middle_frame,
        font = (fontf, 10),
        background = mid,
        foreground = fg,
        padx = 20,
        pady = 20,
        text = 'Lorem Ipsum'
    ).pack(expand=True)
    
    tk.Label(
        middle_frame,
        font = (fontf, 20),
        background = bg,
        foreground = fg,
        text = 'Ex nihilo nihil fit'
    ).pack(fill='both', expand=True)
    
    save_back_buttons = tk.Frame(frame, background=bg)
    save_back_buttons.pack(fill='x', side='bottom')
    
    tk.Button(
        save_back_buttons,
        text = 'Save',
        bg = mid,
        fg = fg,
        activebackground = mid,
        activeforeground = bg,
        font = (fontf, 30, 'bold'),
        command = lambda x = [theme, bg, mid, fg]: return_colors(x)
    ).pack(side='left', fill='x', expand=True, padx=(20,10), pady=20)
    
    tk.Button(
        save_back_buttons,
        text = 'Back',
        bg = mid,
        fg = fg,
        activebackground = mid,
        activeforeground = bg,
        font = (fontf, 30, 'bold'),
        command = main
    ).pack(side='left', fill='x', expand=True, padx=(10,20), pady=20)

def save_new_colors(self: 'CrateSettings', colors: list[str]):
    """Saves the new colors chosen by the user"""
    theme, bg, mid, fg = colors
    
    with open(self.App.palette_json_path, 'r') as file:
        palette = json.load(file)
    
    if bg:
        self.App.BGCOLOR = bg
        palette[theme]['BGCOLOR'] = bg
    if mid:
        self.App.MIDCOLOR = mid
        palette[theme]['MIDCOLOR'] = mid
    if fg:
        self.App.FGCOLOR = fg
        palette[theme]['FGCOLOR'] = fg
    
    with open(self.App.palette_json_path, 'w') as file:
        json.dump(palette, file, ensure_ascii=False, indent=4)
        
    self.main()

def change_font(self: 'CrateSettings'):
    """Creates scrollable canvas, when calls create_fonts"""
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
    font_canvas = tk.Canvas(canvas_container)
    self.content = tk.Frame(font_canvas, background=self.App.BGCOLOR)
    scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=font_canvas.yview)
    font_canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    font_canvas.pack(side="left", fill="both", expand=True)
    canvas_frame = font_canvas.create_window((0, 0), window=self.content, anchor="nw")
    
    #| Links scroll with content
    def on_frame_configure(event):
        font_canvas.configure(scrollregion=font_canvas.bbox('all'))
    self.content.bind('<Configure>', on_frame_configure)
    
    #| Changes width of canvas
    def frame_width(event):
        canvas_width = event.width
        font_canvas.itemconfig(canvas_frame, width = canvas_width)
    font_canvas.bind('<Configure>', frame_width)
    
    #| Enables mousewheel
    def on_mousewheel(event):
        if font_canvas.winfo_exists():
            font_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    font_canvas.bind_all('<MouseWheel>', on_mousewheel)
    
    self.App.window.update_idletasks()
    self.create_fonts()
    
def create_fonts(self: 'CrateSettings'):
    """Creates buttons, each button represent diffrent font from system. On button click calls modify_json_font"""
    
    with open(self.App.font_names_path, 'r') as file:
        reader = csv.DictReader(file)
        valid = {x['FONTNAME'] for x in reader}
    
    for font_name in font.families():
        if font_name in valid:
            tk.Button(
                self.content,
                font = (font_name, 15),
                anchor = 'w',
                background = self.App.MIDCOLOR,
                foreground = self.App.FGCOLOR,
                activeforeground = self.App.BGCOLOR,
                activebackground = self.App.FGCOLOR,
                text = f"{font_name}",
                command = lambda x = font_name: self.save_new_font(x)
            ).pack(expand=True, fill='x', pady=(10,0))
            
            for msg in (string.ascii_uppercase, string.ascii_lowercase, string.digits):
                tk.Label(
                    self.content,
                    font = (font_name, 15),
                    anchor = 'w',
                    background = self.App.BGCOLOR,
                    foreground = self.App.FGCOLOR,
                    text = msg
                ).pack(expand=True, fill='x')

def save_new_font(self: 'CrateSettings', font_name):
    """Modify palette.json with new font for app"""
    with open(self.App.palette_json_path, 'r') as file:
        palette = json.load(file)
    
    palette['FONTF'] = font_name
    self.App.FONTF = font_name
    
    with open(self.App.palette_json_path, 'w') as file:
        json.dump(palette, file, ensure_ascii=False, indent=4)
    
    self.main()