import uuid
import tkinter as tk
import re
from tkinter import ttk
from src.tkTools import clear, popup, prompt
from src.osTools import create_path, path
from src.library import Library,Book

class Interface():
    def __init__(self) -> None:
        self.params = {
            "bg":"#232323",
            "fg":"#EFEFEF",
            "field-bg":"#454545",
            "bg-button":"#000000",
            
            "nbLine":10,
            "path":"data/data.db",
            "old_path":"data/data.db",
            "page":1,
        }

        self.window = tk.Tk()
        self.window.title("LibraSync")
        self.window.config(bg=self.params["bg"])
        icon = tk.PhotoImage(file='img/livre.png')
        self.window.iconphoto(True, icon)
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        # self.window.state('zoomed')

        # Configuration treeview style
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                        background=self.params["bg"],
                        fieldbackground=self.params["field-bg"],
                        foreground=self.params["fg"])
        style.map('Custom.Treeview', background=[('selected', self.params["bg-button"])], foreground=[('selected', self.params["fg"])])

        self.data = Library()
        self.data.init_db(self.params["path"])
        self.data.load_from_db(self.params["path"])

        self.searchConditions = {}
        self.widgets:dict[str,tk.Entry|list] = {}
        self.params["page"] = 1
        self.mainMenu()

        self.window.mainloop()
    def header(self):      
        clear(self.headerFrame)

        title = tk.Label(self.headerFrame, text="My Library", font=("Helvetica",34), bg=self.params["bg"], fg=self.params["fg"])
        title.pack()

    def mainMenu(self):
        clear(self.window)
        self.window.geometry("1000x500")

        self.headerFrame = tk.Frame(self.window, bg=self.params["bg"])
        self.headerFrame.pack(fill="x", pady=20)

        self.header()

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
        
        self.searchBar2 = tk.Entry(searchingFrame, width=10)
        self.searchBar2.pack(side="left", anchor="n", padx=10)
        self.searchBar2.bind("<FocusIn>", self.clear_entry)
        self.searchBar2.bind("<FocusOut>", self.fill_tome_entry)
        self.searchBar2.bind("<Return>", self.searching)
        self.searchBar2.insert(0, "Tome")
        
        self.searchBar3 = tk.Entry(searchingFrame, width=30)
        self.searchBar3.pack(side="left", anchor="n", padx=10)
        self.searchBar3.bind("<FocusIn>", self.clear_entry)
        self.searchBar3.bind("<FocusOut>", self.fill_family_entry)
        self.searchBar3.bind("<Return>", self.searching)
        self.searchBar3.insert(0, "Family")

        self.searchBar4 = tk.Entry(searchingFrame, width=10)
        self.searchBar4.pack(side="left", anchor="n", padx=10)
        self.searchBar4.bind("<FocusIn>", self.clear_entry)
        self.searchBar4.bind("<FocusOut>", self.fill_status_entry)
        self.searchBar4.bind("<Return>", self.searching)
        self.searchBar4.insert(0, "Read")

        startSearching = tk.Button(searchingFrame, text="Search", command=self.searching, width=10, bg=self.params["bg-button"], fg=self.params["fg"])
        startSearching.pack(side="left", anchor="n", padx=10)
        
        self.treeFrame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        self.treeFrame.pack(pady=10)

        self.treeview()

        self.buttons1Frame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        self.buttons1Frame.pack(pady=10)
        
        self.buttons2Frame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        self.buttons2Frame.pack(pady=10)

        self.buttonsPage()
        self.buttons()

    def  buttonsPage(self):
        clear(self.buttons1Frame)

        if self.params["page"] > 1:
            previousButton = tk.Button(self.buttons1Frame, text="Previous", width=15, command=self.previous, bg=self.params["bg-button"], fg=self.params["fg"])
            previousButton.pack(side="left", anchor="n", padx=10)

        if len(self.data.list_books) > ((self.params["page"]-1)*self.params["nbLine"]+self.params["nbLine"]):
            nextButton = tk.Button(self.buttons1Frame, text="Next", width=15, command=self.next, bg=self.params["bg-button"], fg=self.params["fg"])
            nextButton.pack(side="left", anchor="n", padx=10)    
    
    def buttons(self):
        addButton = tk.Button(self.buttons2Frame, text="Add", width=15, command=self.addNewBookMenu, bg=self.params["bg-button"], fg=self.params["fg"])
        addButton.pack(side="left", anchor="n", padx=10)

        modifyButton = tk.Button(self.buttons2Frame, text="Modify", width=15, command=self.modify_selected_row, bg=self.params["bg-button"], fg=self.params["fg"])
        modifyButton.pack(side="left", anchor="n", padx=10)

        delButton = tk.Button(self.buttons2Frame, text="Delete", width=15, command=self.deleteBook, bg=self.params["bg-button"], fg=self.params["fg"])
        delButton.pack(side="left", anchor="n", padx=10)

        settingsButton = tk.Button(self.buttons2Frame, text="Settings", width=15, command=self.settingsMenu, bg=self.params["bg-button"], fg=self.params["fg"])
        settingsButton.pack(side="left", anchor="n", padx=10)

        exitButton = tk.Button(self.buttons2Frame, text="Quit", width=15, command=self.exit, bg=self.params["bg-button"], fg=self.params["fg"])
        exitButton.pack(side="left", anchor="n", padx=10)

    def addNewBookMenu(self):
        clear(self.bodyFrame)

        self.header()

        self.window.geometry("500x600")
        self.widgets["family"] = []

        nameLabel = tk.Label(self.bodyFrame, text="Name : ", bg=self.params["bg"], fg=self.params["fg"])
        nameLabel.pack()
        nameEntry = tk.Entry(self.bodyFrame)
        nameEntry.pack(pady=10)
        self.widgets["name"] = nameEntry

        authorLabel = tk.Label(self.bodyFrame, text="Author : ", bg=self.params["bg"], fg=self.params["fg"])
        authorLabel.pack()
        authorEntry = tk.Entry(self.bodyFrame)
        authorEntry.pack(pady=10)
        self.widgets["author"] = authorEntry

        readLabel = tk.Label(self.bodyFrame, text="Read : ", bg=self.params["bg"], fg=self.params["fg"])
        readLabel.pack()
        readEntry = tk.Entry(self.bodyFrame)
        readEntry.pack(pady=10)
        self.widgets["read"] = readEntry

        tomeLabel = tk.Label(self.bodyFrame, text="Tome : ", bg=self.params["bg"], fg=self.params["fg"])
        tomeLabel.pack()
        tomeEntry = tk.Entry(self.bodyFrame)
        tomeEntry.pack(pady=10)
        self.widgets["tome"] = tomeEntry

        addFamilyButton = tk.Button(self.bodyFrame, text="Add Family", command=lambda : self.addFamily(familiesFrame), bg=self.params["bg-button"], fg=self.params["fg"])
        addFamilyButton.pack(pady=10)
        
        clearButton = tk.Button(self.bodyFrame, text="Clear", command=lambda : clear(familiesFrame), bg=self.params["bg-button"], fg=self.params["fg"])
        clearButton.pack(pady=10)
        
        familiesFrame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        familiesFrame.pack(pady=10)       

        addButton = tk.Button(self.bodyFrame, text="Add", width=15, command=self.newBook, bg=self.params["bg-button"], fg=self.params["fg"])
        addButton.pack(pady=10)

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=self.params["bg-button"], fg=self.params["fg"])
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
        tomes = self.tome_analyze(inputs["tome"])
        if tomes == []:
            popup(self.window, "Invalid Tome inputs.", "Error")
        else:
            for i in tomes:
                self.data.addBook(Book(self.refGenerator(), inputs["name"], inputs["author"], i, inputs["read"], inputs["families"]))
            self.mainMenu()
    
    def tome_analyze(self, text:str):
        tomes:list[int] = []
        
        if not re.match(r"^(\d+(-\d+)?)(,\d+(-\d+)?)*$", text):
            return []
        
        text = text.split(",")
        for rng in text:
            if '-' in rng:
                start, end = map(int, rng.split('-'))
                if start >= end:
                    return []

        for elt in text:
            if '-' in elt:
                tmp = elt.split("-")
                for i in range(int(tmp[0]),int(tmp[1])+1):
                    tomes.append(i)
            else:
                tomes.append(int(elt))

        
        return tomes
    
    def deleteBook(self):
        selected_items = self.tree.selection()
        if selected_items:
            for elt in selected_items:
                ref = self.tree.item(elt, "values")[0]
                self.tree.delete(elt)
                self.data.removeBook(ref)
                self.tree.insert("", 'end', text="Nouvelle Ligne", values=("Nouveau1","Nouveau2","Nouveau3"))
        
        self.treeview()
        self.buttonsPage()

    def modify_selected_row(self):
        self.old_values = []
        selected_items = list(self.tree.selection())
        for elt in selected_items:
            self.old_values.append(self.tree.item(elt, "values"))

        self.process_next_item()

    def process_next_item(self):
        if self.old_values:
            self.item_values = self.old_values.pop(0)
            self.modify_book_menu()
        else:
            self.mainMenu()

    def modify_book_menu(self):
        clear(self.bodyFrame)

        self.window.geometry("500x600")
        self.widgets = {}
        self.widgets["family"] = []

        nameLabel = tk.Label(self.bodyFrame, text="Name : ", bg=self.params["bg"])
        nameLabel.pack()
        nameEntry = tk.Entry(self.bodyFrame)
        nameEntry.insert(0, self.item_values[1])
        nameEntry.pack(pady=10)
        self.widgets["name"] = nameEntry

        authorLabel = tk.Label(self.bodyFrame, text="Author : ", bg=self.params["bg"])
        authorLabel.pack()
        authorEntry = tk.Entry(self.bodyFrame)
        authorEntry.insert(0, self.item_values[2])
        authorEntry.pack(pady=10)
        self.widgets["author"] = authorEntry
        
        tomeLabel = tk.Label(self.bodyFrame, text="Tome : ", bg=self.params["bg"])
        tomeLabel.pack()
        tomeEntry = tk.Entry(self.bodyFrame)
        tomeEntry.insert(0, self.item_values[3])
        tomeEntry.pack(pady=10)
        self.widgets["tome"] = tomeEntry

        readLabel = tk.Label(self.bodyFrame, text="Read : ", bg=self.params["bg"])
        readLabel.pack()
        readEntry = tk.Entry(self.bodyFrame)
        readEntry.insert(0, self.item_values[5])
        readEntry.pack(pady=10)
        self.widgets["read"] = readEntry

        familiesFrame = tk.Frame(self.bodyFrame, bg=self.params["bg"])
        familiesFrame.pack(pady=10)

        for family in self.item_values[4].split():
            self.addFamily(familiesFrame, family)

        addFamilyButton = tk.Button(self.bodyFrame, text="Add Family", command=lambda: self.addFamily(familiesFrame), bg=self.params["bg-button"], fg=self.params["fg"])
        addFamilyButton.pack(pady=10)

        addButton = tk.Button(self.bodyFrame, text="Save", width=15, command=self.updateBook, bg=self.params["bg-button"], fg=self.params["fg"])
        addButton.pack(pady=10)

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=self.params["bg-button"], fg=self.params["fg"])
        backButton.pack()
    
    def updateBook(self):
        ref = self.item_values[0]
        name = self.widgets["name"].get() if self.widgets["name"]!="" and self.item_values[1] != self.widgets["name"] else self.item_values[1]
        author = self.widgets["author"].get() if self.widgets["author"]!="" and self.item_values[2] != self.widgets["author"] else self.item_values[2]
        tome = self.widgets["tome"].get() if self.widgets["tome"]!="" and self.item_values[3] != self.widgets["tome"] else self.item_values[3]
        read_status = self.widgets["read"].get() if self.widgets["read"]!="" and self.item_values[4] != self.widgets["read"] else self.item_values[4]
        families = [self.widgets["family"][i].get() for i in range(len(self.widgets["family"])) if self.widgets["family"][i].get()]

        book = self.data.getByRef(ref)
        if book:
            book.name = name
            book.author = author
            book.tome = tome
            book.family = families
            book.read_status = read_status.lower() == "true"
            self.process_next_item()
    
    def refGenerator(self):
        return str(uuid.uuid4())

    def clear_entry(self, event):
        if event.widget.get() in ["Name", "Author","Tome", "Read", "Family"]:
            event.widget.delete(0, "end")
    
    def fill_name_entry(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Name")
    def fill_author_entry(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Author")
    def fill_tome_entry(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Tome")
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
            "tome":self.searchBar2.get() if self.searchBar2.get() != "Tome" else "",
            "read_status":self.searchBar3.get() if self.searchBar3.get() != "Read" else "",
            "family":self.searchBar4.get() if self.searchBar4.get() != "Family" else ""
        }
        self.searchConditions = args

        self.treeview()

    def treeview(self):
        clear(self.treeFrame)
        columns = ("Ref", "Name","Author","Tome","Family","Read")
        self.tree = ttk.Treeview(self.treeFrame, style="Custom.Treeview", columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree, c, False))
            self.tree.column(col, anchor="center")
        
        ls = self.data.select(((self.params["page"]-1)*self.params["nbLine"]), self.params["nbLine"], where=self.searchConditions) 
        if len(ls)==0:
            self.params["page"] -= 1 if self.params["page"] > 0 else 0
            ls = self.data.select(((self.params["page"]-1)*self.params["nbLine"]), self.params["nbLine"], where=self.searchConditions)

        for elt in ls:
            self.tree.insert("","end", values=(elt.ref, elt.name, elt.author, elt.tome, elt.family, elt.read_status))
        
        self.tree.column("Ref", width=30)
        self.tree.column("Tome", width=50)
        self.tree.pack()
    
    def sort_column(self, tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            tree.move(child, "", index)

        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))

    def next(self):
        self.params["page"] += 1
        self.treeview()
        self.buttonsPage()
    
    def previous(self):
        self.params["page"] -= 1
        self.treeview()
        self.buttonsPage()
    
    def settingsMenu(self):
        clear(self.bodyFrame)

        label = tk.Label(self.bodyFrame, text="Nb Line Display", bg=self.params["bg"], fg=self.params["fg"])
        label.pack()

        nbEntry = tk.Entry(self.bodyFrame)
        nbEntry.insert(0, str(self.params["nbLine"]))
        nbEntry.pack()
        self.widgets["nbLine"] = nbEntry
        
        pathLabel = tk.Label(self.bodyFrame, text="Saved File Path", bg=self.params["bg"], fg=self.params["fg"])
        pathLabel.pack()

        pathEntry = tk.Entry(self.bodyFrame)
        pathEntry.insert(0, self.params["path"])
        pathEntry.pack()
        self.widgets["path"] = pathEntry

        saveButton = tk.Button(self.bodyFrame, text="Save", width=15, command=self.mainMenu, bg=self.params["bg-button"], fg=self.params["fg"])
        saveButton.pack(pady=10)

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=self.params["bg-button"], fg=self.params["fg"])
        backButton.pack(pady=10)
    
    def saveSettings(self):
        nb_line = self.widgets["nbLine"].get()
        new_path = self.widgets["path"].get()

        if path.exists(new_path):
            self.params["old_path"] = self.params["path"]
            self.params["path"] = new_path
        else:
            response = prompt("Create path", f"the path {new_path} doesn't exist,\nDo you want to create it ?")
            if response:
                create_path(new_path)

        if 10 < nb_line < 50 :   
            self.params["nbLine"] = nb_line 

    def exit(self):
        try:
            self.data.save_to_db(self.params["path"])
            self.window.quit()
        except Exception as e:
            popup(self.window, f"Error with saving data:\n{e}")