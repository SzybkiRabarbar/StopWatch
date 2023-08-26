
# TODO zrobić zapisywanie danych do pliku csv
# TODO okienko wyskakujące po wyłączeniu timera z prośbą wybrania opisu i wybór szablonu
# TODO połączyć dane z csv z kalendarzem (wyśweitlanie contentu, calevents)
# TODO dodać kalendarz z czasem pracy i czasem przerwy (main_time, break_time)
    # TODO dodawanie do kalendarza po zamknięciu okiennka timer
    # TODO tkcalendar, ale po kliknięciu na dzień otwiera się aktywność
    # TODO oznaczyć na tkcalendarze że jest jakaś aktywnosć danego dnia (mała kropka, zmieniony kolor itp)
    # TODO zrobienie szablonów (aktywność można podpiąć pod jakąś aktywnosć (np programowanie) z unikalnym kolorem, nazwą opisem itp)
# TODO obszar podsumowania zliczający wszystkie aktywności dla każdego szablonu
# TODO w kalendarzu dodać przesyłanie do google calendar (pomyśleć jak połączyc różne sesje, jak je zapisać w lokalnym kalenadarzu, przy dodawaniu podać nazwe, opis itp)
# TODO sprawdzić zapisywanie plików również po nieoczekikwanym zamknięciu aplikacji
# TODO sprawdzić zmiane domyślnego paska
# TODO sprawdzić czy jest możliwość inplementacji animacji
# TODO przerobić baze na sql i mergować indeksami

import tkinter as tk
from tkinter import ttk, messagebox
import tkcalendar as tkc
from datetime import datetime
import pandas as pd
from os.path import exists

