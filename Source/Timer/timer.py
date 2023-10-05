from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from os import path
from pygame import mixer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from timer_app import TimerApp

class CreateTimer:
    """
    Creates main timer, checkbutton, exit button, break timer, currnet break timer and Count Down button.\n
    Normally main timer counts down the time,
    but then checkbutton is unclicked break timer and currnet break timer starts counts.\n
    Break timer stores time of sum of all 'breaks' 
    and current break timer stores time of current break.
    """
    from Source.Timer.save_window import open_save_window, save_and_quit
    def __init__(self, App: 'TimerApp') -> None:
        self.App = App
        self.main()
    
    def vars_init(self):
        """
        Initializes instance variables.\n
        'Time' stores int representing seconds.\n
        'Timer' stores formated time representing Hour:Minute:Second (H:MM:SS).
        """
        self.main_time = tk.IntVar(value=0)
        self.main_timer = tk.StringVar()
        self.break_time = tk.IntVar(value=0)
        self.break_timer = tk.StringVar(value='0:00:00')
        self.current_break_time = tk.IntVar(value=0)
        self.current_break_timer = tk.StringVar(value='0:00:00')
        self.countdown_time = tk.IntVar(value=0)
        self.countdown_timer = tk.StringVar(value='Count Down Time')
        
        self.is_running = tk.IntVar(value=1)
        self.button_text = tk.StringVar(value="STOP")    
    
    def main(self):
        self.App.clear_window()
        self.start_time = datetime.now()
        self.App.root.geometry("300x260")
        
        self.vars_init()
        mixer.init()
        
        tk.Label(
            self.App.window, 
            font = (self.App.FONTF, 40),
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

        tk.Button(
            self.App.window,
            font = (self.App.FONTF,15),
            fg = self.App.FGCOLOR,
            bg = self.App.BGCOLOR,
            activebackground = self.App.FGCOLOR,
            activeforeground = self.App.BGCOLOR,
            textvariable = self.countdown_timer,
            command = self.set_countdown_time
        ).pack(pady=5, padx=5, side='bottom', fill="both", expand=True)
        
        #* LOOP
        self.time_loop()
    
    def time_loop(self):
        """
        Loop.\n
        Checks IF is_running THEN update main timer ELSE update stop timer.\n
        Checks IF countdown_time THEN calls update_countdown_time
        """        
        if self.is_running.get():
            self.button_text.set("STOP")
            self.current_break_time.set(0)
            self.main_time, self.main_timer = self.update(self.main_time, self.main_timer)
        else:
            self.button_text.set("START")
            self.current_break_time, self.current_break_timer = self.update(self.current_break_time, self.current_break_timer)
            self.break_time, self.break_timer = self.update(self.break_time, self.break_timer)
        if self.countdown_time.get():
            self.update_countdown_time()
        self.App.loop_id = self.App.window.after(1000, self.time_loop) 
    
    def update(self, time: tk.IntVar, timer: tk.StringVar) -> tuple[tk.IntVar, tk.StringVar]:
        """Adds 1 to given time and return updated time (int) and new timer (H:MM:SS)"""
        time.set(time.get() + 1)
        seconds = time.get()
        timer.set(f"{seconds // 3600}:{seconds // 60 % 60 :02d}:{seconds % 60 :02d}")
        return (time, timer)
    
    def update_countdown_time(self):
        """Subtracts 1 from countdown time and update countdown_timer"""
        self.countdown_time.set(self.countdown_time.get() - 1)
        seconds = self.countdown_time.get()
        if seconds:
            self.countdown_timer.set(f"{seconds // 3600}:{seconds // 60 % 60 :02d}:{seconds % 60 :02d}")
        else:
            self.countdown_timer.set('Count Down Time')
            mixer.music.load(self.App.static_path / 'boom.mp3')
            mixer.music.play(loops=0)
    
    def get_shift(self) -> str:
        """Returns current shift of root"""
        t = self.App.root.geometry()
        return t[t.index('+')::]
    
    def set_countdown_time(self):
        """IF countdown_time THEN set countdown_time to 0 ELSE calss open_countdown_window"""
        if self.countdown_time.get():
            self.countdown_time.set(value=0)
            self.countdown_timer.set(value='Count Down Time')
        else:
            self.open_countdown_window()
    
    def open_countdown_window(self):
        """
        Opens new TopLevel window.\n
        In window creates label, combobox and button.\n
        On click sets value from combobox as countdown_time
        """
        countdown_window = tk.Toplevel(self.App.root)
        countdown_window.resizable(False, False)
        countdown_window.attributes('-topmost', 'true')
        countdown_window.grab_set()
        countdown_window.title('Set countdown')
        countdown_window.iconbitmap(self.App.static_path / 'icon.ico')
        countdown_window.config(background=self.App.MIDCOLOR)
        countdown_window.geometry(self.get_shift())
        
        content = tk.Frame(countdown_window, background=self.App.BGCOLOR)
        content.pack(padx=20, pady=20)
        
        tk.Label(
            content,
            font = (self.App.FONTF, 15),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            text = 'Set countdown (in minutes)'
        ).pack()
        
        example = [15,30,45,60]
        picked_minutes = ttk.Combobox(
            content,
            values = example
        )
        picked_minutes.pack(pady=5)
        
        buttons = tk.Frame(content)
        buttons.pack(fill='x')
        
        def save_countdown_time():
            if picked_minutes.get().isnumeric():
                self.countdown_time.set(value=int(picked_minutes.get()) * 60)
            else:
                messagebox.showerror('Error', 'Data you entered is incorrect. You must enter the time in minutes (only numbers 0-9)')
            countdown_window.destroy()
        
        tk.Button(
            buttons,
            font = (self.App.FONTF, 15),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            activebackground = self.App.FGCOLOR,
            activeforeground = self.App.BGCOLOR,
            text = 'Save',
            command = save_countdown_time
        ).pack(side='left', fill='x', expand=True)

        tk.Button(
            buttons,
            font = (self.App.FONTF, 15),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            activebackground = self.App.FGCOLOR,
            activeforeground = self.App.BGCOLOR,
            text = 'Cancel',
            command = countdown_window.destroy
        ).pack(side='right', fill='x', expand=True)