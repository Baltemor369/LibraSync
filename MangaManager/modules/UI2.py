import tkinter as tk
from tkinter import messagebox
import modules.useful_fct as use
from modules.Library import Library
from modules.Book import Book
from assets.const import *

# agencement des frames - voir le paint

class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Library")
        self.iconbitmap("assets/logo.ico")
        self.configure(bg=BG)
        
        self.bind("<Escape>", self.exit)

        self.myLib = Library()
        self.page_nb = 0
        self.sample_length = 10

        self.main_menu()
    
    def run(self):
        self.mainloop()

    def main_menu(self):
        use.clear(self)

        title = tk.Label(self, text="My Library Manager", **TITLE)
        title.pack(pady=10)

        lib_access_B = tk.Button(self, text="Library Access", **BUTTON, command=self.library_menu)
        lib_access_B.pack(pady=5)
        exit_B = tk.Button(self, text="Exit", **BUTTON, command=self.exit)
        exit_B.pack(pady=5)

        use.set_geometry(self, marginEW=50, marginNS=50)
    
    def library_menu(self):
        use.clear(self)

        titleFrame = tk.Frame(self, bg=BG)
        titleFrame.pack(fill="x")

        title = tk.Label(titleFrame, text="My Library Manager", **TITLE)
        title.pack(pady=10)

        bodyFrame = tk.Frame(self, bg=BG)
        bodyFrame.pack(fill="both", expand=True)

        navFrame = tk.Frame(bodyFrame, bg=BG)
        navFrame.pack(fill="y", side="left", **PAD15)

        topFrame = tk.Frame(navFrame, bg=BG)
        topFrame.pack(pady=5, fill="both")

        add_B = tk.Button(topFrame, text="Add Book", **BUTTON)
        add_B.pack(pady=5)

        botFrame = tk.Frame(navFrame, bg=BG)
        botFrame.pack(pady=5, fill="x", side="bottom")

        exit_B = tk.Button(botFrame, text="Exit", **BUTTON, command=self.exit)
        exit_B.pack(pady=5)

        divFrame = tk.Frame(bodyFrame, bg=BG)
        divFrame.pack(fill="both", expand=True, side="right", **PAD15)

        search_bar_E = tk.Entry(divFrame, **ENTRY)
        search_bar_E.insert(0, "Search a book")
        search_bar_E.bind("<FocusIn>", lambda e: e.widget.delete(0, "end") if e.widget.get()=="Search a book" else self.nothing())
        search_bar_E.pack()
        
        tableFrame = tk.Frame(divFrame, bg=BGLIGHT)
        tableFrame.pack(fill="both", expand=True, pady=5)

        self.display_table(tableFrame)
        
        turnPageFrame = tk.Frame(divFrame, bg=BG)
        turnPageFrame.pack(fill="x", pady=10)

        leftDivFrame = tk.Frame(turnPageFrame, bg=BG)
        leftDivFrame.pack(fill="both", expand=True, pady=10, side="left")

        previous_B = tk.Button(leftDivFrame, text="Previous", **BUTTON)
        previous_B.pack(side="left")

        rightDivFrame = tk.Frame(turnPageFrame, bg=BG)
        rightDivFrame.pack(fill="both", expand=True, pady=10, side="right")
        
        next_B = tk.Button(rightDivFrame, text="Next", **BUTTON)
        next_B.pack(side="right")

        use.set_geometry(self, marginEW=50, marginNS=50)
    

    def display_table(self, root:tk.Tk|tk.Frame|tk.Toplevel):
        
        divFrame = tk.Frame(root, bg=BG)
        divFrame.pack(fill="both", expand=True)

        topRowFram = tk.Frame(divFrame, bg=BG)
        topRowFram.pack(fill="x", expand=True)
        
        for key,val in Book(0).get().items():
            caseFrame = tk.Frame(topRowFram, bg=BG, **CASE)
            caseFrame.pack(side="left", fill="both", expand=True)
            if key != "id":
                label = tk.Label(caseFrame, text=key, **LABEL)
                label.pack(fill="both")

        for book in self.myLib.get_all_book():
            rowFrame = tk.Frame(divFrame, bg=BGLIGHT)
            rowFrame.pack(fill="x", expand=True)

            for key,val in book.get():
                caseFrame = tk.Frame(rowFrame, bg=BGLIGHT, **CASE)
                caseFrame.pack(side="left", fill="both", expand=True)
                if key != "id":
                    label = tk.Label(caseFrame, text=val, **LABEL)
                    label.pack(fill="both")        
    
    def error(self, text:str):
        messagebox.showinfo("Error", text)

    def exit(self, e=None):
        self.destroy()
    
    def nothing(self):
        pass