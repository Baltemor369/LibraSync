#public lib import
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re, math
#personnal lib improt
import modules.useful_fct as use
from modules.Library import Library
from modules.Book import Book
from modules.const import *
from modules.tome_string_to_int import tome_str_to_int

class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Library")
        self.iconbitmap("assets/logo.ico")
        self.configure(bg=BG)
        
        self.bind("<Escape>", self.exit)
        self.bind("<Delete>", self.delete_item)
        self.bind("<BackSpace>", self.delete_item)
        self.protocol("WM_DELETE_WINDOW", self.exit)

        self.books = Library()
        self.currentTab = "menu"
        self.limit = 10
        self.maxPage = int(math.ceil(len(self.books.get_all()) / self.limit) - 1)
        self.currentPage = 0
        self.search_input = tk.StringVar()
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
        self.currentTab = "menu"
        self.titrate("Menu")

        lib_access_B = tk.Button(self, text="Library Access", **BUTTON15, command=self.library_menu)
        lib_access_B.pack(pady=10)
        exit_B = tk.Button(self, text="Exit", **BUTTON15, command=self.exit)
        exit_B.pack(pady=3)

        use.set_geometry(self, marginEW=50, marginNS=50)
    
    def library_menu(self):
        use.clear(self)
        self.currentTab = "tab"
        self.titrate("Tab")

        self.currentPage = 0

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

        searchFrame = tk.Frame(divFrame, bg=BG)
        searchFrame.pack(fill="x", expand=True)
        
        subFrame = tk.Frame(searchFrame, bg=BG)
        subFrame.pack(side="left", fill="x", expand=True)

        self.search_bar_E = tk.Entry(subFrame, **ENTRY, width=100, textvariable=self.search_input)
        self.search_bar_E.insert(0, "?Search a book?")
        self.search_bar_E.bind("<FocusIn>", lambda e: e.widget.delete(0, "end") if e.widget.get()=="?Search a book?" else self.do_nothing())
        self.search_bar_E.pack(anchor="center")
        self.search_input.trace_add("write", self.search_update)

        sub1Frame = tk.Frame(searchFrame, bg=BG)
        sub1Frame.pack(side="right")

        filter_B = tk.Button(sub1Frame, text="Filter", **BUTTON10, command=self.filter_window)
        filter_B.pack(side="left")
        
        self.tableFrame = tk.Frame(divFrame, bg=BGLIGHT)
        self.tableFrame.pack(fill="both", expand=True, pady=5)

        self.display_table(self.tableFrame)
        
        turnPageFrame = tk.Frame(divFrame, bg=BG)
        turnPageFrame.pack(fill="x", pady=10)

        leftDivFrame = tk.Frame(turnPageFrame, bg=BG)
        leftDivFrame.pack(fill="both", expand=True, pady=10, side="left")

        previous_B = tk.Button(leftDivFrame, text="Previous", command=self.previous_page, **BUTTON10)
        if self.currentPage > 0:
            previous_B.pack(side="left")

        rightDivFrame = tk.Frame(turnPageFrame, bg=BG)
        rightDivFrame.pack(fill="both", expand=True, pady=10, side="right")
        
        next_B = tk.Button(rightDivFrame, text="Next", command=self.next_page, **BUTTON10)
        if self.currentPage < self.maxPage:
            next_B.pack(side="right")

        use.set_geometry(self, marginEW=50, marginNS=50)
    
    def filter_window(self):
        popup = use.PromptWindow(self, "Filter", labelsText=KEYFILTER, labelParam={"padx":10})
        self.wait_window(popup.window)
        if popup.get_values():
            values = popup.get_values()
            text = ""
            for i,val in enumerate(values):
                if val:
                    text += KEYFILTER[i]
                    text += val + ";"
            self.search_bar_E.delete(0,"end")
            self.search_bar_E.insert(0, text)
            self.display_table(self.tableFrame)
        
    def search_update(self, *args):
        self.search_input.set(self.search_bar_E.get())
        self.display_table(self.tableFrame)
    
    def next_page(self, e=None):
        if self.currentPage < self.maxPage:
            self.currentPage += 1
            self.library_menu()
    
    def previous_page(self, e=None):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.library_menu()
        

    def display_table(self, root:tk.Tk|tk.Frame|tk.Toplevel):
        use.clear(root)

        divFrame = tk.Frame(root, bg=BG)
        divFrame.pack(fill="both", expand=True)
        
        # Create a treeview with columns
        self.tree = ttk.Treeview(divFrame, columns=HEADERS, show="headings")

        # Set column headings
        self.tree.heading("Title", text="Title", command=lambda: self.tree_sort("Title"))
        self.tree.heading("Author", text="Author", command=lambda: self.tree_sort("Author"))
        self.tree.heading("Type", text="Type", command=lambda: self.tree_sort("Type"))
        self.tree.heading("Tome", text="Tome", command=lambda: self.tree_sort("Tome"))

        # Set anchor to center for all columns
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")

        # add data to treeview
        for elt in self.books.get(self.currentPage * self.limit, self.limit, self.search_input.get()):
            book = (elt[1], elt[2], elt[3], elt[4])
            self.tree.insert("",tk.END, values=book)
        
        self.tree.bind("<Double-1>", lambda e: self.modify_elt(e))

        self.tree.pack(fill="both")
    
    def modify_elt(self, evt):
        item = self.tree.identify("item", evt.x, evt.y)
        if item:
            values = self.tree.item(item, "values")
            self.ask = use.PromptWindow(self, f"Modify {values[0]}", ("Title : ", "Author : ", "Type : ", "Tome : "), values)
            self.wait_window(self.ask.window)
            if self.ask.values:
                for i,val in enumerate(self.ask.values):
                    if not val:
                        self.ask.values[i] = values[i]
                self.tree.item(item, values=self.ask.values)
                self.books.update_book(Book(*values), Book(*self.ask.values))
    
    def tree_sort(self, col:str):
        if col.lower() != self.books.get_key_sort().lower():
            self.books.set_reverse(False)
        else:
            self.books.set_reverse(not self.books.reverse )
        self.books.set_sort_order(col.lower())
        self.library_menu()
    
    def delete_item(self, e:tk.Event):
        if self.currentTab == "tab":
            items = self.tree.selection()
            if items:
                for item in items:
                    values = self.tree.item(item, "values")
                    confirmed = messagebox.askyesno("Confirmation",f"Are you sure you want to delete :\nTitle : {values[0]}\nAuthor : {values[1]}\nType : {values[2]}\nTome : {values[3]} ?")
                    if confirmed:
                        self.tree.delete(item)
                        self.books.delete_book([Book(*values)])
                self.library_menu()

    def add_menu(self):
        use.clear(self)
        self.currentTab = "add"
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
        if re.match("^[a-zA-Z0-9 ']+$", values[0]):
            title = values[0]
            if re.match("^[a-zA-Z0-9 ']+$", values[1]):
                author = values[1]
                if re.match("^[a-zA-Z/ ]+$", values[2]):
                    type = values[2]
                    if re.match("^[0-9,-]+$", values[3]):
                        tome = tome_str_to_int(values[3])
                        book_added = 0
                        for ind in tome:
                            # saved in database
                            if self.books.add_books([Book(title, author, type, ind)]):
                                book_added += 1
                            else:
                                self.alert(f"Error with the book {title} from {author} tome {ind}.")
                        self.maxPage = int(math.ceil(len(self.books.get_all()) / self.limit) - 1)
                        self.alert(f"{book_added} books added successfully")
                        self.library_menu()
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
        self.books.close()
        self.destroy()
    
    def do_nothing(self):
        pass