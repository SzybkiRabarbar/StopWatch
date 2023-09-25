from datetime import datetime
import tkinter as tk
from tkinter import ttk
from pandas import DataFrame, read_sql_query
from tkinter.colorchooser import askcolor
from tkinter import messagebox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from timer_app import TimerApp

class CreateTimer:
    """
    Creates main timer, checkbutton, exit button, break timer and currnet break timer.\n
    Normally main timer counts down the time,
    but then checkbutton is unclicked break timer and currnet break timer starts counts.\n
    Break timer stores time of sum of all 'breaks' 
    and current break timer stores time of current break.
    """
    def __init__(self, App: 'TimerApp') -> None:
        self.App = App
        self.main()
    
    def main(self):
        self.App.clear_window()
        self.start_time = datetime.now()
        self.App.root.geometry("300x200")
        
        #| Time stores int representing seconds
        #| Timer stores formated time representing Hour:Minute:Second (H:MM:SS)
        self.main_time = tk.IntVar(value=0)
        self.main_timer = tk.StringVar()
        self.break_time = tk.IntVar(value=0)
        self.break_timer = tk.StringVar()
        self.current_break_time = tk.IntVar(value=0)
        self.current_break_timer = tk.StringVar()
        
        self.is_running = tk.IntVar(value=1)
        self.button_text = tk.StringVar(value="STOP")
        
        tk.Label(
            self.App.window, 
            font = ("Ariel",40),
            pady = 12,
            fg = self.App.FGCOLOR,
            bg = self.App.BGCOLOR,
            textvariable = self.main_timer
        ).pack()

        #| Contains buttons
        button_container = tk.Frame(self.App.window)
        button_container.config(background=self.App.BGCOLOR)
        button_container.pack()
        
        #| Indicades witch timer shoud run
        tk.Checkbutton(
            button_container, 
            font = (self.App.FONTF,15),
            fg = self.App.FGCOLOR,
            bg = self.App.BGCOLOR,
            selectcolor = self.App.MIDCOLOR,
            variable = self.is_running, 
            textvariable = self.button_text, 
            indicatoron = False
        ).pack(side='left', fill='y', padx=5)
        
        #| Exits timer and open save_window
        tk.Button(
            button_container,
            font = (self.App.FONTF,15),
            fg = self.App.FGCOLOR,
            bg = self.App.BGCOLOR,
            activebackground = self.App.FGCOLOR,
            activeforeground = self.App.BGCOLOR,
            text = 'Exit',
            command = self.open_save_window
        ).pack(side='right', padx=5)
        
        #| Contains break timers
        break_frame = tk.Frame(self.App.window)
        break_frame.pack()

        #| Style for breaks timers
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            font = (self.App.FONTF, 15),
            foreground = self.App.FGCOLOR, 
            background = self.App.BGCOLOR
        )

        #| Break label
        ttk.Label(
            break_frame,
            style = "BW.TLabel",
            textvariable = self.break_timer
        ).pack(side="left")

        #| Small Separator
        ttk.Label(
            break_frame,
            style = "BW.TLabel",
            text = "|"
        ).pack(side="left")

        #| Current break label
        ttk.Label(
            break_frame,
            style = "BW.TLabel",
            textvariable = self.current_break_timer
        ).pack(side="right")

        #* LOOP
        self.time_loop()
    
    def time_loop(self):
        """
        Loop.\n
        Checks IF is_running THEN update main timer ELSE update stop timer
        """        
        if self.is_running.get():
            self.button_text.set("STOP")
            self.current_break_time.set(0)
            self.main_time, self.main_timer = self.update(self.main_time, self.main_timer)
        else:
            self.button_text.set("START")
            self.current_break_time, self.current_break_timer = self.update(self.current_break_time, self.current_break_timer)
            self.break_time, self.break_timer = self.update(self.break_time, self.break_timer)    
        self.App.loop_id = self.App.window.after(1000, self.time_loop) 
    
    def update(self, time: tk.IntVar, timer: tk.StringVar) -> tuple[tk.IntVar, tk.StringVar]:
        """
        Adds 1 to given time and return updated time (int) and new timer (H:MM:SS)
        """
        time.set(time.get() + 1)
        seconds = time.get()
        timer.set(f"{seconds // 3600}:{seconds // 60 % 60 :02d}:{seconds % 60 :02d}")
        return (time, timer)
    
    def open_save_window(self):
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
        self.save_window.attributes('-topmost', 'true')
        self.save_window.grab_set()
        self.save_window.title("Save Your Progres")
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
            bg = "light yellow",
            font = ("Consolas",15),
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
        
    def get_shift(self) -> str:
        """
        Returns actual shift of root
        """
        t = self.App.root.geometry()
        return t[t.index('+')::]
    
    def save_and_quit(self):
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
            is_succes, res = self.App.append_to_google_calendar(picked_activity, date, start_time, int(self.main_time.get() + int(self.break_time.get())), desc)
            if is_succes:
                messagebox.showinfo(picked_activity, f"{picked_activity} was succesful added to your calendar", parent=self.save_window)
            else:
                messagebox.showerror(picked_activity, f"Action wasn't added to Google Calendar.\nError occurs:\n{res}", parent=self.save_window)
        
        self.save_window.destroy()
        self.App.open_menu()
    