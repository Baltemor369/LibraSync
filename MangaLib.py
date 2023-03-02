import datetime, tkinter as tk, pickle, re

class Manga:
    def __init__(self, name="",  author="", type="", volume_nb=0, description="", valuation=0.0) -> None:
        self.name = name
        self.author = author
        self.type = type
        self.volume_number = volume_nb
        self.description = description
        self.valuation = valuation
        self._time = "" # Will be used to store the time at which the manga was added
        self.modify=""

    def __repr__(self) -> str:
        buff = f"Name : {self.name} \nAutor : {self.author} \nType : {self.type} \n"
        buff += f"Number of volume : {self.volume_number} \nDescription : {self.description} \n"
        buff += f"Valuation : {self.valuation}/10 \nTime : {self.time} \n"
        buff += "\n"
        return buff

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__        

    def change_volume_number(self, new_value:int) -> None:
        self.volume_number = new_value
    
    def change_type(self, new_type:str) -> None:
        self.type = new_type
    
    def change_author(self, new_author:str) -> None:
        self.author = new_author

    def change_name(self, new_name:str) -> None:
        self.name = new_name
    
    def change_description(self, new_text:str) -> None:
        self.description = new_text

    def change_valuation(self, new_value:float) -> None:
        if 10 >= new_value >= 0:
            self.valuation = new_value

class MangaLib:
    def __init__(self) -> None:
        self.list_manga = []

    def __repr__(self) -> str:
        buff = ""
        for elt in self.list_manga:
            buff += elt.__repr__() 
        return buff

    def add_manga(self, manga:Manga) -> None:
        buff_manga=Manga(manga.name, manga.author, manga.type, manga.volume_number, manga.description, manga.valuation) 
        now=datetime.datetime.now()
        # stores the current time at which the manga is added
        buff_manga._time = "{}-{}-{} {}:{}:{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.list_manga.append(buff_manga) # adds the manga to the list

    def modify_manga(self, manga:Manga, index:int) -> None:
        self.list_manga[index].change_name(manga.name)
        self.list_manga[index].change_author(manga.author)
        self.list_manga[index].change_type(manga.type)
        self.list_manga[index].change_volume_number(manga.volume_number)
        self.list_manga[index].change_description(manga.description)
        self.list_manga[index].change_valuation(manga.valuation)

    def del_manga(self, name="", author="", type="", index="") -> None:
        if re.match("^[0-9]+$", str(index)) is not None: # if the index is a number
            self.list_manga.pop(index) # removes the manga at the specified index
        else:
            # finds a manga with the specified attributes
            generator = self.find_manga(name,author,type) 
            for elt in generator:
                    print(elt)
                    # asks the user to confirm if it's the right manga
                    if input("Is the good one ?y/n\n").upper()=="Y": 
                        self.list_manga.remove(elt)
                        generator.close()
        
    def find_manga(self, name:str, author="", type="") -> Manga:
        for elt in self.list_manga:
            if elt.name == name:
                if elt.author == author: 
                    if elt.type == type:
                        # returns the manga if it matches all the attributes
                        yield elt 
                # returns the manga if it matches the name only
                yield elt 
                  
    def sort_manga(self,sort_category="name"):
        match sort_category:
            case "name":
                self.list_manga.sort(key=lambda Manga: Manga.name) 
            case "time":
                self.list_manga.sort(key=lambda Manga: Manga.time) 
            case "type":
                self.list_manga.sort(key=lambda Manga: Manga.type) 
            case "volume number":
                self.list_manga.sort(key=lambda Manga: Manga.volume_number) 
            case "author":
                self.list_manga.sort(key=lambda Manga: Manga.author) 
            case "valuation":
                self.list_manga.sort(key=lambda Manga: Manga.valuation)
    
    def get(self):
        return self.list_manga

    # Function to save the datas in a file
    def save_data(self):
        with open("data","wb") as file:
            pickler = pickle.Pickler(file)
            pickler.dump(self.list_manga)
    
    # Function to retrieve the datas saved
    def backup(self):
        with open("data","rb") as file:
            unpickler = pickle.Unpickler(file)
            self.list_manga = unpickler.load()

