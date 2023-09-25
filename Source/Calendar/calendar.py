from datetime import datetime
import tkcalendar as tkc
import tkinter as tk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from timer_app import TimerApp

class CreateCalendar:
    """
    Creates calendar and daily activity list.\n
    Daily activity list depends on date selected in the calendar.
    """    
    def __init__(self, App: 'TimerApp') -> None:
        self.App = App
        self.main()
        
    def main(self):
        self.App.clear_window()
        self.App.root.geometry("400x700")
        self.picked_date = ''
        
        today = datetime.now()
        y, m, d = today.year, today.month, today.day

        #| Calendar
        self.cal = tkc.Calendar(self.App.window, selectmode='day', year=y, month=m, day=d, date_pattern='y-mm-dd')
        
        self.App.fetch_dfs()
        
        #| Adds event to calendar
        for action in self.App.df_data.values.tolist():
            date = datetime.strptime(action[0], '%Y-%m-%d')
            self.cal.calevent_create(date, action[5], action[5])
        
        self.activites = self.App.df_activity.values.tolist()
        
        for activity in self.activites:
            self.cal.tag_config(activity[0], background=activity[1], foreground=activity[2])
        self.cal.pack(pady=(20,5))
        
        #| Calendar List
        self.content_title = tk.Label(
            self.App.window,
            font = (self.App.FONTF, 15),
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            text = ""
        )
        self.content_title.pack(pady=(0,5))
        
        #| Stores canvas
        canvas_container = tk.Frame(self.App.window)
        canvas_container.pack(fill='both', expand=True)
        
        #| Canvas contains scrollable content
        self.calendar_canvas = tk.Canvas(canvas_container)
        self.content = tk.Frame(self.calendar_canvas, background=self.App.MIDCOLOR)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=self.calendar_canvas.yview)
        self.calendar_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.calendar_canvas.pack(side="left", fill="both", expand=True)
        canvas_frame = self.calendar_canvas.create_window((0, 0), window=self.content, anchor="nw")
        
        #| Links scroll with content
        def on_frame_configure(event):
            self.calendar_canvas.configure(scrollregion=self.calendar_canvas.bbox("all"))
        self.content.bind("<Configure>", on_frame_configure)
        
        #| Changes width of canvas
        def frame_width(event):
            canvas_width = event.width
            self.calendar_canvas.itemconfig(canvas_frame, width = canvas_width)
        self.calendar_canvas.bind('<Configure>', frame_width)
        
        #| Enables mousewheel
        def on_mousewheel(event):
            self.calendar_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.calendar_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.App.window.update_idletasks()
        
        #* LOOP
        self.grab_date_loop()
        
    def grab_date_loop(self):
        """
        Loop\n
        Grabs date from calendar, call print_data func
        """
        if self.picked_date != self.cal.get_date():
            self.picked_date = self.cal.get_date()
            self.content_title.config(text=self.cal.get_date())
            self.print_data()
        self.loop_id = self.App.window.after(100, self.grab_date_loop)
            
    def print_data(self):
        """
        Prints grid with timestaps and actions from picked date 
        """        
        actions = self.App.df_data[self.App.df_data['date'] == self.picked_date] 
        #| Deletes data from previos picked day
        for widget in self.content.winfo_children(): 
            widget.destroy()
        
        #| Sets a minimum height for each row
        for i in range(96):
            self.content.grid_rowconfigure(i, minsize=20)

        #| Sets the minimum width for the first column and the width of the second column to all available space
        self.content.grid_columnconfigure(0, minsize=50)
        self.content.grid_columnconfigure(1, weight=1)

        #| Adds hours and black line above in first column
        t = 0
        for i in range(96):
            if i % 4 == 3:
                frame = tk.Frame(self.content, highlightbackground="black", highlightthickness=1, width=50, height=1)
                frame.grid(row=i, column=0, sticky='s')
            elif not i % 4:
                separator = tk.Label(self.content, text=f"{t}:00", background=self.App.MIDCOLOR, foreground='black')
                separator.grid(row=i, column=0)
                t += 1
                
        #| Adds buttons to seccond column. Each button represent action (the longer the activity, the bigger the button), button trigger on_click()
        for action in actions.values.tolist():
            start_time = [int(x) for x in action[1].split(':')]
            start_time = ((start_time[0] * 60) + start_time[1] + (1 if start_time[2] else 0)) // 15
            
            duration = int(((action[2] + action[3]) / 60) // 15) 
            activity = [activity for activity in self.activites if activity[0] == action[5]][0]
            
            button = tk.Button(
                self.content,
                font = (self.App.FONTF, 1),
                text = '', 
                background = activity[1],
                foreground = activity[2],
                command = lambda x=[action, activity]: self.App.open_event(x)
            )
            
            #| Rowspan value must be positive integer
            if duration: 
                button.configure(font=(self.App.FONTF, 15), text=f"{action[5]}")
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
                self.calendar_canvas.yview_moveto(str(float((start_time // 4) / 24)))
                t += 1