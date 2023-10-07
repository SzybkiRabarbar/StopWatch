import tkinter as tk
from tkinter import ttk
from pandas import DataFrame, read_sql_query
from tkinter.colorchooser import askcolor
from tkinter import messagebox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Source.Timer.timer import CreateTimer

def open_save_window(self: 'CreateTimer'):
        """
        Opens a TopLevel window with labels showing times in session,
        textbox to enter desc, combobox to pick activity and save button.\n
        Save button appends [
            date, start_time, main_time, break_time, desc and activity number
        ] to DB.data
        """
        self.App.window.after_cancel(self.App.loop_id)
        self.save_window = tk.Toplevel(self.App.root)
        self.save_window.resizable(False, False)
        self.save_window.grab_set()
        self.save_window.title("Save Your Progres")
        self.save_window.iconbitmap(self.App.static_path / 'icon.ico')
        self.save_window.config(background=self.App.MIDCOLOR)
        self.save_window.geometry("320x385" + self.get_shift())
        
        #| TIME FRAME
        #| Contains main_timer, break_timer from session and static text
        time_frame = tk.Frame(self.save_window)
        time_frame.config(background=self.App.MIDCOLOR)
        time_frame.pack(pady=20)
        
        ttk.Label(
            time_frame,
            background = self.App.MIDCOLOR,
            foreground = self.App.FGCOLOR,
            font = (self.App.FONTF,15),
            text = "Dedicated time:"
        ).pack()
        
        tk.Label(
            time_frame,
            background = self.App.MIDCOLOR,
            foreground = self.App.FGCOLOR,
            font = (self.App.FONTF, 40),
            text = self.main_timer.get()
        ).pack()
        
        ttk.Label(
            time_frame,
            background = self.App.MIDCOLOR,
            foreground = self.App.FGCOLOR,
            font = (self.App, 15),
            text = "Breaks time:"
        ).pack()
        
        ttk.Label(
            time_frame,
            background = self.App.MIDCOLOR,
            foreground = self.App.FGCOLOR,
            font = (self.App.FONTF, 15),
            text = self.break_timer.get()
        ).pack()
        
        #| TEXT WIDGET
        #| Takes desc
        self.text_widget = tk.Text(
            self.save_window,
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            font = (self.App.FONTF, 15),
            wrap = 'word',
            height = 5,
            width = 25,
            padx = 5,
            pady = 5
        )
        self.text_widget.pack()
        
        #| BOTTOM FRAME
        #| Contains save_button and activity combobox
        bottom = tk.Frame(self.save_window)
        bottom.config(background=self.App.MIDCOLOR)
        bottom.pack()
        
        #| Run save_and_quit func
        tk.Button(
            bottom,
            background = self.App.MIDCOLOR,
            foreground = self.App.FGCOLOR,
            text = "Save",
            command = self.save_and_quit
        ).pack(side='left', padx=(0,10))
        
        #| ComboBox to pick activity
        self.activities_values = read_sql_query('SELECT name FROM "activities"', self.App.conn)['name'].tolist()
        self.activities_cbox = ttk.Combobox(
            bottom,
            values = self.activities_values
        )
        self.activities_cbox.pack(side='right')
        
        #| Instructions that are executed after the program closes
        self.save_window.protocol("WM_DELETE_WINDOW", lambda: [self.save_window.destroy(), self.App.open_menu()])

def save_and_quit(self: 'CreateTimer'):
    """Saves data to DB and destroys TopLevel window"""
    picked_activity = self.activities_cbox.get().upper() if self.activities_cbox.get() else 'SOMETHING'
    
    #| If picked activity isn't in activities, takes inputs about bgcolor and fgcolor then append to activities db [name,bg,fg]
    if not picked_activity in self.activities_values: 
        bg_color = askcolor(
            title = f"Choose backgroud color for {picked_activity}",
            color = 'red',
            parent = self.save_window
        )[1]
        fg_color = askcolor(
            title = f"Choose text color for {picked_activity}",
            color = 'blue',
            parent = self.save_window
        )[1]
        activity_df = DataFrame({
            'name': [picked_activity],
            'bg': [bg_color if bg_color else '#000000'],
            'fg': [fg_color if fg_color else '#ffffff'],
            'auto': [0]
        })
        activity_df.to_sql('activities', self.App.conn, if_exists='append', index=False)
    
    activity_data = read_sql_query(f'SELECT id, auto FROM activities WHERE "name" == "{picked_activity}"', self.App.conn)
    date = self.start_time.strftime('%Y-%m-%d')
    start_time = self.start_time.strftime('%H:%M:%S')
    desc = self.text_widget.get('1.0', tk.END).strip()
    df = DataFrame({
        'date': [date],
        'start_time': [start_time],
        'main_time': [self.main_time.get()],
        'break_time': [self.break_time.get()],
        'desc': [desc],
        'activity': [activity_data.iloc[0, 0]]
    })
    df.to_sql('data', self.App.conn, if_exists='append',index=False)
    
    if activity_data.iloc[0, 1]:
        self.App.append_to_google_calendar(picked_activity, date, start_time, int(self.main_time.get() + int(self.break_time.get())), desc)
    
    self.save_window.destroy()
    self.App.open_menu()