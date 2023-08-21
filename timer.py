
# TODO dodać menu [timer, kalendarz]
# TODO sprawić ze po otwarciu timera albo kalendarza, root się wyłącza i po zamknięciu timera/ kal włącza się spowrotem 
# TODO dodać kalendarz z czasem pracy i czasem przerwy (main_time, break_time)
    # TODO dodawanie do kalendarza po zamknięciu okiennka timer
# TODO w kalendarzu dodać przesyłanie do google calendar (pomyśleć jak połączyc różne sesje, jak je zapisać w lokalnym kalenadarzu)
# TODO sprawdzić zapisywanie plików również po nieoczekikwanym zamknięciu aplikacji
# TODO sprawdzić zmiane domyślnego paska
# TODO sprawdzić czy jest możliwość inplementacji animacji

import tkinter as tk
from tkinter import ttk

class Timer():
    
    def __init__(self) -> None:
        self.root = tk.Tk()
        
    def open_timer_window(self):
        
        def update(time: tk.IntVar, timer: tk.StringVar) -> tuple[tk.IntVar, tk.StringVar]:
            time.set(time.get() + 1)
            seconds = time.get()
            timer.set(f"{seconds // 3600}:{seconds // 60 % 60 :02d}:{seconds % 60 :02d}")
            return (time, timer)

        def time_loop():
            if is_running.get():
                button_text.set("STOP")
                self.current_break_time.set(0)
                self.main_time, self.main_timer = update(self.main_time, self.main_timer)
            else:
                button_text.set("START")
                self.current_break_time, self.current_break_timer = update(self.current_break_time, self.current_break_timer)
                self.break_time, self.break_timer = update(self.break_time, self.break_timer)
            timer_window.after(1000, time_loop)

        timer_window = tk.Toplevel(self.root)
        timer_window.title("Timer")
        icon = tk.PhotoImage(file="timer-icon.png")
        timer_window.iconphoto(True,icon)
        timer_window.geometry("300x150")
        timer_window.config(bg="#011638")

        style = ttk.Style()
        style.configure("BW.TLabel",
            font=("Ariel",15),
            foreground="#E8C1C5", 
            background="#011638"
            )
        
        self.main_time = tk.IntVar(value=0)
        self.break_time = tk.IntVar(value=0)
        self.current_break_time = tk.IntVar(value=0)
        is_running = tk.IntVar(value=1)

        self.main_timer = tk.StringVar()
        main_label = tk.Label(timer_window, 
            font=("Ariel",40),
            pady=12,
            fg="#E8C1C5",
            bg="#011638",
            textvariable=self.main_timer)
        main_label.pack()

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

        frame = tk.Frame(timer_window)
        frame.pack()

        self.break_timer = tk.StringVar()
        break_label = ttk.Label(frame,
            style="BW.TLabel",
            textvariable=self.break_timer)
        break_label.pack(side="left")

        pipe = ttk.Label(frame,
            style="BW.TLabel",
            text="|")
        pipe.pack(side="left")

        self.current_break_timer = tk.StringVar()
        current_break_label = ttk.Label(frame,
            style="BW.TLabel",
            textvariable=self.current_break_timer)
        current_break_label.pack(side="right")

        time_loop()

    def open_calendar_window(self):
        pass
        
    def main(self):
        self.root.title("TimerApp")
        self.root.config(bg="#011638")
        icon = tk.PhotoImage(file="timer-icon.png")
        self.root.iconphoto(True,icon)
        
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
    t = Timer()
    t.main()