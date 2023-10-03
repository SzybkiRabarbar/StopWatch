import tkinter as tk
from ctypes import windll

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from timer_app import TimerApp

class CreateTitleBar:
    """
    Replaces the default titlebar with custom one.
    Custom titlebar has most of functions of the basic one.
    """
    
    def __init__(self, App: 'TimerApp') -> None:
        self.App = App
        self.custom_title_bar()

    def custom_title_bar(self):
        #@ https://github.com/Terranova-Python/Tkinter-Menu-Bar
        self.App.root.overrideredirect(True) # turns off title bar, geometry
        #root.iconbitmap("your_icon.ico") # to show your own icon 
        self.App.root.minimized = False # only to know if root is minimized
        self.App.root.maximized = False # only to know if root is maximized

        self.App.root.config(bg="#25292e")
        title_bar = tk.Frame(self.App.root, bg=self.App.BARBGC, relief='raised', bd=0,highlightthickness=0)

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
            self.App.root.attributes("-alpha",0) 
            self.App.root.minimized = True       

        def deminimize(event):
            # so you can see the window when is not minimized
            self.App.root.focus() 
            self.App.root.attributes("-alpha",1) 
            if self.App.root.minimized == True:
                self.App.root.minimized = False                              

        # put a close button on the title bar
        self.close_button = tk.Button(title_bar, text='  ✕  ', command=lambda: [self.App.root.destroy()],bg=self.App.BARBGC,padx=2,pady=2,font=("calibri", 13),bd=0,fg=self.App.BARFGC,highlightthickness=0)
        self.return_button = tk.Button(title_bar, text=' ⟲ ', command=self.App.open_menu,bg=self.App.BARBGC,padx=2,pady=2,bd=0,fg=self.App.BARFGC,font=("calibri", 13),highlightthickness=0)
        self.minimize_button = tk.Button(title_bar, text=' — ',command=minimize_me,bg=self.App.BARBGC,padx=2,pady=2,bd=0,fg=self.App.BARFGC,font=("calibri", 13),highlightthickness=0)
        title_bar_title = tk.Label(title_bar, text='TimerApp', bg=self.App.BARBGC,bd=0,fg=self.App.BARFGC,font=("helvetica", 10),highlightthickness=0)

        # pack the widgets
        title_bar.pack(fill='x')
        self.close_button.pack(side='right',ipadx=7,ipady=1)
        self.return_button.pack(side='right',ipadx=7,ipady=1)
        self.minimize_button.pack(side='right',ipadx=7,ipady=1)
        title_bar_title.pack(side='left', padx=10)
        self.App.window.pack(expand = 1, fill = 'both')

        # bind title bar motion to the move window function

        def changex_on_hovering(event):
            self.close_button['bg']='red'
            
        def returnx_to_normalstate(event):
            self.close_button['bg']=self.App.BARBGC
            
        def change_size_on_hovering(event):
            self.return_button['bg']=self.App.EFFECTSCOLOR
            
        def return_size_on_hovering(event):
            self.return_button['bg']=self.App.BARBGC
            
        def changem_size_on_hovering(event):
            self.minimize_button['bg']=self.App.EFFECTSCOLOR
            
        def returnm_size_on_hovering(event):
            self.minimize_button['bg']=self.App.BARBGC
            
        def get_pos(event): # this is executed when the title bar is clicked to move the window
            if self.App.root.maximized == False:
        
                xwin = self.App.root.winfo_x()
                ywin = self.App.root.winfo_y()
                startx = event.x_root
                starty = event.y_root

                ywin = ywin - starty
                xwin = xwin - startx
        
                def move_window(event): # runs when window is dragged
                    self.App.root.config(cursor="fleur")
                    self.App.root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

                def release_window(event): # runs when window is released
                    self.App.root.config(cursor="arrow")
                                
                title_bar.bind('<B1-Motion>', move_window)
                title_bar.bind('<ButtonRelease-1>', release_window)
                title_bar_title.bind('<B1-Motion>', move_window)
                title_bar_title.bind('<ButtonRelease-1>', release_window)
            else:
                self.return_button.config(text=" 🗖 ")
                self.App.root.maximized = not self.App.root.maximized

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
        resizex_widget = tk.Frame(self.App.window,bg=self.App.BGCOLOR,cursor='sb_h_double_arrow')
        resizex_widget.pack(side='right',ipadx=2,fill='y')

        def resizex(event):
            xwin = self.App.root.winfo_x()
            difference = (event.x_root - xwin) - self.App.root.winfo_width()
            
            if self.App.root.winfo_width() > 150 : # 150 is the minimum width for the window
                try:
                    self.App.root.geometry(f"{ self.App.root.winfo_width() + difference }x{ self.App.root.winfo_height() }")
                except:
                    pass
            else:
                if difference > 0: # so the window can't be too small (150x150)
                    try:
                        self.App.root.geometry(f"{ self.App.root.winfo_width() + difference }x{ self.App.root.winfo_height() }")
                    except:
                        pass
                    
            resizex_widget.config(bg=self.App.BGCOLOR)

        resizex_widget.bind("<B1-Motion>",resizex)

        # resize the window height
        resizey_widget = tk.Frame(self.App.window,bg=self.App.BGCOLOR,cursor='sb_v_double_arrow')
        resizey_widget.pack(side='bottom',ipadx=2,fill='x')

        def resizey(event):
            ywin = self.App.root.winfo_y()
            difference = (event.y_root - ywin) - self.App.root.winfo_height()

            if self.App.root.winfo_height() > 150: # 150 is the minimum height for the window
                try:
                    self.App.root.geometry(f"{ self.App.root.winfo_width()  }x{ self.App.root.winfo_height() + difference}")
                except:
                    pass
            else:
                if difference > 0: # so the window can't be too small (150x150)
                    try:
                        self.App.root.geometry(f"{ self.App.root.winfo_width()  }x{ self.App.root.winfo_height() + difference}")
                    except:
                        pass

            resizex_widget.config(bg=self.App.BGCOLOR)

        resizey_widget.bind("<B1-Motion>",resizey)

        self.App.root.bind("<FocusIn>",deminimize) # to view the window by clicking on the window icon on the taskbar
        self.App.root.after(10, lambda: set_appwindow(self.App.root)) # to see the icon on the task bar