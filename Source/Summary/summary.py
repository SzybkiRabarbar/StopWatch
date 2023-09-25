import tkinter as tk
from pandas import to_datetime, read_sql_query
from datetime import datetime, timedelta
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter import messagebox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from timer_app import TimerApp

class CreateSummary:
    """
    Creates list of buttons, each button representing diffrent activity from DB.\n
    Each button creates:
        - button that returns to previous list
        - summary of picked activity [sum, mean, max]
        - buttons that modify picked activity & combobox with time range selection
        - list of action from that activity from selected time period
    """
    def __init__(self, App: 'TimerApp') -> None:
        self.App = App
        self.main()
        
    def main(self):
        self.App.clear_window()
        self.App.was_fullscreen = True
        self.App.root.geometry(f"{self.App.root.winfo_screenwidth()}x{self.App.root.winfo_screenheight()}+0+0")
        
        self.range_optionts = ["Total", "Last 7 days", "Last 30 days", "Last 90 days", "Last Year"]
        self.time_range = 0
        self.fetch_dfs_with_range()
        
        self.content = tk.Frame(self.App.window, background=self.App.BGCOLOR)
        self.content.columnconfigure(0, weight=1)
        for i in range(self.App.df_activity.shape[0]): 
            self.content.rowconfigure(i, weight=1, uniform='group1')
        self.content.pack(fill='both', expand=True)
        
        self.create_buttons()
    
    def fetch_dfs_with_range(self):
        """Apllies time range to df from self.App.fetch_dfs()"""
        self.App.fetch_dfs()
        if self.time_range:
            offset = [0, 7, 30, 90, 365]
            self.App.df_data['date'] = to_datetime(self.App.df_data['date'])
            date_offset = datetime.now() - timedelta(days=offset[self.time_range])
            self.App.df_data = self.App.df_data.loc[self.App.df_data['date'] >= date_offset]
            self.App.df_data['date'] = self.App.df_data['date'].dt.date
    
    def clear(self):
        """Destroy all widgets from content(Frame)"""
        for widget in self.content.winfo_children(): 
            widget.destroy()
    
    def create_buttons(self):
        """
        Draws buttons, each button corresponds to diffrent activity.\n
        Button click calls create_summary with corresponding activity
        """
        self.clear()
        for i, (activity, bg_color, fg_color, id) in enumerate(self.App.df_activity.values.tolist()):
            tk.Button(
                self.content,
                font = (self.App.FONTF, 20),
                background = bg_color,
                foreground = fg_color,
                activebackground = fg_color,
                activeforeground = bg_color,
                text = activity,
                command=lambda x = [activity, bg_color, fg_color, id]: self.create_summary(x)
            ).grid(row=i, sticky='nsew')
    
    def create_summary(self, arg: list[str]):
        """
        Creates:
        - button that returns to previous list
        - summary of picked activity [sum, mean, max]
        - buttons that modify picked activity & combobox with time range selection
        - list of action from that activity from selected time period
        """
        self.clear()
        self.activity, self.bg_color, self.fg_color, self.id = arg
        
        #* HEEDER BUTTON
        #| Calls buttons_generator
        
        top_bar = tk.Frame(self.content)
        top_bar.pack(fill='x')
        tk.Button(
            top_bar,
            background = self.App.MIDCOLOR,
            foreground = self.App.FGCOLOR,
            activebackground = self.App.BGCOLOR,
            activeforeground = self.App.FGCOLOR,
            font = ('calibri',15),
            text = "⭮",
            command = self.create_buttons
        ).pack(fill='both', expand=True)

        #* Summary of picked action
        
        up_data_grid = tk.Frame(self.content)
        up_data_grid.config(background=self.App.BGCOLOR)
        up_data_grid.pack()
        
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            font = (self.App.FONTF, 15),
            foreground = self.App.FGCOLOR, 
            background = self.App.BGCOLOR
        )
        
        #| Title
        tk.Label(
            up_data_grid,
            font = (self.App.FONTF,30),
            foreground = self.App.FGCOLOR, 
            background = self.App.BGCOLOR,
            text = self.activity
        ).grid(column=0, columnspan=3, row=0)
        
        #| Times Performed Counter
        ttk.Label(
            up_data_grid,
            text = f"Performed: {self.App.df_data[self.App.df_data['activity'] == self.activity].shape[0]}",
            style = "BW.TLabel"
        ).grid(column=0, columnspan=3, row=1)
        
        #| Column names
        columns_names = ['Time', 'Activity', 'Break']
        for i, name in enumerate(columns_names):
            ttk.Label(
                up_data_grid,
                text = name,
                style = "BW.TLabel"
            ).grid(column=i, row=2, sticky='w', padx=30)
        
        #| Columns content
        description_data = ['Sum', 'Mean', 'Max']
        if not self.App.df_data.loc[self.App.df_data['activity'] == self.activity].shape[0]:
            main_data = [0,0,0]
            break_data = [0,0,0]
        else:
            main_data = [
                self.App.df_data.loc[self.App.df_data['activity'] == self.activity, 'main_time'].sum(),
                int(self.App.df_data.loc[self.App.df_data['activity'] == self.activity, 'main_time'].mean()),
                self.App.df_data.loc[self.App.df_data['activity'] == self.activity, 'main_time'].max()
            ]
            break_data = [
                self.App.df_data.loc[self.App.df_data['activity'] == self.activity, 'break_time'].sum(),
                int(self.App.df_data.loc[self.App.df_data['activity'] == self.activity, 'break_time'].mean()),
                self.App.df_data.loc[self.App.df_data['activity'] == self.activity, 'break_time'].max()
            ]

        for c_id, d in enumerate([description_data, main_data, break_data]):
            for i, value in enumerate(d):
                txt = f"{value // 3600}:{value // 60 % 60 :02d}:{value % 60 :02d}" if c_id else f"{value}"
                ttk.Label(
                    up_data_grid,
                    text = txt,
                    style = "BW.TLabel"
                ).grid(column=c_id, row=3+i, sticky='w', padx=30)
        
        tk.Frame( #| Separator
            self.content,
            background = self.App.FGCOLOR,
            bd = 0,
            height = 1
        ).pack(fill='x', pady=20)
        
        #* MIDDLE BUTTONS
        
        self.mid_frame = tk.Frame(self.content, background=self.App.BGCOLOR)
        self.mid_frame.pack()
        
        #| change color
        tk.Button(
            self.mid_frame,
            font = (self.App.FONTF, 15),
            width = 13,
            foreground = self.App.FGCOLOR, 
            background = self.App.BGCOLOR,
            activebackground = self.App.FGCOLOR,
            activeforeground = self.App.BGCOLOR,
            text = "Change Color",
            command = self.change_color
        ).pack(side='left', padx=5, fill='y')
        
        #| change name
        tk.Button(
            self.mid_frame,
            font = (self.App.FONTF, 15),
            width = 13,
            foreground = self.App.FGCOLOR, 
            background = self.App.BGCOLOR,
            activebackground = self.App.FGCOLOR,
            activeforeground = self.App.BGCOLOR,
            text = "Change Name",
            command = self.change_name
        ).pack(side='left', padx=5, fill='y')
        
        #| delete activity
        tk.Button(
            self.mid_frame,
            font = (self.App.FONTF, 15),
            width = 13,
            foreground = self.App.FGCOLOR, 
            background = self.App.BGCOLOR,
            activebackground = self.App.FGCOLOR,
            activeforeground = self.App.BGCOLOR,
            text = "Delete",
            command = self.delete_activity
        ).pack(side='left', padx=5, fill='y')
        
        #| change time range
        def change_time_range(*args):
            self.time_range = self.range_optionts.index(picked_range.get())
            self.fetch_dfs_with_range()
            self.create_summary(arg)
        
        picked_range = tk.StringVar(value=self.range_optionts[self.time_range])
        picked_range.trace('w', change_time_range)
        range_menu = ttk.Combobox(
            self.mid_frame,
            textvariable = picked_range,
            values = self.range_optionts,
            state = 'readonly',
            font = (self.App.FONTF, 15),
            width = 13,
            background = self.App.BGCOLOR,
            foreground = 'black'
        )
        range_menu.pack(side='left', padx=5, fill='y')
        
        tk.Frame( #| Separator
            self.content,
            background=self.App.FGCOLOR,
            bd=0,
            height=1
        ).pack(fill='x', pady=20)
        
        #* BOTTOM
        #| Draws data in scrollable canvas
        outer_frame = tk.Frame(self.content)
        outer_frame.pack(padx=10, pady=10, fill='both', expand=True)

        summary_canvas = tk.Canvas(outer_frame, background=self.bg_color, highlightthickness=1, highlightbackground=self.bg_color)
        inner_frame = tk.Frame(summary_canvas, background=self.bg_color)
        inner_frame.columnconfigure(1, weight=1)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=summary_canvas.yview)

        summary_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        summary_canvas.pack(side="left", fill="both", expand=True)
        canvas_frame = summary_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def onFrameConfigure(event):
            summary_canvas.configure(scrollregion=summary_canvas.bbox("all"))
        inner_frame.bind("<Configure>", onFrameConfigure)
        
        def onCanvasConfigure(event):
            summary_canvas.itemconfigure(canvas_frame, width=event.width)
        summary_canvas.bind("<Configure>", onCanvasConfigure)
        
        #| Generates labels with data
        max_value = self.App.df_data[self.App.df_data['activity'] == self.activity]['main_time'].max()
        for i, row in enumerate(self.App.df_data[self.App.df_data['activity'] == self.activity].values.tolist()):
            #| Button opens window with chosen event
            tk.Button(
                inner_frame,
                font = ('Consolas', 15),
                text = f"{row[0]} | {row[1].rjust(8)}",
                background = self.fg_color,
                foreground = self.bg_color,
                command = lambda x = [row, [self.activity, self.bg_color, self.fg_color, self.id]]: self.App.open_event(x)
            ).grid(column=0, row=i, sticky='w', padx=10, pady=5)
            #| Empty frame imitates 
            tk.Frame(
                inner_frame,
                height=30,
                width=int(row[2] / max_value * 1617),
                background=self.fg_color
            ).grid(column=1, row=i, sticky='w', padx=(0,10))
    
    def change_color(self):
        """
        Change color of picked activity.\n
        Opens 2 tk.askcolor windows, one for background color, 
        second for foreground color.
        """
        new_bg_color = askcolor(title="Background color", color=self.bg_color)[1]
        new_fg_color = askcolor(title="Foreground color", color=self.fg_color)[1]
        
        cursor = self.App.conn.cursor()
        if new_bg_color:
            cursor.execute(
                f'UPDATE activities SET bg = "{new_bg_color}" WHERE name = "{self.activity}"'
            )
        if new_fg_color:
            cursor.execute(
                f'UPDATE activities SET fg = "{new_fg_color}" WHERE name = "{self.activity}"'
            )
        self.App.conn.commit()
        self.fetch_dfs_with_range()
        self.create_buttons()
    
    def change_name(self):
        """
        Change name of picked activity.\n
        Opens window with text entry for new name and button to save new name
        """        
        change_name_window = tk.Toplevel(self.mid_frame)
        change_name_window.title('Change name')
        self.new_name = tk.StringVar()
        self.new_name.set(self.activity)
        tk.Entry(
            change_name_window,
            font=('Ariel', 15),
            textvariable=self.new_name
        ).pack()
        tk.Button(
            change_name_window,
            font=('Ariel', 15),
            text='Change name',
            command=self.submit_new_name
        ).pack()
    
    def submit_new_name(self):
        """Modify name of picked activity"""
        
        def is_activity_in_DB(new_activity: str) -> bool:
            return read_sql_query(f'SELECT name FROM activities WHERE name="{new_activity}"', self.App.conn).shape[0]
        
        cursor = self.App.conn.cursor()
        new_activity = self.new_name.get().upper()
        if is_activity_in_DB(new_activity):
            messagebox.showerror(
                f"{new_activity} already exists",
                f"{new_activity} already exists, try new name.\nIf you want to merge activities try deleting one of them."
            )
        elif new_activity:
            cursor.execute(
                f'UPDATE activities SET name = "{new_activity}" WHERE name = "{self.activity}"'
            )
            self.App.conn.commit()
        self.fetch_dfs_with_range()
        self.create_buttons()
    
    def delete_activity(self):
        """
        Deletes picked activity.\n
        Opens messagebox with yes/no question to confirm removal.\n
        Opens a window with the choice of whether to delete all data or move it to another activity.
        """
        def change_activity_in_data(*args):
            """
            Changes the activity for all actions from deleted to newly selected then
            deletes activity
            """
            update_id = read_sql_query(f'SELECT id FROM activities WHERE name = "{picked_activity.get()}"', self.App.conn).iloc[0, 0]
            del_id = read_sql_query(f'SELECT id FROM activities WHERE name = "{self.activity}"', self.App.conn).iloc[0, 0]
            curr = self.App.conn.cursor()
            curr.execute(f'UPDATE data SET activity = "{update_id}" WHERE activity = "{del_id}"')
            curr.execute(f'DELETE FROM activities WHERE id = "{del_id}"')
            self.App.conn.commit()
            pick_new_activity.destroy()
            self.App.open_menu()
        
        def delete_data():
            """Deletes activity and all actions with this activity"""
            id_number = read_sql_query(f'SELECT id FROM activities WHERE name = "{self.activity}"', self.App.conn).iloc[0, 0]
            curr = self.App.conn.cursor()
            curr.execute(f'DELETE FROM data WHERE activity = "{id_number}"')
            curr.execute(f'DELETE FROM activities WHERE id = "{id_number}"')
            self.App.conn.commit()
            pick_new_activity.destroy()
            self.App.open_menu()
        
        is_sure = messagebox.askyesno(
            f"Delete {self.activity}?",
            f"Are you sure you want to delete the activity named '{self.activity}'?",
            parent=self.App.root
        )
        if is_sure:
            pick_new_activity = tk.Toplevel(self.App.root)
            pick_new_activity.resizable(False, False)
            pick_new_activity.attributes('-topmost', 'true')
            pick_new_activity.title(self.activity)
            pick_new_activity.geometry(self.App.default_window_shift)
            pick_new_activity.config(background=self.App.MIDCOLOR)
            
            tk.Label(
                pick_new_activity,
                font = (self.App, 15),
                background = self.App.MIDCOLOR,
                foreground = self.App.FGCOLOR,
                text = f"Do you want to transfer data from\n'{self.activity}' activity to another activity?"
            ).pack()
            
            picked_activity = tk.StringVar()
            picked_activity.trace('w', change_activity_in_data)
            ttk.Combobox(
                pick_new_activity,
                textvariable = picked_activity,
                values = self.App.df_activity['name'].to_list(),
                state = 'readonly',
                font = (self.App.FONTF, 15),
                background = self.App.MIDCOLOR,
                foreground = 'black'
            ).pack(fill='x', expand=True)
            
            tk.Button(
                pick_new_activity,
                font = (self.App.FONTF, 15),
                text = 'No, delete all data',
                command = delete_data
            ).pack()