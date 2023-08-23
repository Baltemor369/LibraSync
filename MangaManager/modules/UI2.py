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
        self.myLib.load_data()
        self.page_nb = 0
        self.sample_length = 10

        self.main_menu()
    
    def run(self):
        self.mainloop()
    
    def titrate(self, text:str):
        titleFrame = tk.Frame(self, bg=BG)
        titleFrame.pack(fill="x")

        title = tk.Label(titleFrame, text=f"Library Manager - {text}", **TITLE)
        title.pack(pady=10)

    def main_menu(self):
        use.clear(self)

        self.titrate("Menu")

        lib_access_B = tk.Button(self, text="Library Access", **BUTTON, command=self.library_menu)
        lib_access_B.pack(pady=10)
        exit_B = tk.Button(self, text="Exit", **BUTTON, command=self.exit)
        exit_B.pack(pady=3)

        use.set_geometry(self, marginEW=50, marginNS=50)
    
    def library_menu(self):
        use.clear(self)

        self.titrate("Tab")

        bodyFrame = tk.Frame(self, bg=BG)
        bodyFrame.pack(fill="both", expand=True)

        navFrame = tk.Frame(bodyFrame, bg=BG)
        navFrame.pack(fill="y", side="left", **PAD15)

        topFrame = tk.Frame(navFrame, bg=BG)
        topFrame.pack(pady=5, fill="both")

        add_B = tk.Button(topFrame, text="Add Book", **BUTTON, command=self.add_menu)
        add_B.pack(pady=5)

        botFrame = tk.Frame(navFrame, bg=BG)
        botFrame.pack(pady=5, fill="x", side="bottom")

        exit_B = tk.Button(botFrame, text="Return", **BUTTON, command=self.main_menu)
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
        use.clear(root)
        self.myLib.load_data()

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
    
    def add_menu(self):
        use.clear(self)

        self.titrate("Add")

        bodyFrame = tk.Frame(self, bg=BG)
        bodyFrame.pack(fill="both", expand=True)
        
        divframe = tk.Frame(bodyFrame, bg=BG)
        divframe.pack(fill="both", expand=True)

        LabelFrame = tk.Frame(divframe, bg=BG)
        LabelFrame.pack(fill="both", expand=True, side="left")
        
        for txt in ["Title :", "Author :", "Type :", "Tome n° :"]:
            div1frame = tk.Frame(LabelFrame, bg=BG)
            div1frame.pack(fill="both", pady=8)
            label = tk.Label(div1frame, text=txt, **LABEL)
            label.pack(side="right")
        
        InputFrame = tk.Frame(divframe, bg=BG)
        InputFrame.pack(fill="both", expand=True, side="right")
        
        for _ in range(4):
            div2frame = tk.Frame(InputFrame, bg=BG)
            div2frame.pack(fill="x", expand=True)
            entry = tk.Entry(div2frame, **ENTRY)
            entry.pack()
        
        footerFrame = tk.Frame(bodyFrame, bg=BG)
        footerFrame.pack(fill="x", expand=True)

        add_B = tk.Button(footerFrame, text=" Add ", **BUTTON)
        add_B.pack()

        botFrame = tk.Frame(self, bg=BG)
        botFrame.pack()

        sub1Frame = tk.Frame(botFrame, bg=BG)
        sub1Frame.pack(fill="both", expand=True, side="left")

        return_B = tk.Button(sub1Frame, text="Return", **BUTTON, command=self.library_menu)
        return_B.pack(pady=5)

        sub2Frame = tk.Frame(botFrame, bg=BG)
        sub2Frame.pack(fill="both", expand=True, side="right")

        exit_B = tk.Button(sub2Frame, text="Exit", **BUTTON, command=self.exit)
        exit_B.pack(pady=5)

        use.set_geometry(self, marginEW=50, marginNS=50)

    def error(self, text:str):
        messagebox.showinfo("Error", text)

    def exit(self, e=None):
        self.destroy()
    
    def nothing(self):
        pass