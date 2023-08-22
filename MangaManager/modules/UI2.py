import tkinter as tk
import modules.useful_fct as use
from modules.Library import Library
from assets.const import *

class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Library")
        self.iconbitmap("assets/logo.ico")
        self.configure(bg=BG)
        
        self.bind("<Escape>", self.exit)

        self.parentFrame = tk.Frame(self, bg=BG)
        self.parentFrame.pack(fill="both",expand=True)

        self.myLib = Library()

        self.main_menu()
    
    def run(self):
        self.mainloop()

    def main_menu(self):
        use.clear(self.parentFrame)

        title = tk.Label(self.parentFrame, text="My Library Manager", **TITLE)
        title.pack(pady=10)

        lib_access_B = tk.Button(self.parentFrame, text="Library Access", width=12, **BUTTON, command=self.library_menu)
        lib_access_B.pack(pady=5)
        exit_B = tk.Button(self.parentFrame, text="Exit", width=12, **BUTTON, command=self.exit)
        exit_B.pack(pady=5)

        use.set_geometry(self, 50, 50)
    
    def library_menu(self):
        use.clear(self.parentFrame)

        title = tk.Label(self.parentFrame, text="My Library Manager", **TITLE)
        title.pack(pady=10)

        search_bar_E = tk.Entry(self.parentFrame, **ENTRY)
        search_bar_E.insert(0, "Search a book")
        search_bar_E.bind("<FocusIn>", lambda e: e.widget.delete(0, "end") if e.widget.get()=="Search a book" else self.nothing())
        search_bar_E.pack(pady=5)


        use.set_geometry(self,50,50)
    
    def exit(self, e=None):
        self.destroy()
    
    def nothing(self):
        pass