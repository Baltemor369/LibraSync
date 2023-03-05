import datetime, tkinter as tk, pickle, re
import dateutil.relativedelta as dr
from typing import List

# To do :
# + Module recherche
# + volume "1-4"=> du volume 1 au 4
# + finir statistique
# + développer module historique(moyenne par semaine/mois voir combien ont été ajout pendant une semaine donnée)
# + refaire affichage stats
# +

class CounterList:
    def __init__(self) -> None:
        self.counter_list = []
    
    def __repr__(self) -> str:
        buff = "\n"
        for elt in self.counter_list:
            buff += f"{elt['name']} : {elt['counter']}\n"
        return buff

    def add_name(self, name:str) -> None:
        if not self.check_name(name):
            self.counter_list.append({'name': name, 'counter': 1})
        else:
            self.increment_counter(name)

    def increment_counter(self, name:str) -> None:
        for item in self.counter_list:
            if item['name'] == name:
                item['counter'] += 1

    def check_name(self, name:str) -> bool:
        for item in self.counter_list:
            if item['name'] == name:
                return True
        return False

class Manga:
    def __init__(self, name="",  author="", type="", volume_nb=0, description="", valuation=0.0, time=datetime.datetime.now()) -> None:
        self.name = name
        self.author = author
        self.type = type
        self.volume_number = volume_nb
        self.description = description
        self.valuation = valuation
        self.time = time # Will be used to store the time at which the manga was added
        self.modify=""

    def __repr__(self) -> str:
        buff = f"Name : {self.name} \nAutor : {self.author} \nType : {self.type} \n"
        buff += f"Number of volume : {self.volume_number} \nDescription : {self.description} \n"
        buff += f"Valuation : {self.valuation}/10 \nTime : {self.time.year}-{self.time.month}-{self.time.day} {self.time.hour}:{self.time.minute}:{self.time.second} \n"
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
        self.list_manga:List[Manga] = []

    def __repr__(self) -> str:
        buff = ""
        for elt in self.list_manga:
            buff += elt.__repr__() 
        return buff

    def add_manga(self, manga:Manga) -> None:
        self.list_manga.append(Manga(manga.name, manga.author, manga.type, manga.volume_number, manga.description, manga.valuation, manga.time)) # adds the manga to the list

    def modify_manga(self, manga:Manga, index:int) -> None:
        self.list_manga[index].change_name(manga.name)
        self.list_manga[index].change_author(manga.author)
        self.list_manga[index].change_type(manga.type)
        self.list_manga[index].change_volume_number(manga.volume_number)
        self.list_manga[index].change_description(manga.description)
        self.list_manga[index].change_valuation(manga.valuation)

    def del_manga(self, name="", author="", type="", index="") -> None:
        if re.match("^\d+$", str(index)) is not None: # if the index is a number
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
                  
    def sort_manga(self,sort_category="name", reverse=False) -> None:
        match sort_category:
            case "name":
                self.list_manga.sort(key=lambda Manga: Manga.name, reverse=reverse) 
            case "time":
                self.list_manga.sort(key=lambda Manga: Manga.time, reverse=reverse)
            case "type":
                self.list_manga.sort(key=lambda Manga: Manga.type, reverse=reverse)
            case "volume_number":
                self.list_manga.sort(key=lambda Manga: Manga.volume_number, reverse=reverse)
            case "author":
                self.list_manga.sort(key=lambda Manga: Manga.author, reverse=reverse)
            case "valuation":
                self.list_manga.sort(key=lambda Manga: Manga.valuation, reverse=reverse)
    
    def get(self) -> List[Manga]:
        return self.list_manga
    
    def get_names(self) -> List[str]:
        buff = []
        for elt in self.get():
            buff.append(elt.name)
        return buff
    
    def get_authors(self) -> List[str]:
        buff = []
        for elt in self.get():
            buff.append(elt.author)
        return buff
    
    def get_types(self) -> List[str]:
        buff = []
        for elt in self.get():
            buff.append(elt.type)
        return buff
    
    def get_valuations(self) -> List[float]:
        buff = []
        for elt in self.get():
            buff.append(elt.valuation)
        return buff

    # Function to save the datas in a file
    def save_data(self) -> None:
        with open("data.txt","w") as file:
            i=0
            for elt in self.get():
                file.write(f"@#N-{str(elt.name)}#A-{str(elt.author)}#TY-{str(elt.type)}#VN-{str(elt.volume_number)}#D-{str(elt.description)}#VA-{str(elt.valuation)}#TI-{str(elt.time)}#@\n")
                i += 1
    
    # Function to retrieve the datas saved
    def backup(self) -> None:
        self.read_file("data.txt")

    def read_file(self, file_name:str):
        all_manga = []
        with open(file_name,"r") as file:
            while 1:
                buffer = file.readline()
                if buffer != "":
                    all_manga.append(buffer)
                else:
                    break
        self.convert_data(all_manga)

    def convert_data(self, mangas:List[str]):
        name_r = r"#N-([\w,\.\- ^_]+)#"
        author_r = r"#A-([\w,\.\- ^_]+)#"
        type_r = r"#TY-([\w,\.\- ^_]+)#"
        volume_nb_r = r"#VN-(\d{1,3})#"
        description_r = r"#D-([\w ,\.\-^_]+)#"
        valuation_r = r"#VA-(10(?:\.0)?|\d(?:\.\d)?)#"
        time_r = r"#TI-(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})#"

        format_string = "%Y-%m-%d %H:%M:%S"

        for elt in mangas:
            name = re.search(name_r,elt).group(1)
            author = re.search(author_r,elt).group(1)
            type = re.search(type_r,elt).group(1)
            volume_nb = re.search(volume_nb_r,elt).group(1)
            description = re.search(description_r,elt).group(1)
            valuation = re.search(valuation_r,elt).group(1)
            time = re.search(time_r,elt).group(1)
            time = datetime.datetime.strptime(time,format_string)

            self.add_manga(Manga(name,author,type,int(volume_nb),description,float(valuation),time))

