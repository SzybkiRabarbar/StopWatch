import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.colorchooser import askcolor
from pandas import DataFrame
from tkinter import messagebox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from timer_app import TimerApp

class OpenEventToplevel:
    """
    Opens new window with picked action data.\n
    Takes as args: [
        data.date, data.start_time, data.main_time, data.break_time, data.desc, activities.name] [activities.name, activities.bg, activities.fg
    ]\n
    Show information about action and buttons to modify that data
    """
    def __init__(self, App: 'TimerApp', arg: list[list, list]) -> None:
        self.App = App
        self.main(arg)
    
    def main(self, arg: list[list, list]): 
        self.action, self.activity = arg
        self.action_window = tk.Toplevel(self.App.root)
        self.action_window.iconbitmap(self.App.static_path / 'icon.ico')
        self.action_window.resizable(False, False)
        self.action_window.attributes('-topmost', 'true')
        self.action_window.title(self.action[5])
        self.action_window.geometry(self.App.default_window_shift)
        self.action_window.config(bg=self.activity[1])
        
        font = tkFont.Font(family='Ariel', size=40)
        text_width = font.measure(self.action[5])
        text_height = font.metrics('linespace')
        
        container = tk.Frame(self.action_window, background=self.activity[1])
        container.pack(fill='both', expand=True, padx=(5, text_height), pady=(5,0))
        
        canvas = tk.Canvas(container, width=text_height, height=text_width, bg=self.activity[1], highlightthickness=1, highlightbackground=self.activity[1])
        canvas.grid(row=0, column=0, sticky='nsew')

        # Makes name rotated 90 degrees
        text = canvas.create_text(text_height/2, text_width/2, anchor="center", angle=90, text=self.action[5], fill=self.activity[2], font=font)
        
        right_container = tk.Frame(container, background=self.App.BGCOLOR)
        right_container.grid(column=1, row=0, sticky='nsew')
        tk.Label(
            right_container,
            font = ('Ariel', 20),
            background = self.activity[1],
            foreground = self.activity[2],
            text = f"{self.action[0]} {self.action[1]}"
        ).pack(fill='x')
        
        tk.Label(
            right_container,
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            font = (self.App.FONTF, 40),
            text = f"{self.action[2] // 3600}:{(self.action[2] % 3600) // 60 :02d}:{(self.action[2] % 3600) % 60 :02d}"
        ).pack()
        
        tk.Label(
            right_container,
            background = self.App.BGCOLOR,
            foreground = self.App.FGCOLOR,
            font = (self.App.FONTF, 15),
            wraplength = 400,
            text = f"{self.action[3] // 3600}:{(self.action[3] % 3600) // 60 :02d}:{(self.action[3] % 3600) % 60 :02d}\n{self.action[4]}"
        ).pack()
            
        button_frame = tk.Frame(right_container)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.pack(side='bottom', fill='x')
        
        tk.Button(
            button_frame,
            font = ('Ariel', 10),
            background = self.activity[1],
            foreground = self.activity[2],
            activebackground = self.activity[2],
            activeforeground = self.activity[1],
            text = 'Change Desc',
            command = self.change_desc
        ).grid(column=0, row=0, sticky='nwes')
        
        tk.Button(
            button_frame,
            font = ('Ariel', 10),
            background = self.activity[1],
            foreground = self.activity[2],
            activebackground = self.activity[2],
            activeforeground = self.activity[1],
            text = 'Change Activity',
            command = self.change_activity
        ).grid(column=1, row=0, sticky='nwes')
    
        tk.Button(
            button_frame,
            font = ('Ariel', 10),
            background = self.activity[1],
            foreground = self.activity[2],
            activebackground = self.activity[2],
            activeforeground = self.activity[1],
            text = 'Delete',
            command = self.delete
        ).grid(column=0, row=1, sticky='nwes')
        
        tk.Button(
            button_frame,
            font = ('Ariel', 10),
            background = self.activity[1],
            foreground = self.activity[2],
            activebackground = self.activity[2],
            activeforeground = self.activity[1],
            text = 'Google calendar',
            command = self.google_calendar
        ).grid(column=1, row=1, sticky='nwes')
    
    def clear(self):
        """Destroy widgets from action_window"""
        for widget in self.action_window.winfo_children(): 
            widget.destroy()        

    def change_desc(self):
        """Creates text box and button witch call save_new_desc"""
        self.clear()
        
        self.new_desc = tk.Text(
            self.action_window,
            bg = "light yellow",
            font = ("Consolas",15),
            height = 10,
            width = 40,
            padx = 5,
            pady = 5
        )
        self.new_desc.pack(padx=10,pady=10)
        self.new_desc.insert('1.0', self.action[4])

        button_frame = tk.Frame(self.action_window, background=self.activity[1])
        button_frame.pack()
        
        tk.Button(
            button_frame,
            font = (self.App.FONTF, 10),
            background = self.activity[1],
            foreground = self.activity[2],
            activebackground = self.activity[2],
            activeforeground = self.activity[1],
            text = 'Save',
            command = self.save_new_desc
        ).pack(side='left')
        
        tk.Button(
            button_frame,
            font = (self.App.FONTF, 10),
            background = self.activity[1],
            foreground = self.activity[2],
            activebackground = self.activity[2],
            activeforeground = self.activity[1],
            text='Cancel',
            command=lambda x = [self.action, self.activity]: [self.action_window.destroy(), self.App.open_event(x)]
        ).pack(side='left')
            
    def save_new_desc(self):
        """
        Gets new description from text box and save it for picked action.\n
        Destroy event window and opens menu.
        """
        input_desc = self.new_desc.get('1.0', 'end-1c')
        if input_desc != self.action[4]:
            cur = self.App.conn.cursor()
            cur.execute(
                f'UPDATE data SET desc = "{input_desc}"'
                f'WHERE date = "{self.action[0]}" AND start_time = "{self.action[1]}"'
            )
            self.App.conn.commit()
        self.action_window.destroy()
        self.App.open_menu()
    
    def change_activity(self):
        """
        Creates combobox with activities and button witch call save_new_activity
        """
        self.clear()
        
        activities_values = self.App.df_activity['name'].tolist()
        self.activities_cbox = ttk.Combobox(
            self.action_window,
            values = activities_values,
            width = 40
        )
        self.activities_cbox.current(self.activity[3] - 1)
        self.activities_cbox.pack(padx=10, pady=10)
        
        tk.Button(
            self.action_window,
            text = 'Save',
            command = self.save_new_activity
        ).pack()
        
    def save_new_activity(self):
        """
        Gets new activity from combobox and save it for picked action.\n
        If new activity isn't in DB.activities appends it.
        (Opens tk.askcolor to pick backgroud and foreground color)\n
        Destroy event window and opens menu.
        """
        picked_activity = self.activities_cbox.get().upper()
        if picked_activity and picked_activity != self.activity[0]:
            if not self.App.df_activity['name'].isin([picked_activity]).any():
                bg_color = askcolor(
                    title=f"Choose backgroud color for {picked_activity}",
                    color='red',
                    parent=self.action_window
                )[1]
                fg_color = askcolor(
                    title=f"Choose text color for {picked_activity}",
                    color='blue',
                    parent=self.action_window
                )[1]
                activity_df = DataFrame({
                    'name': [picked_activity],
                    'bg': [bg_color if bg_color else '#000000'],
                    'fg': [fg_color if fg_color else '#ffffff'],
                    'auto': [0]
                })
                activity_df.to_sql('activities', self.App.conn, if_exists='append', index=False)
            self.App.fetch_dfs()
            new_id = self.App.df_activity.loc[self.App.df_activity['name'] == picked_activity, 'id'].values[0]
            curr = self.App.conn.cursor()
            curr.execute(
                f'UPDATE data SET activity = "{new_id}" '
                f'WHERE date = "{self.action[0]}" AND start_time = "{self.action[1]}"'
                )
            self.App.conn.commit()
        self.action_window.destroy()
        self.App.open_menu()
        
    def delete(self):
        """
        Opens yes/no messagebox.\n
        If yes then:
            - deletes action from DB
            - destroy event window and opens menu.
        """
        if messagebox.askyesno("Delete", f"are you sure you want to delete\n'{self.action[5]}' from {self.action[0]} {self.action[1]}", parent=self.action_window):
            curr = self.App.conn.cursor()
            curr.execute(
                f'DELETE FROM data '
                f'WHERE date = "{self.action[0]}" AND start_time = "{self.action[1]}"'
            )
            self.App.conn.commit()
            self.action_window.destroy()
            self.App.open_menu()
            
    def google_calendar(self):
        """
        Calls append_to_google_calendar, opens messagebox with results
        """
        is_succes, res = self.App.append_to_google_calendar(
            self.action[5], self.action[0], self.action[1], int(self.action[2]) + int(self.action[3]), self.action[4]
        )
        if is_succes:
            messagebox.showinfo(self.action[5], f"{self.action[5]} was succesful added to your calendar", parent=self.action_window)
        else:
            messagebox.showerror(self.action[5], res, parent=self.action_window)