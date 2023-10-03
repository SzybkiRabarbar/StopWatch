import tkinter as tk
from os import remove as remove_file
from tkinter import messagebox
from pandas import read_sql_query

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Source.Settings.settings import CrateSettings
    
def rm_token(self: 'CrateSettings'):
    """Remove token with connection with google calendar"""
    try: 
        remove_file(self.App.db_path / 'token.json')
        messagebox.showinfo('Data removed', 'Data was removed')
    except FileNotFoundError:
        messagebox.showwarning('No data', 'Data not found')
    
def pick_auto_append_activities(self: 'CrateSettings'):
    """Auto append action from picked activities to google calendar"""
    self.App.clear_window()
    
    def save_auto():
        marked = [str(activity_list[x][0]) for x in lbox.curselection()]
        curr = self.App.conn.cursor()
        if marked:
            curr.execute(   
                f'UPDATE activities '
                f'SET auto = CASE ' 
                f'WHEN id IN ({", ".join(marked)}) THEN 1 '
                f'ELSE 0 '
                f'END; '
            )
        else:
            curr.execute(
                'UPDATE activities SET auto = 0;'
            )
        self.App.conn.commit()
        self.App.open_settings()
        
    tk.Label(
        self.App.window,
        font = (self.App.FONTF, 10),
        background = self.App.BGCOLOR,
        foreground = self.App.FGCOLOR,
        text = 'Select activities to be automatically added to your Google calendar'
    ).pack(pady=(10,0))
    
    lbox = tk.Listbox(
        self.App.window,
        font = (self.App, 15),
        background = self.App.BGCOLOR,
        foreground = self.App.FGCOLOR,
        selectmode = tk.MULTIPLE
    )
    lbox.pack(pady=10, padx=30, fill='x')
    activity_list = read_sql_query("SELECT id, name, auto FROM activities", self.App.conn).values.tolist()
    for _, name, auto in activity_list:
        lbox.insert(tk.END, ' ' + name)
        if auto == 1:
            lbox.selection_set(tk.END)
    
    b_frame = tk.Frame(self.App.window)
    b_frame.pack()
    
    tk.Button(
        b_frame,
        font = (self.App, 15),
        background = self.App.BGCOLOR,
        foreground = self.App.FGCOLOR,
        text = 'Save',
        command = save_auto
    ).pack(side='left')
    
    tk.Button(
        b_frame,
        font = (self.App, 15),
        background = self.App.BGCOLOR,
        foreground = self.App.FGCOLOR,
        text = 'Cancel',
        command = self.App.open_settings
    ).pack(side='right')