class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Manga Library")

        self.library = MangaLib()
        
        self.library.backup()

        self.display_menu()
    
    def set_geometry(self, width:int, height:int):
        self.geometry(f"{width}x{height}")

    def display_menu(self):
        self.clear()
        
        self.set_geometry(200,200)

        lib_button = tk.Button(self, width=10, text="My Library", command=self.display_library)
        lib_button.pack(pady=10)

        add_manga_button = tk.Button(self, width=10, text="Add Manga", command=self.display_modification)
        add_manga_button.pack(pady=10)

        stat_button = tk.Button(self, width=10, text="Stats", command=self.display_stats)
        
        exit_button = tk.Button(self, width=10, text="Exit", command=self.exit)
        exit_button.pack(pady=10)

    def display_library(self):
        self.clear()
        frame_top = tk.Frame(self)
        frame_top.pack()
        self.set_geometry(950,300)
        self.create_tab(frame_top)
        
        frame_bottom = tk.Frame(self)
        frame_bottom.pack()

        modification_B = tk.Button(frame_bottom,text="New Manga", width=9, relief="raised",command=self.display_modification)
        modification_B.pack(pady=5)
        # back button
        back_button = tk.Button(frame_bottom, width=9, text="Return", command=self.display_menu)
        back_button.pack(pady=5)
    
    def display_modification(self, index=""):
        self.clear()
        
        self.set_geometry(300,200 + 50 * (re.match("^[0-9]+$", str(index))!=None))

        # Creating a top Frame top for arranging labels/Entry and buttons 
        frame_top = tk.Frame(self)
        frame_top.pack(side="top")

        # Creating a column Frame colonne for alignment
        frame_column = tk.Frame(frame_top)
        frame_column.pack(side="left", fill="x")

        # creating Labels
        for key in Manga().__dict__:

            frame_label = tk.Frame(frame_column)
            frame_label.pack(side="top", anchor="center")
            if key =="volume_nb":
                label = tk.Label(frame_label, text="volume number :")
                label.pack(side="left")
            if key != "time" and key != "modify":
                label = tk.Label(frame_label, text=f"{key} :")
                label.pack(side="left")
        
        # Creating a column frame for alignment
        frame_column = tk.Frame(frame_top)
        frame_column.pack(side="left", fill="x") 

        # Creating inputs(Entry)
        for key in Manga().__dict__:

            frame_label = tk.Frame(frame_column)
            frame_label.pack(side="top", anchor="center")

            match key:
                case "name":
                    buff_name = tk.StringVar(self)
                    if re.match("^[0-9]+$", str(index)):
                        buff_name.set(self.library.get()[index].name)
                    self.name_entry = tk.Entry(frame_column, textvariable=buff_name, justify=tk.LEFT)
                    self.name_entry.pack(side="top")

                case "author":
                    buff_author = tk.StringVar(self)
                    if re.match("^[0-9]+$", str(index)):
                        buff_author.set(self.library.get()[index].author)
                    self.author_entry = tk.Entry(frame_column, textvariable=buff_author, justify=tk.LEFT)
                    self.author_entry.pack(side="top")

                case "type":
                    buff_type = tk.StringVar(self)
                    if re.match("^[0-9]+$", str(index)):
                        buff_type.set(self.library.get()[index].type)
                    self.type_entry = tk.Entry(frame_column, textvariable=buff_type, justify=tk.LEFT)
                    self.type_entry.pack(side="top")

                case "volume_number":
                    buff_volume_nb = tk.StringVar(self)
                    if re.match("^[0-9]+$", str(index)):
                        buff_volume_nb.set(self.library.get()[index].volume_number)
                    self.volume_nb_entry = tk.Entry(frame_column, textvariable=buff_volume_nb, justify=tk.LEFT)
                    self.volume_nb_entry.pack(side="top")

                case "description":
                    buff_description = tk.StringVar(self)
                    if re.match("^[0-9]+$", str(index)):
                        buff_description.set(self.library.get()[index].description)
                    self.description_entry = tk.Entry(frame_column, textvariable=buff_description, justify=tk.LEFT)
                    self.description_entry.pack(side="top")

                case "valuation":
                    buff_valuation = tk.StringVar(self)
                    if re.match("^[0-9]+$", str(index)):
                        buff_valuation.set(self.library.get()[index].valuation)
                    self.valuation_entry = tk.Entry(frame_column, textvariable=buff_valuation, justify=tk.LEFT)
                    self.valuation_entry.pack(side="top")

        # Creation of a bottom frame for the layout of labels/Entry and buttons
        frame_bottom = tk.Frame(self)
        frame_bottom.pack(side="top")

        # Creation of the manga add button (add or modify)
        add_button = tk.Button(frame_bottom, width=5,text="Add", command=lambda: self.modification(index))
        add_button.pack(side="top")

        # Display of delete button if it is an element modification
        if re.match("^[0-9]+$", str(index)) is not None:
            del_button = tk.Button(frame_bottom, width=5, text="Delete", command=lambda index=index: self.delete_manga(index))
            del_button.pack(side="top", pady=10)
        
        # back button
        back_button = tk.Button(frame_bottom, width=5, text="Return", command=self.display_library)
        back_button.pack(side="top")

    def display_stats(self):
        # total manga
        # total par type
        # total par auteur
        # nb de manga ajouter derniere semaine/moi/année
        # évaluation statistique(moyen ecart type etc)
        pass

    def modification(self, index=""):
        # recovery input datas
        name_get = self.name_entry.get()
        author_get = self.author_entry.get()
        type_get = self.type_entry.get()
        volume_nb_get = self.volume_nb_entry.get()
        description_get = self.description_entry.get()
        valuation_get = self.valuation_entry.get()

        # check in input datas
        data_verify = True
        # if @name_get, @author_et, @type_get et @description_get 
        # only possess letters or numbers 
        if re.match("^[a-zA-Z0-9 ,.]+$",name_get) is None:
            data_verify = False
        if re.match("^[a-zA-Z0-9 ,.]+$",author_get) is None:
            data_verify = False
        if re.match("^[a-zA-Z0-9 ,.]+$",type_get) is None:
            data_verify = False
        if re.match("^[a-zA-Z0-9 ,.]+$",description_get) is None:
            data_verify = False
        # if @volume_nb_get, @valuation_get
        # only possess number with optional "."
        if re.match("^[0-9.]+$",volume_nb_get) is None:
            data_verify = False
        if re.match("^[0-9.]+$",valuation_get) is None:
            data_verify = False

        if data_verify:
            # If @index is given
            if re.match("^[0-9]+$", str(index)):
                # modification of the manga at @index
                self.library.modify_manga(Manga(name_get, author_get, type_get, int(volume_nb_get), description_get, float(valuation_get)),index)
                self.library.save_data()
            else:
                # add the manga to manga list
                self.library.add_manga(Manga(name_get, author_get, type_get, volume_nb_get, description_get, valuation_get))
                self.library.save_data()
            
            # display the new library
            self.display_library()
            
    def create_tab(self, root_frame:tk.Frame, align_side="top"):
        # Global Frame pour display management
        frame_tab = tk.Frame(root_frame)
        frame_tab.pack(side=align_side)
        
        # Create table headers
        for key in Manga().__dict__:

            # Creation of columns for the layout and alignment of elements
            frame_column = tk.Frame(frame_tab)
            frame_column.pack(side="left")
            
            # Creation of the frame case for the headers
            frame_case = tk.Frame(frame_column,  height=1)
            frame_case.pack(side="top")

            # Management of special cases due to type and size
            match key:
                case "description":
                    text = tk.Label(frame_case, text=key, width=20, height=1, borderwidth=2, relief="solid")
                    text.pack()
                case "modify":
                    # Creating an invisible button
                    # for alignment with table rows
                    button = tk.Button(frame_case, text="", relief="flat")
                    button.pack(anchor="center")
                case _:
                    text = tk.Label(frame_case, text=key, width=15, height=1, borderwidth=2, relief="solid")
                    text.pack()
            
            # tracking index in library scan
            index = 0
            
            # Creation of the boxes with the data according to @key
            for elt in self.library.get():
                
                # Creation of the box for display management
                frame_case = tk.Frame(frame_column)
                frame_case.pack(fill="both", anchor="center")

                # Management of special cases due to type and size
                match key:
                        case "volume_number":
                            text = tk.Label(frame_case, text=elt.__dict__[key], width=15, height=4, borderwidth=2, relief="solid")
                            text.pack()
                        case "description":
                            text = tk.Label(frame_case, text=elt.__dict__[key], width=20, height=4, borderwidth=2, relief="solid")
                            text.pack()
                        case "modify":
                            button = tk.Button(frame_case, text="modify", command=lambda i=index: self.display_modification(i))
                            button.pack(padx=5, pady=20, anchor="center")
                        case _:
                            text = tk.Label(frame_case, text=elt.__dict__[key], width=15, height=4, borderwidth=2, relief="solid")
                            text.pack()
                index += 1
    
    def delete_manga(self, index:int):
        self.library.del_manga(index=index)
        self.library.save_data()
        self.display_library()

    def clear(self):
        for widget in self.winfo_children():
            widget.pack_forget()
    
    def exit(self):
        self.library.save_data()
        self.destroy()