
# TODO infotoplvl
    # * zmiana desc
    # * usunięcie 
    # * zmiana na inną aktywność
# TODO dark i light mode
# TODO w kalendarzu dodać przesyłanie do google calendar (pomyśleć jak połączyc różne sesje, jak je zapisać w lokalnym kalenadarzu, przy dodawaniu podać nazwe, opis itp)
# TODO dodać powiadomienie w timer (użytkownik może ustawić sobie budzik na np 45 minut itp)
# TODO pobawic się wielkością guzików w summary
# TODO pole z kalendarzem zrobić dłuższe

import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
import tkinter.font as tkFont
import tkcalendar as tkc
from datetime import datetime, timedelta
import pandas as pd
from sqlite3 import connect
from ctypes import windll

class TimerApp():
    
    EFFECTSCOLOR = '#3e4042' # button color effects in the title bar
    BARCOLOR = '#1e1e1c' # title bar color
    BGCOLOR = '#25292e' # background color
    FGCOLOR = '#cbc8cb' # text color

    def __init__(self) -> None:
        self.time_reset()
        self.conn = connect('sqlite.db')
        self.custom_title_bar()

    def after_init(self):
        self.window_shift = f"+{self.root.winfo_screenwidth() // 3}+{self.root.winfo_screenheight() // 3}"
        self.root.resizable(False, False)
        self.open_main_window()
    
    def fetch_dfs(self):
        self.df_data = pd.read_sql_query(
            'SELECT data.date, data.start_time, data.main_time, data.break_time, data.desc, activities.name AS activity '
            'FROM data '
            'JOIN activities ON data.activity = activities.id',
            self.conn)
        
        self.df_activity = pd.read_sql_query('SELECT name, bg, fg FROM activities', self.conn)    
    
    def clear_window(self):
        for widget in self.window.winfo_children(): 
                widget.destroy()
        try:
            self.window.after_cancel(self.loop_id)
        except AttributeError:
            pass
    
    def custom_title_bar(self):
        #@ https://github.com/Terranova-Python/Tkinter-Menu-Bar
        self.root = tk.Tk()
        self.root.title('Timer')
        self.root.overrideredirect(True) # turns off title bar, geometry
        #root.iconbitmap("your_icon.ico") # to show your own icon 
        self.root.minimized = False # only to know if root is minimized
        self.root.maximized = False # only to know if root is maximized

        self.root.config(bg="#25292e")
        title_bar = tk.Frame(self.root, bg=TimerApp.BARCOLOR, relief='raised', bd=0,highlightthickness=0)

        def set_appwindow(mainWindow): # to display the window icon on the taskbar, 
                                    # even when using root.overrideredirect(True
            # Some WindowsOS styles, required for task bar integration
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            # Magic
            hwnd = windll.user32.GetParent(mainWindow.winfo_id())
            stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            stylew = stylew & ~WS_EX_TOOLWINDOW
            stylew = stylew | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
        
            mainWindow.wm_withdraw()
            mainWindow.after(10, lambda: mainWindow.wm_deiconify())
            
        def minimize_me():
            # so you can't see the window when is minimized
            self.root.attributes("-alpha",0) 
            self.root.minimized = True       

        def deminimize(event):
            # so you can see the window when is not minimized
            self.root.focus() 
            self.root.attributes("-alpha",1) 
            if self.root.minimized == True:
                self.root.minimized = False                              

        # put a close button on the title bar
        self.close_button = tk.Button(title_bar, text='  ×  ', command=lambda: [self.root.destroy()],bg=TimerApp.BARCOLOR,padx=2,pady=2,font=("calibri", 13),bd=0,fg=TimerApp.FGCOLOR,highlightthickness=0)
        self.return_button = tk.Button(title_bar, text=' ⟲ ', command=self.open_main_window,bg=TimerApp.BARCOLOR,padx=2,pady=2,bd=0,fg=TimerApp.FGCOLOR,font=("calibri", 13),highlightthickness=0)
        self.minimize_button = tk.Button(title_bar, text=' 🗕 ',command=minimize_me,bg=TimerApp.BARCOLOR,padx=2,pady=2,bd=0,fg=TimerApp.FGCOLOR,font=("calibri", 13),highlightthickness=0)
        title_bar_title = tk.Label(title_bar, text='TimerApp', bg=TimerApp.BARCOLOR,bd=0,fg=TimerApp.FGCOLOR,font=("helvetica", 10),highlightthickness=0)

        # a frame for the main area of the window, this is where the actual app will go
        self.window = tk.Frame(self.root, bg=TimerApp.BGCOLOR,highlightthickness=0)

        # pack the widgets
        title_bar.pack(fill='x')
        self.close_button.pack(side='right',ipadx=7,ipady=1)
        self.return_button.pack(side='right',ipadx=7,ipady=1)
        self.minimize_button.pack(side='right',ipadx=7,ipady=1)
        title_bar_title.pack(side='left', padx=10)
        self.window.pack(expand=1, fill='both') # replace this with your main Canvas/Frame/etc.

        # bind title bar motion to the move window function

        def changex_on_hovering(event):
            self.close_button['bg']='red'
            
        def returnx_to_normalstate(event):
            self.close_button['bg']=TimerApp.BARCOLOR
            
        def change_size_on_hovering(event):
            self.return_button['bg']=TimerApp.EFFECTSCOLOR
            
        def return_size_on_hovering(event):
            self.return_button['bg']=TimerApp.BARCOLOR
            
        def changem_size_on_hovering(event):
            self.minimize_button['bg']=TimerApp.EFFECTSCOLOR
            
        def returnm_size_on_hovering(event):
            self.minimize_button['bg']=TimerApp.BARCOLOR
            
        def get_pos(event): # this is executed when the title bar is clicked to move the window
            if self.root.maximized == False:
        
                xwin = self.root.winfo_x()
                ywin = self.root.winfo_y()
                startx = event.x_root
                starty = event.y_root

                ywin = ywin - starty
                xwin = xwin - startx
        
                def move_window(event): # runs when window is dragged
                    self.root.config(cursor="fleur")
                    self.root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

                def release_window(event): # runs when window is released
                    self.root.config(cursor="arrow")
                                
                title_bar.bind('<B1-Motion>', move_window)
                title_bar.bind('<ButtonRelease-1>', release_window)
                title_bar_title.bind('<B1-Motion>', move_window)
                title_bar_title.bind('<ButtonRelease-1>', release_window)
            else:
                self.return_button.config(text=" 🗖 ")
                self.root.maximized = not self.root.maximized

        title_bar.bind('<Button-1>', get_pos) # so you can drag the window from the title bar
        title_bar_title.bind('<Button-1>', get_pos) # so you can drag the window from the title 

        # button effects in the title bar when hovering over buttons
        self.close_button.bind('<Enter>',changex_on_hovering)
        self.close_button.bind('<Leave>',returnx_to_normalstate)
        self.return_button.bind('<Enter>', change_size_on_hovering)
        self.return_button.bind('<Leave>', return_size_on_hovering)
        self.minimize_button.bind('<Enter>', changem_size_on_hovering)
        self.minimize_button.bind('<Leave>', returnm_size_on_hovering)

        # resize the window width
        resizex_widget = tk.Frame(self.window,bg=TimerApp.BGCOLOR,cursor='sb_h_double_arrow')
        resizex_widget.pack(side='right',ipadx=2,fill='y')

        def resizex(event):
            xwin = self.root.winfo_x()
            difference = (event.x_root - xwin) - self.root.winfo_width()
            
            if self.root.winfo_width() > 150 : # 150 is the minimum width for the window
                try:
                    self.root.geometry(f"{ self.root.winfo_width() + difference }x{ self.root.winfo_height() }")
                except:
                    pass
            else:
                if difference > 0: # so the window can't be too small (150x150)
                    try:
                        self.root.geometry(f"{ self.root.winfo_width() + difference }x{ self.root.winfo_height() }")
                    except:
                        pass
                    
            resizex_widget.config(bg=TimerApp.BGCOLOR)

        resizex_widget.bind("<B1-Motion>",resizex)

        # resize the window height
        resizey_widget = tk.Frame(self.window,bg=TimerApp.BGCOLOR,cursor='sb_v_double_arrow')
        resizey_widget.pack(side='bottom',ipadx=2,fill='x')

        def resizey(event):
            ywin = self.root.winfo_y()
            difference = (event.y_root - ywin) - self.root.winfo_height()

            if self.root.winfo_height() > 150: # 150 is the minimum height for the window
                try:
                    self.root.geometry(f"{ self.root.winfo_width()  }x{ self.root.winfo_height() + difference}")
                except:
                    pass
            else:
                if difference > 0: # so the window can't be too small (150x150)
                    try:
                        self.root.geometry(f"{ self.root.winfo_width()  }x{ self.root.winfo_height() + difference}")
                    except:
                        pass

            resizex_widget.config(bg=TimerApp.BGCOLOR)

        resizey_widget.bind("<B1-Motion>",resizey)

        self.root.bind("<FocusIn>",deminimize) # to view the window by clicking on the window icon on the taskbar
        self.root.after(10, lambda: set_appwindow(self.root)) # to see the icon on the task bar
        
        self.after_init()
                
        self.root.mainloop()
            
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
            self.loop_id = self.window.after(1000, time_loop) 

        self.clear_window()
        self.start_time = datetime.now()
        self.root.geometry("300x200" + self.window_shift)
        # timer_window.resizable(False, False)
        self.window.config(bg=TimerApp.BGCOLOR)
        
        #| main_time stores the time (in sec)
        self.main_time = tk.IntVar(value=0)
        #| main_timer stores formated main_time (H:M:S)
        self.main_timer = tk.StringVar()
        #| is_running indicates wich time should be updated (main_time or break_time)
        is_running = tk.IntVar(value=1)
        #| button_text stores STOP or START
        button_text = tk.StringVar(value="STOP")
        #| break_time stores the time of summ of breaks (in sec)
        self.break_time = tk.IntVar(value=0)
        #| break_timer stores formated break_time (H:M:S)
        self.break_timer = tk.StringVar()
        #| current_break_time stores the time of current break (in sec)
        self.current_break_time = tk.IntVar(value=0)
        #| current_break_timer stores formated current_break_time (H:M:S)
        self.current_break_timer = tk.StringVar()
        
        tk.Label(
            self.window, 
            font=("Ariel",40),
            pady=12,
            fg=TimerApp.FGCOLOR,
            bg=TimerApp.BGCOLOR,
            textvariable=self.main_timer
        ).pack()

        #| Contains buttons
        button_container = tk.Frame(self.window)
        button_container.config(background=TimerApp.BGCOLOR)
        button_container.pack()
        
        #| Indicades witch timer shoud run
        tk.Checkbutton(
            button_container, 
            font=("Ariel",15),
            fg=TimerApp.FGCOLOR,
            bg=TimerApp.BGCOLOR,
            selectcolor=TimerApp.EFFECTSCOLOR, 
            variable=is_running, 
            textvariable=button_text, 
            indicatoron=False
        ).pack(side='left',fill='y', padx=5)
        
        #| Exits timer and open save_window
        tk.Button(
            button_container,
            font=("Ariel",15),
            fg=TimerApp.FGCOLOR,
            bg=TimerApp.BGCOLOR,
            activebackground=TimerApp.FGCOLOR,
            activeforeground=TimerApp.BGCOLOR,
            text='Exit',
            command=self.open_save_window
        ).pack(side='right', padx=5)
        
        #| Contains break timers
        break_frame = tk.Frame(self.window)
        break_frame.pack()

        #| Style for breaks timers
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            font=("Ariel",15),
            foreground=TimerApp.FGCOLOR, 
            background=TimerApp.BGCOLOR
        )

        #| Break label
        ttk.Label(
            break_frame,
            style="BW.TLabel",
            textvariable=self.break_timer
        ).pack(side="left")

        #| Small Separator
        ttk.Label(
            break_frame,
            style="BW.TLabel",
            text="|"
        ).pack(side="left")

        #| Current break label
        ttk.Label(
            break_frame,
            style="BW.TLabel",
            textvariable=self.current_break_timer
        ).pack(side="right")

        #* LOOP
        time_loop()
    
    def open_save_window(self):
        """
        Show a window with times in session, field to enter desc and to pick activity, saves data in csv
        """
        def save_and_quit():
            """
            Saves data and destroys window
            """
            picked_activity = activities_cbox.get().upper() if activities_cbox.get() else 'SOMETHING'
            
            #| If picked activity isn't in activities, takes inputs about bgcolor and fgcolor then append to activities db [name,bg,fg]
            if not picked_activity in activities_values: 
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
                activity_df.to_sql('activities', self.conn, if_exists='append', index=False)
                
            df = pd.DataFrame({
                'date': [self.start_time.strftime('%Y-%m-%d')],
                'start_time': [self.start_time.strftime('%H:%M:%S')],
                'main_time': [self.main_time.get()],
                'break_time': [self.break_time.get()],
                'desc': [text_widget.get('1.0', tk.END).strip()],
                'activity': [pd.read_sql_query(f'SELECT id FROM activities WHERE "name" == "{picked_activity}"', self.conn).iloc[0, 0]]
            })
            df.to_sql('data', self.conn, if_exists='append',index=False)
            save_window.destroy()
            self.open_main_window()
        
        self.window.after_cancel(self.loop_id)
        save_window = tk.Toplevel(self.root)
        save_window.resizable(False, False)
        save_window.attributes('-topmost', 'true')
        save_window.grab_set()
        save_window.title("Save Your Progres")
        save_window.geometry("320x385" + self.window_shift)
        
        #| TIME FRAME
        #| Contains main_timer, break_timer from session and static text
        time_frame = tk.Frame(save_window)
        time_frame.pack(pady=20)
        
        ttk.Label(
            time_frame,
            font=("Ariel",15),
            text="Dedicated time:"
        ).pack()
        
        tk.Label(
            time_frame,
            font=("Ariel",40),
            text=self.main_timer.get()
        ).pack()
        
        ttk.Label(
            time_frame,
            font=("Ariel",15),
            text="Breaks time:"
        ).pack()
        
        ttk.Label(
            time_frame,
            font=("Ariel",15),
            text=self.break_timer.get()
        ).pack()
        
        #| TEXT WIDGET
        #| Takes desc
        text_widget = tk.Text(
            save_window,
            bg="light yellow",
            font=("Consolas",15),
            height=5,
            width=25,
            padx=5,
            pady=5
        )
        text_widget.pack()
        
        #| BOTTOM FRAME
        #| Contains save_button and activity combobox
        bottom = tk.Frame(save_window)
        bottom.pack()
        
        #| Run save_and_quit func
        tk.Button(
            bottom,
            text="Save",
            command=save_and_quit
        ).pack(side='left', padx=(0,10))
        
        #| ComboBox to pick activity
        activities_values = pd.read_sql_query('SELECT name FROM "activities"', self.conn)['name'].tolist()
        activities_cbox = ttk.Combobox(
            bottom,
            values=activities_values
        )
        activities_cbox.pack(side='right')
        
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
            self.loop_id = self.window.after(100,grab_date_loop)
            
        def print_data():
            """
            Prints grid with timestaps and actions from picked date 
            """        
            actions = self.df_data[self.df_data['date'] == self.picked_date] 
            
            #| Deletes data from previos picked day
            for widget in content.winfo_children(): 
                widget.destroy()
            
            #| Sets a minimum height for each row
            for i in range(96):
                content.grid_rowconfigure(i, minsize=20)

            #| Sets the minimum width for the first column and the width of the second column to all available space
            content.grid_columnconfigure(0, minsize=50)
            content.grid_columnconfigure(1, weight=1)

            #| Adds hours and black line above in first column
            t = 0
            for i in range(96):
                if i % 4 == 3:
                    frame = tk.Frame(content, highlightbackground="black", highlightthickness=1, width=50, height=1)
                    frame.grid(row=i, column=0, sticky='s')
                elif not i % 4:
                    separator = tk.Label(content, text=f"{t}:00", background=TimerApp.FGCOLOR, foreground=TimerApp.BGCOLOR)
                    separator.grid(row=i, column=0)
                    t += 1
                    
            #| Adds buttons to seccond column. Each button represent action (the longer the activity, the bigger the button), button trigger on_click()
            for action in actions.values.tolist():
                start_time = [int(x) for x in action[1].split(':')]
                start_time = ((start_time[0] * 60) + start_time[1] + (1 if start_time[2] else 0)) // 15
                
                duration = int(((action[2] + action[3]) / 60) // 15) 
                activity = [activity for activity in activites if activity[0] == action[5]][0]
                
                button = tk.Button(
                    content,
                    font=('Ariel', 1),
                    text='', 
                    background = activity[1],
                    foreground = activity[2],
                    command = lambda x = [action, activity]: self.open_info_Toplevel(x)
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
            
        self.clear_window()
        self.root.geometry("400x500" + self.window_shift)
        self.picked_date = ''
        
        today = datetime.now()
        y, m, d = today.year, today.month, today.day

        #| CALENDAR
        #| creates calendar with events
        cal = tkc.Calendar(self.window, selectmode='day', year=y, month=m, day=d, date_pattern='y-mm-dd')
        
        self.fetch_dfs()
        
        for action in self.df_data.values.tolist():
            date = datetime.strptime(action[0], '%Y-%m-%d')
            cal.calevent_create(date, action[4], action[5])
        
        activites = self.df_activity.values.tolist()
        
        for activity in activites:
            cal.tag_config(activity[0], background=activity[1], foreground=activity[2])
        cal.pack(pady=(20,5))
        
        #| CONTENT
        
        content_title = tk.Label(
            self.window,
            font=("Ariel",15),
            background=TimerApp.BGCOLOR,
            foreground=TimerApp.FGCOLOR,
            text=""
        )
        content_title.pack(pady=(0,5))
        
        #| Stores canvas
        canvas_container = tk.Frame(self.window)
        canvas_container.pack(fill='both')
        
        #| Canvas contains scrollable content
        canvas = tk.Canvas(canvas_container)
        content = tk.Frame(canvas, background=TimerApp.FGCOLOR)
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
        
        #| Enables mousewheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.window.update_idletasks()
        
        #* LOOP
        grab_date_loop()
    
    def open_summary_window(self):
        
        def clear():
            for widget in content.winfo_children(): 
                widget.destroy()
        
        def buttons_generator():
            """
            Draws buttons corresponding to each activity, click returns summary
            """
            clear()
            for i, (activity, bg_color, fg_color) in enumerate(self.df_activity.values.tolist()):
                tk.Button(
                    content,
                    font=('Ariel', 20),
                    background=bg_color,
                    foreground=fg_color,
                    activebackground=fg_color,
                    activeforeground=bg_color,
                    text=f"{activity}",
                    command=lambda x = [activity, bg_color, fg_color]: generate_summary(x)
                ).grid(row=i, sticky='nsew')
        
        def generate_summary(arg: list):
            """
            Draws a summary for the selected activity
            """
            clear()
            activity, bg_color, fg_color = arg
            #* HEEDER BUTTON
            #| Calls buttons_generator
            top_bar = tk.Frame(content)
            top_bar.pack(fill='x')
            tk.Button(
                top_bar,
                background=TimerApp.FGCOLOR,
                foreground=TimerApp.BGCOLOR,
                activebackground=TimerApp.BGCOLOR,
                activeforeground=TimerApp.FGCOLOR,
                font=('calibri',15),
                text="⭮",
                command=buttons_generator
            ).pack(fill='both', expand=True)
            
            #* TOP
            #| Summary of picked action
            up_data_grid = tk.Frame(content)
            up_data_grid.config(background=TimerApp.BGCOLOR)
            up_data_grid.pack()
            
            style = ttk.Style()
            style.configure(
                "BW.TLabel",
                font=("Ariel",15),
                foreground=TimerApp.FGCOLOR, 
                background=TimerApp.BGCOLOR
            )
            
            #| Title
            tk.Label(
                up_data_grid,
                font=("Ariel",30),
                foreground=TimerApp.FGCOLOR, 
                background=TimerApp.BGCOLOR,
                text=f"{activity}"
            ).grid(column=0, columnspan=3, row=0)
            
            #| Times Performed
            ttk.Label(
                up_data_grid,
                text=f"Performed: {self.df_data[self.df_data['activity'] == activity].shape[0]}",
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
            if not self.df_data.loc[self.df_data['activity'] == activity].shape[0]:
                main_data = [0,0,0]
                break_data = [0,0,0]
            else:
                main_data = [
                    self.df_data.loc[self.df_data['activity'] == activity, 'main_time'].sum(),
                    int(self.df_data.loc[self.df_data['activity'] == activity, 'main_time'].mean()),
                    self.df_data.loc[self.df_data['activity'] == activity, 'main_time'].max()
                ]
                break_data = [
                    self.df_data.loc[self.df_data['activity'] == activity, 'break_time'].sum(),
                    int(self.df_data.loc[self.df_data['activity'] == activity, 'break_time'].mean()),
                    self.df_data.loc[self.df_data['activity'] == activity, 'break_time'].max()
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
                background=TimerApp.FGCOLOR,
                bd=0,
                height=1
            ).pack(fill='x', pady=20)
            
            #* MIDDLE
            
            mid_frame = tk.Frame(content, background=TimerApp.BGCOLOR)
            mid_frame.pack()
            
            def change_color():
                new_bg_color = askcolor(title="Background color", color=bg_color)[1]
                new_fg_color = askcolor(title="Foreground color", color=fg_color)[1]
                
                cursor = self.conn.cursor()
                if new_bg_color:
                    cursor.execute(
                        f'UPDATE activities SET bg = "{new_bg_color}" WHERE name = "{activity}"'
                    )
                if new_fg_color:
                    cursor.execute(
                        f'UPDATE activities SET fg = "{new_fg_color}" WHERE name = "{activity}"'
                    )
                self.conn.commit()
                fetch_dfs_with_range()
                buttons_generator()
            
            def change_name():
                def submit_new_name():
                    cursor = self.conn.cursor()
                    if new_name.get():
                        cursor.execute(
                            f'UPDATE activities SET name = "{new_name.get().upper()}" WHERE name = "{activity}"'
                        )
                    self.conn.commit()
                    fetch_dfs_with_range()
                    buttons_generator()
                change_name_window = tk.Toplevel(mid_frame)
                change_name_window.title('Change name')
                new_name = tk.StringVar()
                new_name.set(activity)
                tk.Entry(
                    change_name_window,
                    font=('Ariel', 15),
                    textvariable=new_name
                ).pack()
                tk.Button(
                    change_name_window,
                    font=('Ariel', 15),
                    text='Change name',
                    command=submit_new_name
                ).pack()
            
            def change_time_range(*args):
                self.time_range = self.range_optionts.index(picked_range.get())
                fetch_dfs_with_range()
                generate_summary(arg)
            
            #| change color
            tk.Button(
                mid_frame,
                font=("Ariel",15),
                foreground=TimerApp.FGCOLOR, 
                background=TimerApp.BGCOLOR,
                activebackground=TimerApp.FGCOLOR,
                activeforeground=TimerApp.BGCOLOR,
                text="Change Color",
                command=change_color
            ).pack(side='left', padx=5)
            
            #| change name
            tk.Button(
                mid_frame,
                font=("Ariel",15),
                foreground=TimerApp.FGCOLOR, 
                background=TimerApp.BGCOLOR,
                activebackground=TimerApp.FGCOLOR,
                activeforeground=TimerApp.BGCOLOR,
                text="Change Name",
                command=change_name
            ).pack(side='left', padx=5, fill='y')
            
            #| change time range
            picked_range = tk.StringVar(value=self.range_optionts[self.time_range])
            picked_range.trace('w', change_time_range)
            range_menu = tk.OptionMenu(
                mid_frame,
                picked_range,
                *self.range_optionts
            )
            range_menu.config(
                font=("Ariel",15),
                background=TimerApp.BGCOLOR,
                foreground=TimerApp.FGCOLOR,
                activebackground=TimerApp.BGCOLOR,
                activeforeground=TimerApp.FGCOLOR,
                highlightbackground=TimerApp.BGCOLOR,
                highlightcolor=TimerApp.BGCOLOR
            )
            range_menu['menu'].config(
                font=("Ariel",10),
                background=TimerApp.BGCOLOR,
                foreground=TimerApp.FGCOLOR
            )
            range_menu.pack(side='left', padx=5)
            
            tk.Frame( #| Separator
                content,
                background=TimerApp.FGCOLOR,
                bd=0,
                height=1
            ).pack(fill='x', pady=20)
            
            #* BOTTOM
            #| Draws data in scrollable canvas
            outer_frame = tk.Frame(content)
            outer_frame.pack(padx=10, pady=10, fill='both', expand=True)

            canvas = tk.Canvas(outer_frame, background=bg_color, highlightthickness=1, highlightbackground=bg_color)
            inner_frame = tk.Frame(canvas, background=bg_color)
            inner_frame.columnconfigure(1, weight=1)
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
            
            #| Generates labels with data
            max_value = self.df_data[self.df_data['activity'] == activity]['main_time'].max()
            for i, row in enumerate(self.df_data[self.df_data['activity'] == activity].values.tolist()):
                tk.Button(
                    inner_frame,
                    font=('Consolas', 15),
                    text=f"{row[0]} | {row[1].rjust(8)}",
                    background=fg_color,
                    foreground=bg_color,
                    command=lambda x = [row, [activity, bg_color, fg_color]]: self.open_info_Toplevel(x)
                ).grid(column=0, row=i, sticky='w', padx=10, pady=5)
                tk.Frame( # max width 1617
                    inner_frame,
                    height=30,
                    width=int(row[2] / max_value * 1617),
                    background=fg_color
                ).grid(column=1, row=i, sticky='w', padx=(0,10))
        
        def fetch_dfs_with_range():
            self.fetch_dfs()
            if self.time_range:
                offset = [0, 7, 30, 90, 365]
                self.df_data['date'] = pd.to_datetime(self.df_data['date'])
                date_off_set = datetime.now() - timedelta(days=offset[self.time_range])
                self.df_data = self.df_data.loc[self.df_data['date'] >= date_off_set]
                self.df_data['date'] = self.df_data['date'].dt.date
            # print(self.df_data)
                
        self.clear_window()
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        
        self.range_optionts = ["Total", "Last 7 days", "Last 30 days", "Last 90 days", "Last Year"]
        self.time_range = 0
        fetch_dfs_with_range()
        
        content = tk.Frame(self.window, background=TimerApp.BGCOLOR)
        content.columnconfigure(0, weight=1)
        for i in range(self.df_activity.shape[0]): 
            content.rowconfigure(i, weight=1, uniform='group1')
        content.pack(fill='both', expand=True)
        
        buttons_generator()
    
    def open_info_Toplevel(self, arg: list[list, list]): 
        """
        Opens new window with picked action data
        arg: [data.date, data.start_time, data.main_time, data.break_time, data.desc, activities.name] [activities.name, activities.bg, activities.fg]
        """
        action, activity = arg
        action_window = tk.Toplevel(self.root)
        action_window.resizable(False, False)
        action_window.attributes('-topmost', 'true')
        action_window.title(action[5])
        action_window.geometry(self.window_shift)
        action_window.config(bg=activity[1])
        
        font = tkFont.Font(family='Ariel', size=40)
        text_width = font.measure(action[5])
        text_height = font.metrics('linespace')
        
        container = tk.Frame(action_window, background=activity[1])
        container.pack(fill='both', expand=True, padx=(5, text_height), pady=(5,0))
        
        canvas = tk.Canvas(container, width=text_height, height=text_width, bg=activity[1], highlightthickness=1, highlightbackground=activity[1])
        canvas.grid(row=0, column=0, sticky='nsew')

        # Makes name rotated 90 degrees
        text = canvas.create_text(text_height/2, text_width/2, anchor="center", angle=90, text=action[5], fill=activity[2], font=font)
        
        right_container = tk.Frame(container, background=TimerApp.BGCOLOR)
        right_container.grid(column=1, row=0, sticky='nsew')
        tk.Label(
            right_container,
            font=('Ariel', 20),
            background=activity[1],
            foreground=activity[2],
            text=
            f"{action[0]} {action[1]}"
        ).pack(fill='x')
        
        tk.Label(
            right_container,
            background=TimerApp.BGCOLOR,
            foreground=TimerApp.FGCOLOR,
            font=('Ariel', 40),
            text=
            f"{action[2] // 3600}:{(action[2] % 3600) // 60 :02d}:{(action[2] % 3600) % 60 :02d}"
        ).pack()
        
        tk.Label(
            right_container,
            background=TimerApp.BGCOLOR,
            foreground=TimerApp.FGCOLOR,
            font=('Ariel', 15),
            wraplength=400,
            text=
            f"{action[3] // 3600}:{(action[3] % 3600) // 60 :02d}:{(action[3] % 3600) % 60 :02d}\n"
            f"{action[4]}"
        ).pack()
        
        def change_desc():
            pass
        
        def change_activity():
            pass
        
        def delete():
            pass
        
        def google_calendar():
            pass
        
        button_frame = tk.Frame(right_container)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.pack(side='bottom', fill='x')
        
        tk.Button(
            button_frame,
            font=('Ariel', 10),
            background=activity[1],
            foreground=activity[2],
            activebackground=activity[2],
            activeforeground=activity[1],
            text='Change Desc',
            command=change_desc
        ).grid(column=0, row=0, sticky='nwes')
        
        tk.Button(
            button_frame,
            font=('Ariel', 10),
            background=activity[1],
            foreground=activity[2],
            activebackground=activity[2],
            activeforeground=activity[1],
            text='Change Activity',
            command=change_activity
        ).grid(column=1, row=0, sticky='nwes')
    
        tk.Button(
            button_frame,
            font=('Ariel', 10),
            background=activity[1],
            foreground=activity[2],
            activebackground=activity[2],
            activeforeground=activity[1],
            text='Delete',
            command=delete
        ).grid(column=0, row=1, sticky='nwes')
        
        tk.Button(
            button_frame,
            font=('Ariel', 10),
            background=activity[1],
            foreground=activity[2],
            activebackground=activity[2],
            activeforeground=activity[1],
            text='Google calendar',
            command=google_calendar
        ).grid(column=1, row=1, sticky='nwes')
    
    def open_main_window(self):
        """
        MENU
        """
        self.clear_window()
        self.root.geometry('446x548'+self.window_shift)
        self.window.config(bg=TimerApp.BGCOLOR)
        
        button_to_timer = tk.Button(
            self.window,
            text="Timer",
            fg=TimerApp.BGCOLOR, 
            bg=TimerApp.FGCOLOR,
            activebackground=TimerApp.EFFECTSCOLOR,
            activeforeground=TimerApp.FGCOLOR,
            pady= 12,
            padx= 50,
            font=("Ariel", 40 , 'bold'),
            command=self.open_timer_window
        )
        button_to_timer.pack(fill='x', padx=30, pady=20)
        
        button_to_calendar = tk.Button(
            self.window,
            text='Calendar',
            fg=TimerApp.BGCOLOR, 
            bg=TimerApp.FGCOLOR,
            activebackground=TimerApp.EFFECTSCOLOR,
            activeforeground=TimerApp.FGCOLOR,
            pady= 12,
            padx= 50,
            font=("Ariel", 40 , 'bold'),
            command=self.open_calendar_window
        )
        button_to_calendar.pack(fill='x', padx=30, pady=20)
        
        button_to_summary = tk.Button(
            self.window,
            text='Summary',
            fg=TimerApp.BGCOLOR, 
            bg=TimerApp.FGCOLOR,
            activebackground=TimerApp.EFFECTSCOLOR,
            activeforeground=TimerApp.FGCOLOR,
            pady= 12,
            padx= 50,
            font=("Ariel", 40 , 'bold'),
            command=self.open_summary_window
        )
        button_to_summary.pack(fill='x', padx=30, pady=20)

if __name__=="__main__":
    t = TimerApp()
    t.conn.close()