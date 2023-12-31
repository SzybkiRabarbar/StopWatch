import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
import tkcalendar as tkc
from datetime import datetime
import pandas as pd
from os.path import exists

class TimerApp():
    
    def __init__(self) -> None:
        self.time_reset()
        self.is_files()
        self.icon = False
    
    def is_files(self):
        pass
        # if not exists('data.csv'):
            
    
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
            Loop
            Checks if update main timer or stop timer and updates it
            """        
            if is_running.get():
                button_text.set("STOP")
                self.current_break_time.set(0)
                self.main_time, self.main_timer = update(self.main_time, self.main_timer)
            else:
                button_text.set("START")
                self.current_break_time, self.current_break_timer = update(self.current_break_time, self.current_break_timer)
                self.break_time, self.break_timer = update(self.break_time, self.break_timer)    
            self.loop_id = timer_window.after(1000, time_loop) 

        self.root.destroy()
        self.start_time = datetime.now()
        timer_window = tk.Tk()
        timer_window.title("Timer")
        timer_window.geometry("300x150" + self.window_shift)
        timer_window.resizable(False, False)
        timer_window.config(bg="#011638")
        
        #* MAIN TIMER
        #| main_time stores the time (in sec)
        self.main_time = tk.IntVar(value=0)
        #| main_timer stores formated main_time (H:M:S)
        self.main_timer = tk.StringVar()
        main_label = tk.Label(
            timer_window, 
            font=("Ariel",40),
            pady=12,
            fg="#E8C1C5",
            bg="#011638",
            textvariable=self.main_timer
        )
        main_label.pack()

        #* STOP BUTTON
        #| stop_button indicates wich time should be updated (main_time or break_time)
        #| changes is_running bool var with is used in time_loop func
        is_running = tk.IntVar(value=1)
        button_text = tk.StringVar(value="STOP")
        stop_button = tk.Checkbutton(
            timer_window, 
            font=("Ariel",15),
            fg="#D499B9",
            bg="#011638",
            selectcolor="#2E294E", 
            variable=is_running, 
            textvariable=button_text, 
            indicatoron=False
        )
        stop_button.pack()
        
        #* BREAKS TIMERS FRAME
        #| Frame for breaks timers
        break_frame = tk.Frame(timer_window)
        break_frame.pack()

        #| Style for breaks timers
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            font=("Ariel",15),
            foreground="#E8C1C5", 
            background="#011638"
        )

        #* BREAK TIMER
        #| break_time stores the time (in sec)
        self.break_time = tk.IntVar(value=0)
        #| break_timer stores formated break_time (H:M:S)
        self.break_timer = tk.StringVar()
        break_label = ttk.Label(
            break_frame,
            style="BW.TLabel",
            textvariable=self.break_timer
        )
        break_label.pack(side="left")

        ttk.Label(
            break_frame,
            style="BW.TLabel",
            text="|"
        ).pack(side="left")

        #* CURRENT BREAK TIMER
        #| current_break_time stores the time (in sec)
        self.current_break_time = tk.IntVar(value=0)
        #| current_break_timer stores formated current_break_time (H:M:S)
        self.current_break_timer = tk.StringVar()
        current_break_label = ttk.Label(
            break_frame,
            style="BW.TLabel",
            textvariable=self.current_break_timer
        )
        current_break_label.pack(side="right")

        #* LOOP
        time_loop()
        
        #| Instructions that are executed after the program closes
        timer_window.protocol("WM_DELETE_WINDOW", lambda: [timer_window.after_cancel(self.loop_id), timer_window.destroy(), self.open_save_window()])
    
    def open_save_window(self):
        """
        Show a window with times in session, field to enter desc and to pick activity, saves data in csv
        """
        def save_to_csv_and_quit():
            """
            Saves data to csv and destroys window
            """
            picked_activity = activity_cbox.get().upper() if activity_cbox.get() else 'SOMETHING'
            
            #| If picked activity isn't in activity.csv, takes inputs about bgcolor and fgcolor then append to activity db [name,bg,fg]
            if not picked_activity in activity_values: 
                bg_color = askcolor(
                    title=f"Choose backgroud color for {picked_activity}",
                    color='pink'
                )[1]
                fg_color = askcolor(
                    title=f"Choose text color for {picked_activity}",
                    color='blue'
                )[1]
                activity_df = pd.DataFrame({
                    'name': [picked_activity],
                    'bg': [bg_color if bg_color else '#000000'],
                    'fg': [fg_color if fg_color else '#ffffff']
                })
                activity_df.to_csv('activity.csv', index=False, mode='a', header=False)
                
            df = pd.DataFrame({
                'date': [self.start_time.strftime('%Y-%m-%d')],
                'start_time': [self.start_time.strftime('%H:%M:%S')],
                'main_time': [self.main_time.get()],
                'break_time': [self.break_time.get()],
                'desc': [text_widget.get('1.0', tk.END).strip()],
                'activity': [picked_activity]
            })
            df.to_csv('data.csv',index=False, mode='a', header=not exists('data.csv'))
            save_window.destroy()
            self.open_main_window()
        
        save_window = tk.Tk()
        save_window.title("Save your time")
        save_window.geometry("400x400" + self.window_shift)
        save_window.resizable(False, False)
        save_window.config(bg="#011638")
        
        #* TIME FRAME
        #| Contains main_timer, break_timer from session and static text
        time_frame = tk.Frame(save_window)
        time_frame.config(background='#011638')
        time_frame.pack(pady=20)
        
        session_time_style = ttk.Style()
        session_time_style.configure(
            "BW.TLabel",
            font=("Ariel",15),
            foreground="#E8C1C5", 
            background="#011638"
        )
        
        heading_main_time = ttk.Label(
            time_frame,
            style="BW.TLabel",
            text="Dedicated time:"
        )
        heading_main_time.pack()
        
        session_main_time = tk.Label(
            time_frame,
            font=("Ariel",40),
            fg="#E8C1C5",
            bg="#011638",
            text=self.main_timer.get()
        )
        session_main_time.pack()
        
        heading_break_time = ttk.Label(
            time_frame,
            style="BW.TLabel",
            text="Breaks time:"
        )
        heading_break_time.pack()
        
        session_break_label = ttk.Label(
            time_frame,
            style="BW.TLabel",
            text=self.break_timer.get()
        )
        session_break_label.pack()
        
        #* TEXT WIDGET
        #| Takes desc
        text_widget = tk.Text(
            save_window,
            bg="light yellow",
            font=("Ink Free",15),
            height=5,
            width=25,
            padx=20,
            pady=20,
            fg="purple"
        )
        text_widget.pack()
        
        #* BOTTOM FRAME
        #| Contains save_button and activity combobox
        bottom = tk.Frame(save_window)
        bottom.pack()
        
        #| Run save_to_csv_and_quit func
        save_button = tk.Button(
            bottom,
            text="Save",
            command=save_to_csv_and_quit
        )
        save_button.pack(side='left', padx=(0,10))
        
        #| ComboBox to pick activity
        activity_values = [x[0] for x in pd.read_csv('activity.csv').values.tolist()]
        activity_cbox = ttk.Combobox(
            bottom,
            values=activity_values
        )
        activity_cbox.pack(side='right')
        
        #| Instructions that are executed after the program closes
        save_window.protocol("WM_DELETE_WINDOW", lambda: [save_window.destroy(), self.open_main_window()])
    
    def open_calendar_window(self):
        """
        Shows window with calendar where you can pick date and show data from picked day
        """
        def grab_date_loop():
            """
            Loop
            Grabs date from calendar, call print_data func
            """
            if self.picked_date != cal.get_date():
                self.picked_date = cal.get_date()
                content_title.config(text=cal.get_date())
                print_data()
            self.loop_id = cal_window.after(100,grab_date_loop)
            
        def print_data():
            """
            Prints grid with timestaps and actions from picked date 
            """
            def debug():
                print(action)
                print(start_time)
                print(duration)
                
            actions = self.data[self.data['date'] == self.picked_date]        
            
            #| Deletes data from previos picked day
            for widget in content.winfo_children(): 
                widget.destroy()
            
            #| Sets a minimum height for each row
            for i in range(96):
                content.grid_rowconfigure(i, minsize=20)

            #| Sets the minimum width for the first column and the width of the second column to all available space
            content.grid_columnconfigure(0, minsize=50)
            content.grid_columnconfigure(1, weight=1)

            #| Adds times and black line above in first column
            t = 0
            for i in range(96):
                if i % 4 == 3:
                    frame = tk.Frame(content, highlightbackground="black", highlightthickness=1, width=50, height=1)
                    frame.grid(row=i, column=0, sticky='s')
                elif not i % 4:
                    separator = tk.Label(content, text=f"{t}:00")
                    separator.grid(row=i, column=0)
                    t += 1
                    
            #| Adds buttons to seccond column. Each button represent action (the longer the activity, the bigger the button)
            for action in actions.values.tolist():
                start_time = [int(x) for x in action[1].split(':')]
                start_time = ((start_time[0] * 60) + start_time[1] + (1 if start_time[2] else 0)) // 15
                # start_time = int(((start_time[0] * 3600) + (start_time[1] * 60) + start_time[2]) / 60)
                duration = int(((action[2] + action[3]) / 60) // 15) 
                activity = [activity for activity in activites if activity[0] == action[5]][0]
                # debug()
                button = tk.Button(
                    content,
                    font=('Ariel', 1),
                    text='', 
                    background = activity[1],
                    foreground = activity[2],
                    command = lambda x = [action, activity]: on_button_click(x)
                )
                
                #| Rowspan value must be positive integer
                if duration: 
                    button.configure(font =('Ariel', 15), text=f"{action[5]}")
                    button.grid(
                        column = 1,
                        row = start_time,
                        rowspan = duration + 1,
                        sticky='nwes'
                    )
                else:
                    button.grid(
                        column = 1,
                        row = start_time,
                        sticky='nwes'
                    )
                
                #| Moves scrollbar to first action
                if t == 24:
                    canvas.yview_moveto(str(float((start_time // 4) / 24)))
                    t += 1
                        
        def on_button_click(arg: list[list, list]):
            """
            Opens new window with picked action data
            """
            print(arg)
            action, activity = arg
            action_window = tk.Toplevel(cal_window)
            action_window.title(action[5])
            action_window.geometry(self.window_shift)
            action_window.config(bg=activity[1])
            tk.Label(
                action_window,
                font=('Ariel', 15),
                wraplength=400,
                text=
                f"{action[5]}\n"
                f"{action[2] // 3600}:{(action[2] % 3600) // 60 :02d}:{(action[2] % 3600) % 60 :02d}\n"
                f"{action[3] // 3600}:{(action[3] % 3600) // 60 :02d}:{(action[3] % 3600) % 60 :02d}\n"
                f"{action[4].strip()}"
            ).pack(padx=20,pady=20)
            
        self.root.destroy()
        cal_window = tk.Tk()
        cal_window.title("Calendar")
        cal_window.geometry("400x500" + self.window_shift)
        cal_window.resizable(False, False)
        self.picked_date = ''
        
        today = datetime.now()
        y = today.year
        m = today.month
        d = today.day

        #* CALENDAR
        #| creates calendar with events
        cal = tkc.Calendar(cal_window, selectmode='day', year=y, month=m, day=d, date_pattern='y-mm-dd')
        
        self.data = pd.read_csv('data.csv')
        for action in self.data.values.tolist():
            date = datetime.strptime(action[0], '%Y-%m-%d')
            cal.calevent_create(date, action[4], action[5])
        
        activites = pd.read_csv('activity.csv').values.tolist()
        for activity in activites:
            cal.tag_config(activity[0], background=activity[1], foreground=activity[2])

        cal.pack(pady=(20,5))
        
        #* CONTENT
        
        content_title = tk.Label(
            cal_window,
            font=("Ariel",15),
            text=""
        )
        content_title.pack(pady=(0,5))
        
        ## canvas_container <- canvas <- content[grid]
        canvas_container = tk.Frame(cal_window)
        canvas_container.pack(fill='both')
        
        #| canvas contains scrollable content
        canvas = tk.Canvas(canvas_container)
        content = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas_frame = canvas.create_window((0, 0), window=content, anchor="nw")
        
        #| Links scroll with content
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        content.bind("<Configure>", on_frame_configure)
        
        #| Changes width of canvas
        def frame_width(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_frame, width = canvas_width)
        canvas.bind('<Configure>', frame_width)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        cal_window.update_idletasks()
        
        #* LOOP
        grab_date_loop()
        
        #| Instructions that are executed after the program closes
        cal_window.protocol("WM_DELETE_WINDOW", lambda: [cal_window.after_cancel(self.loop_id), cal_window.destroy(), self.open_main_window()])
    
    def open_summary_window(self):
        
        def clear():
            for widget in content.winfo_children(): 
                widget.destroy()
        
        def exit():
            summ_window.destroy()
            self.open_main_window()
        
        def buttons_generator():
            """
            Draws buttons corresponding to each activity, click returns summary
            """
            clear()
            for i, (activity, bg_color, fg_color) in enumerate(df_activity.values.tolist()):
                tk.Button(
                    content,
                    font=('Ariel', 20),
                    background=bg_color,
                    foreground=fg_color,
                    activebackground=fg_color,
                    activeforeground=bg_color,
                    text=f"{activity}",
                    command=lambda x = activity: generate_summary(x)
                ).grid(row=i, sticky='nsew')
        
        def generate_summary(activity: str):
            """
            Draws a summary for the selected activity
            """
            clear()
            
            #* TOP
            #| Summary of picked action
            up_data_grid = tk.Frame(content)
            up_data_grid.config(background="#011638")
            up_data_grid.pack()
            
            style = ttk.Style()
            style.configure(
                "BW.TLabel",
                font=("Ariel",15),
                foreground="#E8C1C5", 
                background="#011638"
            )
            
            #| Title
            tk.Label(
                up_data_grid,
                font=("Ariel",30),
                foreground="#E8C1C5", 
                background="#011638",
                text=f"{activity}"
            ).grid(column=0, columnspan=3, row=0)
            
            #| Times Performed
            ttk.Label(
                up_data_grid,
                text=f"Performed: {df_data[df_data['activity'] == activity].shape[0]}",
                style="BW.TLabel"
            ).grid(column=0, columnspan=3, row=1)
            
            #| Column names
            columns_names = [
                'Time', 'Activity', 'Break'
            ]
            for i, name in enumerate(columns_names):
                ttk.Label(
                    up_data_grid,
                    text=name,
                    style="BW.TLabel"
                ).grid(column=i, row=2, sticky='w', padx=30)
            
            #| Columns content
            description_data = [
                'Sum', 'Mean', 'Max'
            ]
            main_data = [
                df_data.loc[df_data['activity'] == activity, 'main_time'].sum(),
                int(df_data.loc[df_data['activity'] == activity, 'main_time'].mean()),
                df_data.loc[df_data['activity'] == activity, 'main_time'].max()
            ]
            break_data = [
                df_data.loc[df_data['activity'] == activity, 'break_time'].sum(),
                int(df_data.loc[df_data['activity'] == activity, 'break_time'].mean()),
                df_data.loc[df_data['activity'] == activity, 'break_time'].max()
            ] 
            for c_id, d in enumerate([description_data, main_data, break_data]):
                for i, value in enumerate(d):
                    txt = f"{value // 3600}:{value // 60 % 60 :02d}:{value % 60 :02d}" if c_id else f"{value}"
                    ttk.Label(
                        up_data_grid,
                        text=txt,
                        style="BW.TLabel"
                    ).grid(column=c_id, row=3+i, sticky='w', padx=30)
            
            tk.Frame( #| Separator
                content,
                background='#E8C1C5',
                bd=0,
                height=1
            ).pack(fill='x', pady=20)
            
            #* MIDDLE
            
            def change_color(action):
                print('color',action)
            
            tk.Button(
                content,
                font=("Ariel",15),
                foreground="#E8C1C5", 
                background="#011638",
                activebackground="#E8C1C5",
                activeforeground="#011638",
                text="Change Color",
                command=lambda x=activity: change_color(x)
            ).pack()
            
            tk.Frame( #| Separator
                content,
                background='#E8C1C5',
                bd=0,
                height=1
            ).pack(fill='x', pady=20)
            
            #* BOTTOM
            #| Draws data in scrollable canvas
            outer_frame = tk.Frame(content)
            outer_frame.pack(padx=10, pady=10, fill='both', expand=True)

            canvas = tk.Canvas(outer_frame)
            inner_frame = tk.Frame(canvas)
            inner_frame.columnconfigure(0, weight=1)
            scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)

            canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas_frame = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            def onFrameConfigure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            inner_frame.bind("<Configure>", onFrameConfigure)
            
            def onCanvasConfigure(event):
                canvas.itemconfigure(canvas_frame, width=event.width)
            canvas.bind("<Configure>", onCanvasConfigure)
            
            for i, row in enumerate(df_data[df_data['activity'] == activity].values.tolist()):
                tk.Label(
                    inner_frame,
                    text=" | ".join([str(x) for x in row])
                ).grid(row=i, sticky='we')
        
        self.root.destroy()
        summ_window = tk.Tk()
        summ_window.title("Summary")
        # summ_window.geometry(f"{summ_window.winfo_screenwidth()}x{summ_window.winfo_screenheight()}")
        summ_window.attributes('-fullscreen', True)
        
        #| Takes data from DBs
        df_data = pd.read_csv('data.csv')
        df_activity = pd.read_csv('activity.csv')
        
        top_bar = tk.Frame(summ_window)
        top_bar.pack(fill='x')
        
        tk.Button(
            top_bar,
            text="Summary",
            command=buttons_generator
        ).pack(side='left')
        
        tk.Button(
            top_bar,
            text='Exit',
            command=exit
        ).pack(side='right')
        
        
        content = tk.Frame(summ_window, background='#011638')
        content.columnconfigure(0, weight=1)
        for i in range(df_activity.shape[0]): 
            content.rowconfigure(i, weight=1, uniform='group1')
        content.pack(fill='both', expand=True)
        
        buttons_generator()
        
        #| Instructions that are executed after the program closes
        summ_window.protocol("WM_DELETE_WINDOW", lambda: [summ_window.destroy(), self.open_main_window()])
    
    def open_main_window(self):
        """
        MENU
        """
        self.root = tk.Tk()
        self.root.title("TimerApp")
        self.root.config(bg="#011638")
        self.root.resizable(False, False)
        if not self.icon:
            self.icon = tk.PhotoImage(file="timer-icon.png")
            self.root.iconphoto(True, self.icon)
        self.window_shift = f"+{self.root.winfo_screenwidth() // 3}+{self.root.winfo_screenheight() // 3}"
        self.root.geometry(self.window_shift)
        
        button_to_timer = tk.Button(
            self.root,
            text="Timer",
            fg="#011638", 
            bg="#E8C1C5",
            activebackground="#D499B9",
            pady= 12,
            padx= 50,
            font=("Ariel", 40 , 'bold'),
            command=self.open_timer_window
        )
        button_to_timer.pack(fill='x', padx=30, pady=20)
        
        button_to_calendar = tk.Button(
            self.root,
            text='Calendar',
            fg="#011638", 
            bg="#E8C1C5",
            activebackground="#D499B9",
            pady= 12,
            padx= 50,
            font=("Ariel", 40 , 'bold'),
            command=self.open_calendar_window
        )
        button_to_calendar.pack(fill='x', padx=30, pady=20)
        
        button_to_summary = tk.Button(
            self.root,
            text='Summary',
            fg="#011638", 
            bg="#E8C1C5",
            activebackground="#D499B9",
            pady= 12,
            padx= 50,
            font=("Ariel", 40 , 'bold'),
            command=self.open_summary_window
        )
        button_to_summary.pack(fill='x', padx=30, pady=20)

        self.root.mainloop()
     
if __name__=="__main__":
    t = TimerApp()
    t.open_main_window()