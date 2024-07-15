import uuid
import tkinter as tk
import re
from tkinter import ttk
from src.const import *
from src.tkTools import clear, popup, prompt
from src.osTools import create_path, path
from src.library import Library,Book

class Interface():
    def __init__(self) -> None:
        self.params = {
            "nbLine":10,
            "path":DATA_FILE,
            "old_path":DATA_FILE,
            "page":1,   
        }
        
        self.window = tk.Tk()
        self.window.title("LibraSync")
        self.window.config(bg=BG)
        icon = tk.PhotoImage(file='img/livre.png')
        self.window.iconphoto(True, icon)
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        # self.window.state('zoomed')

        # Configuration treeview style
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                        background=BG,
                        fieldbackground=FIELD_BG,
                        foreground=FG)
        style.map('Custom.Treeview', background=[('selected', BG_BUTTON)], foreground=[('selected', FG)])

        self.data = Library()
        self.data.init_db(self.params["path"])
        self.data.load_from_db(self.params["path"])

        self.searchConditions = {}
        self.widgets:dict[str,tk.Entry|list|tk.StringVar] = {}
        self.params["page"] = 1
        self.mainMenu()

        self.window.mainloop()
    def header(self):      
        clear(self.headerFrame)

        title = tk.Label(self.headerFrame, text="My Library", font=("Helvetica",34), bg=BG, fg=FG)
        title.pack()

    def mainMenu(self):
        clear(self.window)
        self.window.geometry("1000x500")

        self.headerFrame = tk.Frame(self.window, bg=BG)
        self.headerFrame.pack(fill="x", pady=20)

        self.header()

        self.bodyFrame = tk.Frame(self.window, bg=BG)
        self.bodyFrame.pack()

        searchingFrame = tk.Frame(self.bodyFrame, bg=BG)
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

        startSearching = tk.Button(searchingFrame, text="Search", command=self.searching, width=10, bg=BG_BUTTON, fg=FG)
        startSearching.pack(side="left", anchor="n", padx=10)
        
        self.treeFrame = tk.Frame(self.bodyFrame, bg=BG)
        self.treeFrame.pack(pady=10)

        self.treeview()

        self.buttons1Frame = tk.Frame(self.bodyFrame, bg=BG)
        self.buttons1Frame.pack(pady=10)
        
        self.buttons2Frame = tk.Frame(self.bodyFrame, bg=BG)
        self.buttons2Frame.pack(pady=10)

        self.buttonsPage()
        self.buttons()

    def  buttonsPage(self):
        clear(self.buttons1Frame)

        if self.params["page"] > 1:
            previousButton = tk.Button(self.buttons1Frame, text="Previous", width=15, command=self.previous, bg=BG_BUTTON, fg=FG)
            previousButton.pack(side="left", anchor="n", padx=10)

        if len(self.data.list_books) > ((self.params["page"]-1)*self.params["nbLine"]+self.params["nbLine"]):
            nextButton = tk.Button(self.buttons1Frame, text="Next", width=15, command=self.next, bg=BG_BUTTON, fg=FG)
            nextButton.pack(side="left", anchor="n", padx=10)    
    
    def buttons(self):
        addButton = tk.Button(self.buttons2Frame, text="Add", width=15, command=self.addNewBookMenu, bg=BG_BUTTON, fg=FG)
        addButton.pack(side="left", anchor="n", padx=10)

        modifyButton = tk.Button(self.buttons2Frame, text="Modify", width=15, command=self.modify_selected_row, bg=BG_BUTTON, fg=FG)
        modifyButton.pack(side="left", anchor="n", padx=10)

        delButton = tk.Button(self.buttons2Frame, text="Delete", width=15, command=self.deleteBook, bg=BG_BUTTON, fg=FG)
        delButton.pack(side="left", anchor="n", padx=10)

        settingsButton = tk.Button(self.buttons2Frame, text="Settings", width=15, command=self.settingsMenu, bg=BG_BUTTON, fg=FG)
        settingsButton.pack(side="left", anchor="n", padx=10)

        exitButton = tk.Button(self.buttons2Frame, text="Quit", width=15, command=self.exit, bg=BG_BUTTON, fg=FG)
        exitButton.pack(side="left", anchor="n", padx=10)

    def addNewBookMenu(self):
        clear(self.bodyFrame)

        self.header()

        self.window.geometry("500x600")

        nameLabel = tk.Label(self.bodyFrame, text="Name : ", bg=BG, fg=FG)
        nameLabel.pack()
        nameEntry = tk.Entry(self.bodyFrame, width=30)
        nameEntry.pack(pady=10)
        self.widgets["name"] = nameEntry

        authorLabel = tk.Label(self.bodyFrame, text="Author : ", bg=BG, fg=FG)
        authorLabel.pack()
        authorEntry = tk.Entry(self.bodyFrame, width=30)
        authorEntry.pack(pady=10)
        self.widgets["author"] = authorEntry

        readLabel = tk.Label(self.bodyFrame, text="Read : ", bg=BG, fg=FG)
        readLabel.pack()
        readValue = tk.StringVar()
        readValue.set("no")  # valeur par défaut
        options = ["yes", "no"]
        readOptionMenu = tk.OptionMenu(self.bodyFrame, readValue, *options)
        readOptionMenu.pack(pady=10)
        self.widgets["read"] = readValue

        tomeLabel = tk.Label(self.bodyFrame, text="Tome : ", bg=BG, fg=FG)
        tomeLabel.pack()
        tomeEntry = tk.Entry(self.bodyFrame, width=30)
        tomeEntry.pack(pady=10)
        self.widgets["tome"] = tomeEntry
        
        familiesFrame = tk.Frame(self.bodyFrame, bg=BG)
        familiesFrame.pack(pady=10)

        familyLabel = tk.Label(familiesFrame, text="Family : ", bg=BG, fg=FG)
        familyLabel.pack(side=tk.LEFT)

        familiesEntry = tk.Entry(familiesFrame)
        familiesEntry.pack(side=tk.LEFT, padx=5)
        familiesEntry.insert(0, "")
        self.widgets["family"] = familiesEntry

        addButton = tk.Button(self.bodyFrame, text="Add", width=15, command=self.newBook, bg=BG_BUTTON, fg=FG)
        addButton.pack(pady=10)

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=BG_BUTTON, fg=FG)
        backButton.pack()

    
    def newBook(self):
        inputs = {
            "name":self.widgets["name"].get(),
            "author":self.widgets["author"].get(),
            "tome":self.widgets["tome"].get(),
            "read":self.widgets["read"].get(),
            "families": self.widgets["family"].get()
        }
        tomes = self.tome_analyze(inputs["tome"])
        if tomes == []:
            popup(self.window, "Invalid Tome inputs.", "Error")
        else:
            for i in tomes:
                self.data.addBook(Book(self.refGenerator(), inputs["name"], inputs["author"], i, inputs["families"], inputs["read"]))
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
        books = []
        selected_items = list(self.tree.selection())
        
        for elt in selected_items:
            values = list(self.tree.item(elt, "values"))
            books.append(Book(*values))

        self.process_next_item(books)

    def process_next_item(self, list_books:list):
        if len(list_books)>0:
            self.modify_book_menu(list_books, list_books.pop(0))
        else:
            self.mainMenu()

    def modify_book_menu(self, books, book:Book):
        clear(self.bodyFrame)

        self.window.geometry("500x600")

        nameLabel = tk.Label(self.bodyFrame, text="Name : ", bg=BG)
        nameLabel.pack()
        nameEntry = tk.Entry(self.bodyFrame, width=30)
        nameEntry.insert(0, book.name)
        nameEntry.pack(pady=10)
        self.widgets["name"] = nameEntry

        authorLabel = tk.Label(self.bodyFrame, text="Author : ", bg=BG)
        authorLabel.pack()
        authorEntry = tk.Entry(self.bodyFrame, width=30)
        authorEntry.insert(0, book.author)
        authorEntry.pack(pady=10)
        self.widgets["author"] = authorEntry
        
        tomeLabel = tk.Label(self.bodyFrame, text="Tome : ", bg=BG)
        tomeLabel.pack()
        tomeEntry = tk.Entry(self.bodyFrame, width=30)
        tomeEntry.insert(0, book.tome)
        tomeEntry.pack(pady=10)
        self.widgets["tome"] = tomeEntry

        readLabel = tk.Label(self.bodyFrame, text="Read : ", bg=BG)
        readLabel.pack()
        readValue = tk.StringVar()
        readValue.set(book.read_status)
        options = ["yes", "no"]
        readOptionMenu = tk.OptionMenu(self.bodyFrame, readValue, *options)
        readOptionMenu.pack(pady=10)
        self.widgets["read"] = readValue

        familiesFrame = tk.Frame(self.bodyFrame, bg=BG)
        familiesFrame.pack(pady=10)

        familyLabel = tk.Label(familiesFrame, text="Family : ", bg=BG, fg=FG)
        familyLabel.pack(side=tk.LEFT)

        familiesEntry = tk.Entry(familiesFrame)
        familiesEntry.pack(side=tk.LEFT, padx=5)
        familiesEntry.insert(0, book.family)
        self.widgets["family"] = familiesEntry

        addButton = tk.Button(self.bodyFrame, text="Save", width=15, command=lambda : self.updateBook(books, book), bg=BG_BUTTON, fg=FG)
        addButton.pack(pady=10)

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=BG_BUTTON, fg=FG)
        backButton.pack()
    
    def editFamilyInput(self, frame: tk.Frame, familyName, book:Book):
        familyFrame = tk.Frame(frame, bg=BG)
        familyFrame.pack(pady=10)

        familyLabel = tk.Label(familyFrame, text="Family : ", bg=BG, fg=FG)
        familyLabel.pack(side=tk.LEFT)

        familiesEntry = tk.Entry(familyFrame)
        familiesEntry.pack(side=tk.LEFT, padx=5)
        familiesEntry.insert(0, familyName)
        
        self.widgets["family"].append(familiesEntry)

        def deleteFamily():
            familyFrame.destroy()
            self.widgets["family"].remove(familiesEntry)
            book.removeFamily(familyName)

        deleteButton = tk.Button(familyFrame, text="Delete", command=deleteFamily, bg=BG_BUTTON, fg=FG)
        deleteButton.pack(side=tk.LEFT, padx=5)
    
    def updateBook(self, books, book:Book):
        ref = book.ref
        name = self.widgets["name"].get() if book.name != self.widgets["name"] else book.name
        author = self.widgets["author"].get() if book.author != self.widgets["author"] else book.author
        tome = self.widgets["tome"].get() if book.tome != self.widgets["tome"] else book.tome
        read_status = self.widgets["read"].get() if book.read_status != self.widgets["read"] else book.read_status
        families = self.widgets["family"].get()

        book = self.data.getByRef(ref)
        if book:
            book.name = name
            book.author = author
            book.tome = tome
            book.family = families
            book.read_status = read_status
            self.process_next_item(books)
    
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

        label = tk.Label(self.bodyFrame, text="Nb Line Display", bg=BG, fg=FG)
        label.pack()

        nbEntry = tk.Entry(self.bodyFrame)
        nbEntry.insert(0, str(self.params["nbLine"]))
        nbEntry.pack()
        self.widgets["nbLine"] = nbEntry
        
        pathLabel = tk.Label(self.bodyFrame, text="Saved File Path", bg=BG, fg=FG)
        pathLabel.pack()

        pathEntry = tk.Entry(self.bodyFrame)
        pathEntry.insert(0, self.params["path"])
        pathEntry.pack()
        self.widgets["path"] = pathEntry

        saveButton = tk.Button(self.bodyFrame, text="Save", width=15, command=self.mainMenu, bg=BG_BUTTON, fg=FG)
        saveButton.pack(pady=10)

        backButton = tk.Button(self.bodyFrame, text="Back", width=15, command=self.mainMenu, bg=BG_BUTTON, fg=FG)
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
            self.window.quit()