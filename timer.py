import tkinter as tk
from tkinter import ttk

def update(time: tk.IntVar, timer: tk.StringVar) -> tuple[tk.IntVar, tk.StringVar]:
    time.set(time.get() + 1)
    seconds = time.get()
    timer.set(f"{seconds // 3600}:{seconds // 60 % 60 :02d}:{seconds % 60 :02d}")
    return (time, timer)

def loop():
    global main_time, main_timer
    global current_break_time, current_break_timer
    global break_time, break_timer
    if is_running.get():
        button_text.set("STOP")
        current_break_time.set(0)
        main_time, main_timer = update(main_time, main_timer)
    else:
        button_text.set("START")
        current_break_time, current_break_timer = update(current_break_time, current_break_timer)
        break_time, break_timer = update(break_time, break_timer)
    window.after(1000, loop)

window = tk.Tk()
window.title("Timer")
#icon = tk.PhotoImage(file="timer-icon.png")
#window.iconphoto(True,icon)
window.geometry("300x150")
window.config(bg="#011638")

style = ttk.Style()
style.configure("BW.TLabel",
                font=("Ariel",15),
                foreground="#E8C1C5", 
                background="#011638"
                )

main_time = tk.IntVar(value=0)
break_time = tk.IntVar(value=0)
current_break_time = tk.IntVar(value=0)
is_running = tk.IntVar(value=1)

main_timer = tk.StringVar()
main_label = tk.Label(window, 
                      font=("Ariel",40),
                      pady=12,
                      fg="#E8C1C5",
                      bg="#011638",
                      textvariable=main_timer)
main_label.pack()

button_text = tk.StringVar(value="STOP")
stop_button = tk.Checkbutton(window, 
                             font=("Ariel",15),
                             fg="#D499B9",
                             bg="#011638",
                             selectcolor="#2E294E", 
                             variable=is_running, 
                             textvariable=button_text, 
                             indicatoron=False)
stop_button.pack()

frame = tk.Frame(window)
frame.pack()

break_timer = tk.StringVar()
break_label = ttk.Label(frame,
                       style="BW.TLabel",
                       textvariable=break_timer)
break_label.pack(side="left")

pipe = ttk.Label(frame,
                style="BW.TLabel",
                text="|")
pipe.pack(side="left")

current_break_timer = tk.StringVar()
current_break_label = ttk.Label(frame,
                               style="BW.TLabel",
                               textvariable=current_break_timer)
current_break_label.pack(side="right")

loop()
window.mainloop()