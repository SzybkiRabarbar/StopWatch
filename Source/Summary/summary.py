import tkinter as tk
from pandas import to_datetime, read_sql_query
from datetime import datetime, timedelta
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter import messagebox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stop_watch import StopWatch

class CreateSummary:
    """
    Creates list of buttons, each button representing diffrent activity from DB.\n
    Each button creates:
        - button that returns to previous list
        - summary of picked activity [sum, mean, max]
        - buttons that modify picked activity & combobox with time range selection
        - list of action from that activity from selected time period
    """
    def __init__(self, App: 'StopWatch') -> None:
        self.App = App
        self.main()
        
    def main(self):
        self.App.clear_window()
        self.App.was_fullscreen = True
        self.App.root.geometry(
            f"{self.App.root.winfo_screenwidth()}x{self.App.root.winfo_screenheight()}+0+0"
        )
        
        self.geometry_icon = tk.StringVar(value='🗗')
        self.range_optionts = ["Total", "Last 7 days", "Last 30 days", "Last 90 days", "Last Year"]
        self.time_range = 0
        self.fetch_dfs_with_range()
        
        self.up_button = tk.Frame(self.App.window, background=self.App.BGCOLOR)
        self.up_button.pack(fill='x')
        
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
            
        for widget in self.up_button.winfo_children(): 
            widget.destroy()
    
    def create_buttons(self):
        """
        Draws buttons, each button corresponds to diffrent activity.\n
        Button click calls create_summary with corresponding activity
        """
        self.clear()
        
        tk.Button(
            self.up_button,
            background = self.App.MIDCOLOR,
            foreground = self.App.FGCOLOR,
            activebackground = self.App.BGCOLOR,
            activeforeground = self.App.FGCOLOR,
            font = ('times new roman', 15),
            textvariable = self.geometry_icon,
            command = self.change_geometry
        ).pack(fill='both', expand=True)
        
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
    
    def change_geometry(self):
        if self.geometry_icon.get() == '🗗':
            self.geometry_icon.set('🗖')
            self.App.was_fullscreen = False
            self.App.root.geometry(
                f"{self.App.root.winfo_screenwidth() - 300}x{self.App.root.winfo_screenheight() - 300}+150+150"
            )
        else:
            self.geometry_icon.set('🗗')
            self.App.was_fullscreen = True
            self.App.root.geometry(
                f"{self.App.root.winfo_screenwidth()}x{self.App.root.winfo_screenheight()}+0+0"
            )
    
    def create_summary(self, arg: list[str]):
        """
        Creates:
        - button that returns to previous list (call create_buttons)
        - summary of picked activity [sum, mean, max]
        - buttons that modify picked activity and combobox with time range selection
        - list of action from that activity from selected time period (button and bar informing about the time spent)
        """
        self.clear()
        self.activity, self.bg_color, self.fg_color, self.id = arg
        
        #* HEEDER BUTTON
        #| Button that returns to previous list (call create_buttons)
        # top_bar = tk.Frame(self.content)
        # top_bar.pack(fill='x')
        tk.Button(
            self.up_button,
            background = self.App.MIDCOLOR,
            foreground = self.App.FGCOLOR,
            activebackground = self.App.BGCOLOR,
            activeforeground = self.App.FGCOLOR,
            font = ('times new roman',15),
            text = "⭮",
            command = self.create_buttons
        ).pack(fill='both', expand=True)

        #* SUMMARY GRID
        #| Summary of picked activity [sum, mean, max]
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
        #| Buttons that modify picked activity and combobox with time range selection
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
        #| List of action from that activity from selected time period (button and bar informing about the time spent)
        outer_frame = tk.Frame(self.content)
        outer_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.summary_canvas = tk.Canvas(outer_frame, background=self.bg_color, highlightthickness=1, highlightbackground=self.bg_color)
        self.inner_frame = tk.Frame(self.summary_canvas, background=self.bg_color)
        self.inner_frame.columnconfigure(1, weight=1)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=self.summary_canvas.yview)

        self.summary_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.summary_canvas.pack(side="left", fill="both", expand=True)
        canvas_frame = self.summary_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        def onFrameConfigure(event):
            self.summary_canvas.configure(scrollregion=self.summary_canvas.bbox("all"))
        self.inner_frame.bind("<Configure>", onFrameConfigure)
        
        def onCanvasConfigure(event):
            self.summary_canvas.itemconfigure(canvas_frame, width=event.width)
        self.summary_canvas.bind("<Configure>", onCanvasConfigure)
        
        max_value = self.App.df_data[self.App.df_data['activity'] == self.activity]['main_time'].max()
        available_width = 0
        for i, row in enumerate(self.App.df_data[self.App.df_data['activity'] == self.activity].values.tolist()):
            #| Button opens window with chosen event
            event_button = tk.Button(
                self.inner_frame,
                font = ('Consolas', 15),
                text = f"{row[0]} | {row[1].rjust(8)}",
                background = self.fg_color,
                foreground = self.bg_color,
                command = lambda x = [row, [self.activity, self.bg_color, self.fg_color, self.id]]: self.App.open_event(x)
            )
            event_button.grid(column=0, row=i, sticky='w', padx=10, pady=5)

            if not available_width:
                available_width = self.return_available_width(event_button)
            
            #| Frame acts as a bar informing about the time spent
            tk.Frame(
                self.inner_frame,
                height=30,
                width=int(row[2] / max_value * available_width),
                background=self.fg_color
            ).grid(column=1, row=i, sticky='w', padx=(0,10))
    
    def return_available_width(self, button: tk.Button):
        """
        Returns available width value.\n
        summary_canvas.width - event_button.width - sum of all horizontal padding (in summary_canvas)
        """
        self.App.root.update_idletasks()
        return self.summary_canvas.winfo_width() - button.winfo_width() - 20
    
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
        self.App.confirm_execution()
        self.create_buttons()
    
    def change_name(self): 
        """
        Change name of picked activity.\n
        Opens window with text entry for new name and button to save new name
        """        
        change_name_window = tk.Toplevel(self.mid_frame)
        change_name_window.grab_set()
        change_name_window.title('Change name')
        change_name_window.iconbitmap(self.App.static_path / 'icon.ico')
        change_name_window.config(background=self.App.BGCOLOR)
        change_name_window.geometry(self.App.default_window_shift)
        self.new_name = tk.StringVar()
        self.new_name.set(self.activity)
        tk.Entry(
            change_name_window,
            font = ('Ariel', 15),
            textvariable = self.new_name
        ).pack(padx=10)
        tk.Button(
            change_name_window,
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            font = ('Ariel', 15),
            text = 'Change name',
            command = self.submit_new_name
        ).pack(padx=10, fill='x', expand=True)
    
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
            self.App.confirm_execution()
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
            self.App.confirm_execution()
            self.App.open_menu()
        
        def delete_data():
            """Deletes activity and all actions with this activity"""
            id_number = read_sql_query(f'SELECT id FROM activities WHERE name = "{self.activity}"', self.App.conn).iloc[0, 0]
            curr = self.App.conn.cursor()
            curr.execute(f'DELETE FROM data WHERE activity = "{id_number}"')
            curr.execute(f'DELETE FROM activities WHERE id = "{id_number}"')
            self.App.conn.commit()
            pick_new_activity.destroy()
            self.App.confirm_execution()
            self.App.open_menu()
        
        is_sure = messagebox.askyesno(
            f"Delete {self.activity}?",
            f"Are you sure you want to delete the activity named '{self.activity}'?",
            parent=self.App.root
        )
        if is_sure:
            pick_new_activity = tk.Toplevel(self.App.root)
            pick_new_activity.resizable(False, False)
            pick_new_activity.grab_set()
            pick_new_activity.title(self.activity)
            pick_new_activity.iconbitmap(self.App.static_path / 'icon.ico')
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
                values = self.App.df_activity[self.App.df_activity['name'] != self.activity]['name'].to_list(),
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