class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Manga Library")

        self.library = MangaLib()
        self.sort_key = "name"
        self.sort_reverse = False
        
        self.library.sort_manga(self.sort_key)
        
        # catcch Escap key press
        self.bind("<Escape>",self.exit)
        
        # retrieve manga library already saved in "data" file
        self.library.backup()

        self.display_menu()
    
    def set_geometry(self, width:int, height:int):
        self.geometry(f"{width}x{height}")

    def display_menu(self):
        self.clear()
        
        self.set_geometry(200,200)

        self.sort_key = "name"

        lib_button = tk.Button(self, width=10, text="My Library", command=self.display_library)
        lib_button.pack(pady=10)

        add_manga_button = tk.Button(self, width=10, text="Add Manga", command=self.display_modification)
        add_manga_button.pack(pady=10)

        stat_button = tk.Button(self, width=10, text="Stats", command=self.display_stats)
        stat_button.pack(pady=10)
        
        exit_button = tk.Button(self, width=10, text="Exit", command=self.exit)
        exit_button.pack(pady=10)

    def display_library(self):
        self.clear()
        frame_top = tk.Frame(self)
        frame_top.pack()
        self.set_geometry(950,150+60*len(self.library.get()))

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
        
        self.set_geometry(300,200 + 50 * (re.match("^\d+$", str(index))!=None))

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
                    if re.match("^\d+$", str(index)):
                        buff_name.set(self.library.get()[index].name)
                    self.name_entry = tk.Entry(frame_column, textvariable=buff_name, justify=tk.LEFT)
                    self.name_entry.pack(side="top")

                case "author":
                    buff_author = tk.StringVar(self)
                    if re.match("^\d+$", str(index)):
                        buff_author.set(self.library.get()[index].author)
                    self.author_entry = tk.Entry(frame_column, textvariable=buff_author, justify=tk.LEFT)
                    self.author_entry.pack(side="top")

                case "type":
                    buff_type = tk.StringVar(self)
                    if re.match("^\d+$", str(index)):
                        buff_type.set(self.library.get()[index].type)
                    self.type_entry = tk.Entry(frame_column, textvariable=buff_type, justify=tk.LEFT)
                    self.type_entry.pack(side="top")

                case "volume_number":
                    buff_volume_nb = tk.StringVar(self)
                    if re.match("^\d+$", str(index)):
                        buff_volume_nb.set(self.library.get()[index].volume_number)
                    self.volume_nb_entry = tk.Entry(frame_column, textvariable=buff_volume_nb, justify=tk.LEFT)
                    self.volume_nb_entry.pack(side="top")

                case "description":
                    buff_description = tk.StringVar(self)
                    if re.match("^\d+$", str(index)):
                        buff_description.set(self.library.get()[index].description)
                    self.description_entry = tk.Entry(frame_column, textvariable=buff_description, justify=tk.LEFT)
                    self.description_entry.pack(side="top")

                case "valuation":
                    buff_valuation = tk.StringVar(self)
                    if re.match("^\d+$", str(index)):
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
        if re.match("^\d+$", str(index)) is not None:
            del_button = tk.Button(frame_bottom, width=5, text="Delete", command=lambda index=index: self.delete_manga(index))
            del_button.pack(side="top", pady=10)
        
        # back button
        back_button = tk.Button(frame_bottom, width=5, text="Return", command=self.display_library)
        back_button.pack(side="top")

    def display_stats(self):
        self.clear()
        
        self.calcul_stats()
        
        self.set_geometry(300,100*len(self.library.get()))
        
        # refaire l'affichae => pas beau
        for key in self.data_stat:
            frame_row = tk.Frame(self)
            frame_row.pack()
            frame_case_key = tk.Frame(frame_row)
            frame_case_key.pack(side="left")
            label = tk.Label(frame_case_key,text=f"{key} : ")
            label.pack()
            frame_case_value = tk.Frame(frame_row)
            frame_case_value.pack(side="left")
            label = tk.Label(frame_case_value,text=f"{self.data_stat[key]}")
            label.pack()

        # back button
        back_button = tk.Button(self, width=9, text="Return", command=self.display_menu)
        back_button.pack(side="bottom",pady=5)

    def calcul_stats(self):
        self.data_stat = {}
        # total manga
        self.data_stat["Total mangas"] = len(self.library.get())
        
        # total by type
        stat_type = CounterList()

        for elt in self.library.get_types():
            stat_type.add_name(elt)
        self.data_stat["Total by type"] = stat_type
        
        # total par auteur
        stat_author = CounterList()

        for elt in self.library.get_authors():
            stat_author.add_name(elt)
        self.data_stat["Total by author"] = stat_author
        
        # total de manga ajouter derniere semaine/moi/année
        # current time
        now = datetime.datetime.now()

        # counter definition
        self.data_stat["Total last week"] = 0
        self.data_stat["Total last month"] = 0
        self.data_stat["Total last year"] = 0
        
        for elt in self.library.get():
            delta = dr.relativedelta(now, elt.time)
            if delta.days <= 7:
                self.data_stat["Total last week"] += 1
            if delta.months <=1:
                self.data_stat["Total last month"] += 1
            if delta.years <= 1:
                self.data_stat["Total last year"] += 1
        
        valuations = self.library.get_valuations()

        self.data_stat["Average"] = round(sum(valuations)/len(valuations),2)
        self.data_stat["Standard deviation"] = max(valuations) - min(valuations)

    def modification(self, index=""):
        # recovery input datas
        name_get = self.name_entry.get()
        author_get = self.author_entry.get()
        type_get = self.type_entry.get()
        volume_nb_get = self.volume_nb_entry.get()
        description_get = self.description_entry.get()
        valuation_get = self.valuation_entry.get()

        # Check in input datas
        data_verify = True

        # Creating regex exp for the check in input data
        # allow alphanumeric characters and "," "." "-" " "
        reg_text = r"^[\w,\.\- ^_]+$"
        # allow list of int separate by "," or "-"
        reg_volume = r"^\d{1,3}$"
        # allow int and float between 0 and 10 included
        reg_valuation = r"^(?:10(?:\.0)?|\d(?:\.\d)?)$"

        if re.match(reg_text,name_get) is None:
            data_verify = False
        if re.match(reg_text,author_get) is None:
            data_verify = False
        if re.match(reg_text,type_get) is None:
            data_verify = False
        if re.match(reg_text,description_get) is None:
            data_verify = False
        if re.match(reg_volume,volume_nb_get) is None:
            data_verify = False
        if re.match(reg_valuation,valuation_get) is None:
            data_verify = False

        if data_verify:
            # If @index is given
            if re.match("^\d+$", str(index)):
                # modification of the manga at @index
                self.library.modify_manga(Manga(name_get, author_get, type_get, int(volume_nb_get), description_get, float(valuation_get)),index)
                # self.library.save_data()
            else:
                # add the manga to manga list
                self.library.add_manga(Manga(name_get, author_get, type_get, int(volume_nb_get), description_get, float(valuation_get)))
                # self.library.save_data()
            
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
                    if key == self.sort_key:
                        if self.sort_reverse:
                            text = tk.Label(frame_case, text=f"{key} ▲", width=15, height=1, borderwidth=2, relief="solid")
                        else:
                            text = tk.Label(frame_case, text=f"{key} ▼", width=15, height=1, borderwidth=2, relief="solid")
                    else:
                        text = tk.Label(frame_case, text=key, width=15, height=1, borderwidth=2, relief="solid")
                    text.pack()
                    text.bind("<Button-1>", lambda evt,k=key: self.sort_my_lib(k))
            
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
    
    def sort_my_lib(self, key:str):
        if key == self.sort_key:
            self.sort_reverse = not self.sort_reverse
            self.library.sort_manga(key,self.sort_reverse)
        else:
            self.sort_key=key
            self.library.sort_manga(key)
        self.display_library()

    def delete_manga(self, index:int):
        self.library.del_manga(index=index)
        # self.library.save_data()
        self.display_library()

    def clear(self):
        for widget in self.winfo_children():
            widget.pack_forget()
    
    def exit(self, evt=""):
        self.library.save_data()
        self.destroy()