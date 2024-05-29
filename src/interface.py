import tkinter as tk
import uuid
from tkinter import ttk
from src.tkTools import clear, popup
from src.library import Library,Book

class Interface():
    def __init__(self) -> None:
        self.data_path = "data/data.db"
        self.params = {
            "bg":"#EEEEEE",
            "fg":"#000000",
            "bg-button":"#CCCCCC",
        }

        self.window = tk.Tk()
        self.window.title("LibraSync")
        self.window.config(bg=self.params["bg"])
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        # self.window.state('zoomed')

        # Configuration treeview style
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                        background=self.params["bg-button"],
                        fieldbackground="#2E2E2E",
                        foreground=self.params["fg"])
        style.map('Custom.Treeview', background=[('selected', '#4A4A4A')], foreground=[('selected', 'white')])

        self.data = Library()
        self.data.init_db(self.data_path)
        self.data.load_from_db(self.data_path)
        self.searchConditions = {}
        self.references = []
        self.page:int = 1
        self.nbLine = 10
        self.mainMenu()

        self.window.mainloop()

    def mainMenu(self):
        clear(self.window)
        self.window.geometry("1000x500")

        self.selected_item = {}
        
        title = tk.Label(self.window, text="My Library", font=("Helvetica",34), bg=self.params["bg"])
        title.pack(pady=30)


        self.bodyFrame = tk.Frame(self.window, bg=self.params["bg"])
        self.bodyFrame.pack()

        searchingFrame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        searchingFrame.pack(pady=10)

        self.searchBar = tk.Entry(searchingFrame, width=40)
        self.searchBar.pack(side="left", anchor="n", padx=10)
        self.searchBar.bind("<FocusIn>", self.clear_entry)
        self.searchBar.bind("<FocusOut>", self.fill_name_entry)
        self.searchBar.bind("<Return>", self.searching)
        self.searchBar.insert(0, "Name")

        self.searchBar1 = tk.Entry(searchingFrame, width=40)
        self.searchBar1.pack(side="left", anchor="n", padx=10)
        self.searchBar1.bind("<FocusIn>", self.clear_entry)
        self.searchBar1.bind("<FocusOut>", self.fill_author_entry)
        self.searchBar1.bind("<Return>", self.searching)
        self.searchBar1.insert(0, "Author")
        
        self.searchBar3 = tk.Entry(searchingFrame, width=30)
        self.searchBar3.pack(side="left", anchor="n", padx=10)
        self.searchBar3.bind("<FocusIn>", self.clear_entry)
        self.searchBar3.bind("<FocusOut>", self.fill_family_entry)
        self.searchBar3.bind("<Return>", self.searching)
        self.searchBar3.insert(0, "Family")

        self.searchBar2 = tk.Entry(searchingFrame, width=20)
        self.searchBar2.pack(side="left", anchor="n", padx=10)
        self.searchBar2.bind("<FocusIn>", self.clear_entry)
        self.searchBar2.bind("<FocusOut>", self.fill_status_entry)
        self.searchBar2.bind("<Return>", self.searching)
        self.searchBar2.insert(0, "Read")

        startSearching = tk.Button(searchingFrame, text="Search", command=self.searching, width=10, bg=self.params["bg-button"])
        startSearching.pack(side="left", anchor="n", padx=10)
        
        self.treeFrame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        self.treeFrame.pack(pady=10)

        self.treeview()

        self.buttonsFrame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        self.buttonsFrame.pack(pady=10)

        self.buttons()

    def  buttons(self):
        clear(self.buttonsFrame)

        if self.page > 1:
            previousButton = tk.Button(self.buttonsFrame, text="Previous", width=15, command=self.previous, bg=self.params["bg-button"])
            previousButton.pack(side="left", anchor="n", padx=10)

        addButton = tk.Button(self.buttonsFrame, text="Add", width=15, command=self.addNewBookMenu, bg=self.params["bg-button"])
        addButton.pack(side="left", anchor="n", padx=10)

        modifyButton = tk.Button(self.buttonsFrame, text="Modify", width=15, command=self.modify_selected_row, bg=self.params["bg-button"])
        modifyButton.pack(side="left", anchor="n", padx=10)

        delButton = tk.Button(self.buttonsFrame, text="Delete", width=15, command=self.deleteBook, bg=self.params["bg-button"])
        delButton.pack(side="left", anchor="n", padx=10)

        settingsButton = tk.Button(self.buttonsFrame, text="Settings", width=15, command=self.settingsMenu, bg=self.params["bg-button"])
        settingsButton.pack(side="left", anchor="n", padx=10)

        exitButton = tk.Button(self.buttonsFrame, text="Quit", width=15, command=self.exit, bg=self.params["bg-button"])
        exitButton.pack(side="left", anchor="n", padx=10)

        if len(self.data.list_books) > ((self.page-1)*10+10):
            nextButton = tk.Button(self.buttonsFrame, text="Next", width=15, command=self.next, bg=self.params["bg-button"])
            nextButton.pack(side="left", anchor="n", padx=10)    
    
    def addNewBookMenu(self):
        clear(self.bodyFrame)
        self.window.geometry("500x600")
        self.widgets:dict[str,tk.Entry|list] = {}
        self.widgets["family"] = []

        nameLabel = tk.Label(self.bodyFrame, text="Name : ")
        nameLabel.pack()
        nameEntry = tk.Entry(self.bodyFrame)
        nameEntry.pack(pady=10)
        self.widgets["name"] = nameEntry

        authorLabel = tk.Label(self.bodyFrame, text="Author : ")
        authorLabel.pack()
        authorEntry = tk.Entry(self.bodyFrame)
        authorEntry.pack(pady=10)
        self.widgets["author"] = authorEntry

        readLabel = tk.Label(self.bodyFrame, text="Read : ")
        readLabel.pack()
        readEntry = tk.Entry(self.bodyFrame)
        readEntry.pack(pady=10)
        self.widgets["read"] = readEntry

        tomeLabel = tk.Label(self.bodyFrame, text="Tome : ")
        tomeLabel.pack()
        tomeEntry = tk.Entry(self.bodyFrame)
        tomeEntry.pack(pady=10)
        self.widgets["tome"] = tomeEntry

        addFamilyButton = tk.Button(self.bodyFrame, text="Add Family", command=lambda : self.addFamily(familiesFrame), bg=self.params["bg-button"])
        addFamilyButton.pack(pady=10)
        
        clearButton = tk.Button(self.bodyFrame, text="Clear", command=lambda : clear(familiesFrame), bg=self.params["bg-button"])
        clearButton.pack(pady=10)
        
        familiesFrame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        familiesFrame.pack(pady=10)       

        addButton = tk.Button(self.bodyFrame, text="Add", width=15, command=self.newBook, bg=self.params["bg-button"])
        addButton.pack(pady=10)

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=self.params["bg-button"])
        backButton.pack()
    
    def addFamily(self, frame:tk.Frame|tk.Tk, value:str=""):
        familiesLabel = tk.Label(frame, text="Families : ", bg=self.params["bg"])
        familiesLabel.pack()
        
        familiesEntry = tk.Entry(frame)
        familiesEntry.pack(pady=10)
        familiesEntry.insert(0, value)
        self.widgets["family"].append(familiesEntry)
    
    def newBook(self):
        inputs = {
            "name":self.widgets["name"].get(),
            "author":self.widgets["author"].get(),
            "tome":self.widgets["tome"].get(),
            "read":self.widgets["read"].get().lower() in ["true","yes","y"],
            "families": [elt.get() for elt in self.widgets["family"]]
        }
        self.data.addBook(Book(self.refGenerator(), inputs["name"], inputs["author"], inputs["tome"], inputs["read"], inputs["families"]))
        self.mainMenu()
    
    def deleteBook(self):
        selected_item = self.tree.selection()
        if selected_item:
            ref = self.tree.item(selected_item, "values")[0]
            self.tree.delete(selected_item)
            self.data.removeBook(ref)

    def modify_selected_row(self):
        self.selected_item = self.tree.selection()
        self.item_values = self.tree.item(self.selected_item, "values")

        if self.selected_item:
            values = self.tree.item(self.selected_item, "values")
            self.modify_book_menu(values)

    def modify_book_menu(self, values):
        clear(self.bodyFrame)
        self.window.geometry("500x600")
        self.widgets = {}
        self.widgets["family"] = []

        nameLabel = tk.Label(self.bodyFrame, text="Name : ", bg=self.params["bg"])
        nameLabel.pack()
        nameEntry = tk.Entry(self.bodyFrame)
        nameEntry.insert(0, values[1])
        nameEntry.pack(pady=10)
        self.widgets["name"] = nameEntry

        authorLabel = tk.Label(self.bodyFrame, text="Author : ", bg=self.params["bg"])
        authorLabel.pack()
        authorEntry = tk.Entry(self.bodyFrame)
        authorEntry.insert(0, values[2])
        authorEntry.pack(pady=10)
        self.widgets["author"] = authorEntry

        readLabel = tk.Label(self.bodyFrame, text="Read : ", bg=self.params["bg"])
        readLabel.pack()
        readEntry = tk.Entry(self.bodyFrame)
        readEntry.insert(0, values[4])
        readEntry.pack(pady=10)
        self.widgets["read"] = readEntry

        familiesFrame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        familiesFrame.pack(pady=10)

        for family in values[3].split():
            self.addFamily(familiesFrame, family)

        addFamilyButton = tk.Button(self.bodyFrame, text="Add Family", command=lambda: self.addFamily(familiesFrame), bg=self.params["bg-button"])
        addFamilyButton.pack(pady=10)

        addButton = tk.Button(self.bodyFrame, text="Modify", width=15, command=self.updateBook, bg=self.params["bg-button"])
        addButton.pack(pady=10)

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=self.params["bg-button"])
        backButton.pack()
    
    def updateBook(self):
        if self.selected_item:
            ref = self.item_values[0]
            name = self.widgets["name"].get()
            author = self.widgets["author"].get()
            read_status = self.widgets["read"].get()
            families = [self.widgets["family"][i].get() for i in range(len(self.widgets["family"])) if self.widgets["family"][i].get()]

            book = self.data.getByRef(ref)
            if book:
                book.name = name
                book.author = author
                book.family = families
                book.read_status = read_status == "true"

            self.mainMenu()
    
    def refGenerator(self):
        return str(uuid.uuid4())

    def clear_entry(self, event):
        if event.widget.get() in ["Name", "Author", "Read", "Family"]:
            event.widget.delete(0, "end")
    
    def fill_name_entry(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Name")
    def fill_author_entry(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Author")
    def fill_status_entry(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Read")
    def fill_family_entry(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Family")

    def searching(self, evt=""):
        clear(self.treeFrame)

        args = {
            "name":self.searchBar.get() if self.searchBar.get() != "Name" else "",
            "author":self.searchBar1.get() if self.searchBar1.get() != "Author" else "",
            "read_status":self.searchBar2.get() if self.searchBar2.get() != "Read" else "",
            "family":self.searchBar3.get() if self.searchBar3.get() != "Family" else ""
        }
        self.searchConditions = args

        self.treeview()

    def treeview(self):
        clear(self.treeFrame)

        self.tree = ttk.Treeview(self.treeFrame, style="Custom.Treeview", columns=("Name","Author","Tome","Family","Read"), show='headings')

        for col in ("Name", "Tome", "Author", "Family", "Read"):
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree, c, False))
        
        for elt in self.data.select(((self.page-1)*self.nbLine), self.nbLine, where=self.searchConditions):
            self.tree.insert("","end", values=(elt.name, elt.author, elt.tome, elt.family, elt.read_status))
        
        self.tree.pack()
    
    def sort_column(self, tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            tree.move(child, "", index)

        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))

    def next(self):
        self.page += 1
        self.treeview()
        self.buttons()
    
    def previous(self):
        self.page -= 1
        self.treeview()
        self.buttons()
    
    def settingsMenu(self):
        clear(self.bodyFrame)

        dark_mode_button = tk.Button(self.bodyFrame, text="DarkMode", command=self.switch_mode, bg=self.params["bg-button"])
        dark_mode_button.pack()

        label = tk.Label(self.bodyFrame, text="NbLineDisplay", bg=self.params["bg"])
        label.pack()

        # number input
        
        pathLabel = tk.Label(self.bodyFrame, text="SaveFilePath", bg=self.params["bg"])
        pathLabel.pack()

        # text input

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=self.params["bg-button"])
        backButton.pack()

    def switch_mode(self):
        # change colors definition 
        self.params["bg"] = "#333333" if self.params["bg"] != "#333333" else "#EEEEEE"
        self.params["fg"] = "#FFFFFF" if self.params["fg"] != "#FFFFFF" else "#000000"
        self.params["bg-button"] = "#CCCCCC" if self.params["bg-button"] != "#CCCCCC" else "#555555"
        
        # redirect to settings menu
        self.settingsMenu()

    def exit(self):
        try:
            self.data.save_to_db(self.data_path)
            self.window.quit()
        except Exception as e:
            popup(self.window, f"Error with saving data:\n{e}")