class TimerApp():
    
    def __init__(self) -> None:
        self.time_reset()
    
    def time_reset(self) -> None:
        self.main_time = False
        self.break_time = False
        self.current_break_time = False
        
    def open_timer_window(self):
        
        """
        Shows a window with main timer, button, break timer and currnet break timer.
        Normally main timer counts down the time,but then button is unclicked break timer and currnet break timer starts counts.
        Break timer stores time of sum of all 'breaks' and current break timer stores time of current break.
        """
        
        def update(time: tk.IntVar, timer: tk.StringVar) -> tuple[tk.IntVar, tk.StringVar]:
            """
            Updates given time and return new time value and string timer to display
            """
            time.set(time.get() + 1)
            seconds = time.get()
            timer.set(f"{seconds // 3600}:{seconds // 60 % 60 :02d}:{seconds % 60 :02d}")
            return (time, timer)

        def time_loop():
            """
            Checks if update main timer or stop timer and updates it
            """
            #! loop dont stop after WM_DELETE_WINDOW and rises (this error ocurs in other loops in code)
            #? 'invalid command name "loop" while executing "loop" ("after" script)'
            if is_running.get():
                button_text.set("STOP")
                self.current_break_time.set(0)
                self.main_time, self.main_timer = update(self.main_time, self.main_timer)
            else:
                button_text.set("START")
                self.current_break_time, self.current_break_timer = update(self.current_break_time, self.current_break_timer)
                self.break_time, self.break_timer = update(self.break_time, self.break_timer)    
            timer_window.after(1000, time_loop) 

        self.root.destroy()
        self.start_time = datetime.now()
        timer_window = tk.Tk()
        timer_window.title("Timer")
        # icon = tk.PhotoImage(file="timer-icon.png")
        # timer_window.iconphoto(True,icon)
        timer_window.geometry("300x150" + self.window_shift)
        timer_window.config(bg="#011638")
        
        #| main_time stores the time (in sec)
        self.main_time = tk.IntVar(value=0)
        #| main_timer stores formated main_time (H:M:S)
        self.main_timer = tk.StringVar()
        main_label = tk.Label(timer_window, 
            font=("Ariel",40),
            pady=12,
            fg="#E8C1C5",
            bg="#011638",
            textvariable=self.main_timer)
        main_label.pack()

        
        #| stop_button indicates wich time should be updated (main_time or break_time)
        is_running = tk.IntVar(value=1)
        button_text = tk.StringVar(value="STOP")
        stop_button = tk.Checkbutton(timer_window, 
            font=("Ariel",15),
            fg="#D499B9",
            bg="#011638",
            selectcolor="#2E294E", 
            variable=is_running, 
            textvariable=button_text, 
            indicatoron=False)
        stop_button.pack()
        
        #| Frame for breaks timers
        frame = tk.Frame(timer_window)
        frame.pack()

        #| Style for breaks timers
        style = ttk.Style()
        style.configure("BW.TLabel",
            font=("Ariel",15),
            foreground="#E8C1C5", 
            background="#011638"
            )

        #| break_time stores the time (in sec)
        self.break_time = tk.IntVar(value=0)
        #| break_timer stores formated break_time (H:M:S)
        self.break_timer = tk.StringVar()
        break_label = ttk.Label(frame,
            style="BW.TLabel",
            textvariable=self.break_timer)
        break_label.pack(side="left")

        pipe = ttk.Label(frame,
            style="BW.TLabel",
            text="|")
        pipe.pack(side="left")

        #| current_break_time stores the time (in sec)
        self.current_break_time = tk.IntVar(value=0)
        #| current_break_timer stores formated current_break_time (H:M:S)
        self.current_break_timer = tk.StringVar()
        current_break_label = ttk.Label(frame,
            style="BW.TLabel",
            textvariable=self.current_break_timer)
        current_break_label.pack(side="right")

        time_loop()
        
        timer_window.protocol("WM_DELETE_WINDOW", lambda: [timer_window.destroy(), self.open_save_window()])
    
    def open_save_window(self):
        """
        Show a window with times in session, field to enter desc and to pick activity
        """
        def save_to_csv_and_quit():
            """
            Saves data to csv and destroys window
            """
            df = pd.DataFrame({
                'date': [self.start_time.strftime('%Y-%m-%d')],
                'start_time': [self.start_time.strftime('%H:%M:%S')],
                'main_time': [self.main_time.get()],
                'break_time': [self.break_time.get()],
                'desc': ['desc not added yet'],
                'activity': ['smth']
            })
            print(df)
            df.to_csv('data.csv',index=False, mode='a', header=not exists('data.csv'))
            save_window.destroy()
            self.open_main_window()
        
        save_window = tk.Tk()
        save_window.title("Save your time")
        save_window.geometry("400x400" + self.window_shift)
        save_window.config(bg="#011638")
        
        #| Contains main_timer and break_timer from session
        time_frame = tk.Frame(save_window)
        time_frame.config(background='#011638')
        time_frame.pack(pady=20)
        
        session_time_style = ttk.Style()
        session_time_style.configure("BW.TLabel",
            font=("Ariel",15),
            foreground="#E8C1C5", 
            background="#011638")
        
        heading_main_time = ttk.Label(time_frame,
            style="BW.TLabel",
            text="Dedicated time:")
        heading_main_time.pack()
        
        session_main_time = tk.Label(time_frame,
            font=("Ariel",40),
            fg="#E8C1C5",
            bg="#011638",
            text=self.main_timer.get())
        session_main_time.pack()
        
        heading_break_time = ttk.Label(time_frame,
            style="BW.TLabel",
            text="Breaks time:")
        heading_break_time.pack()
        
        session_break_label = ttk.Label(time_frame,
            style="BW.TLabel",
            text=self.break_timer.get()
            )
        session_break_label.pack()
        
        text_widget = tk.Text(save_window,
            bg="light yellow",
            font=("Ink Free",15),
            height=5,
            width=25,
            padx=20,
            pady=20,
            fg="purple")
        text_widget.pack()
        
        #| Run save_to_csv_and_quit func
        save_button = tk.Button(save_window,
                                text="Save",
                                command=save_to_csv_and_quit)
        save_button.pack()
        
        save_window.protocol("WM_DELETE_WINDOW", lambda: [save_window.destroy(), self.open_main_window()])
    
    def open_calendar_window(self):
        """
        Shows window with calendar where you can pick date and show data form picked day
        """
        def grab_date():
        
            if self.temp != cal.get_date():
                self.temp = cal.get_date()
                print("Wybrana data to:", cal.get_date())
                content.config(text="Wybrana data to: " + cal.get_date())
        
            cal_window.after(100,grab_date)
        
        self.root.destroy()
        cal_window = tk.Tk()
        cal_window.title("Calendar")
        cal_window.geometry("400x400" + self.window_shift)
        cal_window.config(bg="#011638")
        self.temp = ''
        
        
        # if self.main_time and self.break_time and self.current_break_time:
        #     txt = f'{self.main_time.get()} | {self.break_time.get()} | {self.current_break_time.get()}'
        #     t = tk.Label(cal_window,
        #         text=txt)
        #     t.pack()
        
        ## Time
        today = datetime.now()
        y = today.year
        m = today.month
        d = today.day
        
        #* przekształcić na liste pobraną z csv
        lst = [
            ['2023-08-22', '', 'smth'],
            ['2023-08-20', '', 'running'],
            ['2023-08-18', '', 'smth'],
            ['2023-08-10', '', 'running']
        ]
        
        activites = [
            ['running', '#8f9491', '#F3EAF4'],
            ['smth', '#2C5530', '#F3FFB6']
        ]
        
        cal = tkc.Calendar(cal_window, selectmode='day', year=y, month=m, day=d, date_pattern='y-mm-dd')
        
        for line in lst:
            date = datetime.strptime(line[0], '%Y-%m-%d')
            cal.calevent_create(date, line[1], line[2])
        
        for activity in activites:
            cal.tag_config(activity[0], background=activity[1], foreground=activity[2])

        cal.pack(pady=20)
        
        content = tk.Label(cal_window, text="")
        content.pack(pady=20)
        
        grab_date()
        
        cal_window.protocol("WM_DELETE_WINDOW", lambda: [cal_window.destroy(), self.open_main_window()])
        
    def open_main_window(self):
        """
        MENU
        """
        self.root = tk.Tk()
        self.root.title("TimerApp")
        self.root.config(bg="#011638")
        # icon = tk.PhotoImage(file="timer-icon.png")
        # self.root.iconphoto(True,icon)
        self.window_shift = f"+{self.root.winfo_screenwidth() // 3}+{self.root.winfo_screenheight() // 3}"
        self.root.geometry(self.window_shift)
        
        button_to_timer = tk.Button(self.root,
            text="Timer",
            fg="#011638", 
            bg="#E8C1C5",
            activebackground="#D499B9",
            pady= 12,
            padx= 50,
            font=("Ariel", 40 , 'bold'),
            command=self.open_timer_window)
        button_to_timer.pack(fill='x', padx=30, pady=20)
        
        button_to_calendar = tk.Button(self.root,
            text='Calendar',
            fg="#011638", 
            bg="#E8C1C5",
            activebackground="#D499B9",
            pady= 12,
            padx= 50,
            font=("Ariel", 40 , 'bold'),
            command=self.open_calendar_window)
        button_to_calendar.pack(fill='x', padx=30, pady=20)

        self.root.mainloop()
    
            
if __name__=="__main__":
    t = TimerApp()
    t.open_main_window()