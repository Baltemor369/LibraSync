import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import modules.useful_fct as use
import re, math
from modules.Library import Library
from modules.Book import Book
from modules.const import *

# agencement des frames - voir le paint

class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Library")
        self.iconbitmap("assets/logo.ico")
        self.configure(bg=BG)
        
        self.bind("<Escape>", self.exit)
        self.protocol("WM_DELETE_WINDOW", self.exit)

        self.books = Library()
        self.limit = 10
        self.maxPage = int(math.ceil(len(self.books.get_all()) / self.limit) - 1)
        self.currentPage = 0
        self.reverse_sort = False
        self.sort_key = ""

        self.ask = None

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

        lib_access_B = tk.Button(self, text="Library Access", **BUTTON15, command=self.library_menu)
        lib_access_B.pack(pady=10)
        exit_B = tk.Button(self, text="Exit", **BUTTON15, command=self.exit)
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

        add_B = tk.Button(topFrame, text="Add Book", **BUTTON10, command=self.add_menu)
        add_B.pack(pady=5)

        botFrame = tk.Frame(navFrame, bg=BG)
        botFrame.pack(pady=5, fill="x", side="bottom")

        exit_B = tk.Button(botFrame, text="Return", **BUTTON10, command=self.main_menu)
        exit_B.pack(pady=5)

        divFrame = tk.Frame(bodyFrame, bg=BG)
        divFrame.pack(fill="both", expand=True, side="right", **PAD15)

        search_bar_E = tk.Entry(divFrame, **ENTRY, width=60)
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

        previous_B = tk.Button(leftDivFrame, text="Previous", **BUTTON10)
        previous_B.pack(side="left")

        rightDivFrame = tk.Frame(turnPageFrame, bg=BG)
        rightDivFrame.pack(fill="both", expand=True, pady=10, side="right")
        
        next_B = tk.Button(rightDivFrame, text="Next", **BUTTON10)
        next_B.pack(side="right")

        use.set_geometry(self, marginEW=50, marginNS=50)
    

    def display_table(self, root:tk.Tk|tk.Frame|tk.Toplevel):
        use.clear(root)

        divFrame = tk.Frame(root, bg=BG)
        divFrame.pack(fill="both", expand=True)
        
        # Create a treeview with columns
        tree = ttk.Treeview(divFrame, columns=HEADERS, show="headings")

        # Set column headings
        tree.heading("Title", text="Title", command=lambda: self.tree_sort(tree, "Title"))
        tree.heading("Author", text="Author", command=lambda: self.tree_sort(tree, "Author"))
        tree.heading("Type", text="Type", command=lambda: self.tree_sort(tree, "Type"))
        tree.heading("Tome", text="Tome", command=lambda: self.tree_sort(tree, "Tome"))

        # Set anchor to center for all columns
        for col in tree["columns"]:
            tree.column(col, anchor="center")

        # add data to treeview
        for elt in self.books.get_many(self.currentPage * self.limit, self.limit):
            book = (elt[1], elt[2], elt[3], elt[4])
            tree.insert("",tk.END, values=book)
        
        tree.bind("<Double-1>", lambda e: self.modify_elt(e, tree))

        tree.pack(fill="both")
    
    def modify_elt(self, evt, tree:ttk.Treeview):
        item = tree.identify("item", evt.x, evt.y)
        if item:
            values = tree.item(item, "values")
            self.ask = use.PromptWindow(self, f"Modify {values[0]}", ("Title : ", "Author : ", "Type : ", "Tome : "), values)
            self.wait_window(self.ask.window)
            if self.ask.values:
                for i,val in enumerate(self.ask.values):
                    if not val:
                        self.ask.values[i] = values[i]
                tree.item(item, values=self.ask.values)
    
    def tree_sort(self, tree, col):
        if col != self.sort_key:
            self.reverse_sort = False
            self.sort_key = col
        else:
            self.reverse_sort = not self.reverse_sort
        
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        data.sort(reverse=self.reverse_sort)
        for index, (val, child) in enumerate(data):
            tree.move(child, "", index)
    
    def delete_row(tree, item):
        tree.delete(item)

    def add_menu(self):
        use.clear(self)

        self.titrate("Add")

        bodyFrame = tk.Frame(self, bg=BG)
        bodyFrame.pack(fill="both", expand=True)
        
        divframe = tk.Frame(bodyFrame, bg=BG)
        divframe.pack(fill="both", expand=True)

        LabelFrame = tk.Frame(divframe, bg=BG)
        LabelFrame.pack(fill="both", expand=True, side="left")
        
        tmp = ["Title :", "Author :", "Type :", "Tome n° :"]
        for txt in tmp:
            div1frame = tk.Frame(LabelFrame, bg=BG)
            div1frame.pack(fill="both", expand=True)
            label = tk.Label(div1frame, text=txt, **LABEL)
            label.pack(side="right")
        
        InputFrame = tk.Frame(divframe, bg=BG)
        InputFrame.pack(fill="both", expand=True, side="right")
        
        self.list_entry = []
        for i,_ in enumerate(tmp):
            div2frame = tk.Frame(InputFrame, bg=BG)
            div2frame.pack(fill="both", expand=True)

            self.list_entry.append(tk.Entry(div2frame, **ENTRY))
            self.list_entry[i].pack(pady=1)
            self.list_entry[i].bind("<Return>",self.add_book)
        
        footerFrame = tk.Frame(bodyFrame, bg=BG)
        footerFrame.pack(fill="x", expand=True)

        add_B = tk.Button(footerFrame, text=" Add ", **BUTTON10, command=self.add_book)
        add_B.pack()

        botFrame = tk.Frame(self, bg=BG)
        botFrame.pack(fill="x", expand=True)

        sub1Frame = tk.Frame(botFrame, bg=BG)
        sub1Frame.pack(fill="both", expand=True, side="left")

        return_B = tk.Button(sub1Frame, text="Return", **BUTTON10, command=self.library_menu)
        return_B.pack(pady=5, side="left")

        sub2Frame = tk.Frame(botFrame, bg=BG)
        sub2Frame.pack(fill="both", expand=True, side="right")

        exit_B = tk.Button(sub2Frame, text="Exit", **BUTTON10, command=self.exit)
        exit_B.pack(pady=5, side="right")

        use.set_geometry(self, marginEW=50, marginNS=50)
    
    def add_book(self, e=None):
        values = []
        for elt in self.list_entry:
            values.append(elt.get())
        if re.match("^[a-zA-Z0-9 ']+$", values[0]) is not None:
            title = values[0]
            if re.match("^[a-zA-Z0-9 ']+$", values[1]) is not None:
                author = values[1]
                if re.match("^[a-zA-Z/ ]+$", values[2]) is not None:
                    type = values[2]
                    if re.match("^[0-9]+$", values[3]) is not None:
                        tome = values[3]
                        
                        ## MODIFICATION HERE ##
                        if self.books.add_books([Book(title, author, type, tome)]):
                            self.alert("Books added successfully")
                            self.library_menu()
                        else:
                            self.alert("Book already registered.")
                    else:
                        self.alert("Incorrect Tome value.")
                else:
                    self.alert("Incorrect Type value.")
            else:
                self.alert("Incorrect Author value.")
        else:
            self.alert("Incorrect Title value.")

    def alert(self, text:str):
        messagebox.showinfo("Alert", text)

    def exit(self, e=None):
        try:
            self.ask.destroy()
        except AttributeError:
            pass
        except tk.TclError:
            pass

        self.destroy()
    
    def nothing(self):
        pass