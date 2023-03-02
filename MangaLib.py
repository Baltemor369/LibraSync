import datetime, tkinter as tk, tkinter.ttk as tkk, pickle, re

class Manga:
    def __init__(self, name="",  creator="", type="", volume_nb=0, description="", valuation=0.0) -> None:
        self.name = name
        self.autor = creator
        self.type = type
        self.volume_number = volume_nb
        self.description = description
        self.valuation = valuation
        self.time = ""
        self.modify=""

    def __repr__(self) -> str:
        buff = f"Name : {self.name} \nAutor : {self.autor} \nType : {self.type} \n"
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
    
    def change_autor(self, new_autor:str) -> None:
        self.autor = new_autor

    def change_name(self, new_name:str) -> None:
        self.name = new_name
    
    def change_description(self, new_text:str) -> None:
        self.description = new_text

    def change_valuation(self, new_value:float) -> None:
        if 10 >= new_value >= 0:
            self.valuation = new_value

class MangaLib:
    def __init__(self) -> None:
        self.list_manga = [Manga()]
        self.list_manga.pop()
    
    def __repr__(self) -> str:
        buff = ""
        for elt in self.list_manga:
            buff += elt.__repr__()
        return buff

    def add_manga(self, manga:Manga) -> None:
        buff_manga=Manga(manga.name, manga.autor, manga.type, manga.volume_number, manga.description, manga.valuation)
        now=datetime.datetime.now()
        buff_manga.time = "{}-{}-{} {}:{}:{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.list_manga.append(buff_manga)
    
    def modify_manga(self, manga:Manga, index:int) -> None:
        self.list_manga[index].change_name(manga.name)
        self.list_manga[index].change_autor(manga.autor)
        self.list_manga[index].change_type(manga.type)
        self.list_manga[index].change_volume_number(manga.volume_number)
        self.list_manga[index].change_description(manga.description)
        self.list_manga[index].change_valuation(manga.valuation)

    def del_manga(self, name="", autor="", type="", index="") -> None:
        if re.match("^[0-9]+$", str(index)) is not None:
            self.list_manga.pop(index)
        else:
            generator = self.find_manga(name,autor,type)
            for elt in generator:
                    print(elt)
                    if input("Is the good one ?y/n\n").upper()=="Y":
                        self.list_manga.remove(elt)
                        generator.close()
        
    def find_manga(self, name:str, autor="", type="") -> Manga:
        for elt in self.list_manga:
            if elt.name == name:
                if elt.autor == autor: 
                    if elt.type == type:
                        yield elt
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
            case "autor":
                self.list_manga.sort(key=lambda Manga: Manga.autor)
            case "valuation":
                self.list_manga.sort(key=lambda Manga: Manga.valuation)
    
    def get(self):
        return self.list_manga

    def save_data(self):
        with open("data","wb") as file:
            pickler = pickle.Pickler(file)
            pickler.dump(self.list_manga)
    
    def backup(self):
        with open("data","rb") as file:
            unpickler = pickle.Unpickler(file)
            self.list_manga = unpickler.load()

class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Manga Library")

        self.library = MangaLib()
        self.library.add_manga(Manga("test","test","test",1,"test",1))
        self.library.add_manga(Manga("test1","test1","test1",1,"test1",1))
        self.library.add_manga(Manga("test2","test2","test2",1,"test2",1))
        self.display_library()
    
    def set_geometry(self, width:int, height:int):
        self.geometry(f"{width}x{height}")

    def display_menu(self):
        self.clear()
        
        self.set_geometry(200,300)


    def display_library(self):
        self.clear()
        self.set_geometry(950,250)
        self.create_tab(self)
        
        modification_B = tk.Button(self,text="New Manga", relief="raised",command=self.display_modification)
        modification_B.pack(side="bottom")
    
    def display_modification(self, index=""):
        self.clear()
        
        self.set_geometry(300,200 + 50 * (re.match("^[0-9]+$", str(index))!=None))

        # création d'une frame top pour l'agencement des labels/Entry et des boutons 
        frame_top = tk.Frame(self)
        frame_top.pack(side="top")

        # création d'une frame colonne pour l'alignement
        frame_column = tk.Frame(frame_top)
        frame_column.pack(side="left", fill="x")

        # Création des labels
        for key in Manga().__dict__:

            frame_label = tk.Frame(frame_column)
            frame_label.pack(side="top", anchor="center")
            
            if key != "time" and key != "modify":
                label = tk.Label(frame_label, text=f"{key} :", justify=tk.LEFT)
                label.pack(side="left")
        
        # création d'une frame colonne pour l'alignement 
        frame_column = tk.Frame(frame_top)
        frame_column.pack(side="left", fill="x") 

        # Créations des inputs(Entry)
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

                case "autor":
                    buff_autor = tk.StringVar(self)
                    if re.match("^[0-9]+$", str(index)):
                        buff_autor.set(self.library.get()[index].autor)
                    self.autor_entry = tk.Entry(frame_column, textvariable=buff_autor, justify=tk.LEFT)
                    self.autor_entry.pack(side="top")

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

        # création d'une frame bottom pour l'agencement des labels/Entry et des boutons 
        frame_bottom = tk.Frame(self)
        frame_bottom.pack(side="top")

        # Création du bouton d'ajout du manga(ajout ou modification)
        add_button = tk.Button(frame_bottom, width=5,text="Add", command=lambda: self.modification(index))
        add_button.pack(side="top")

        # Affichage du bouton delete si c'est une modification d'un élément
        if re.match("^[0-9]+$", str(index)) is not None:
            del_button = tk.Button(frame_bottom, width=5, text="Delete", command=lambda index=index: self.delete_manga(index))
            del_button.pack(side="top", pady=10)
        
        # Bouton de retour au tableau
        back_button = tk.Button(frame_bottom, width=5, text="Return", command=self.display_library)
        back_button.pack(side="top")

    def modification(self, index=""):
        # récupération des données des Entry
        name_get = self.name_entry.get()
        autor_get = self.autor_entry.get()
        type_get = self.type_entry.get()
        volume_nb_get = self.volume_nb_entry.get()
        description_get = self.description_entry.get()
        valuation_get = self.valuation_entry.get()

        # vérification des données d'entrée
        data_verify = True
        # si @name_get, @autor_et, @type_get et @description_get 
        # ne possède que des lettres ou chiffres
        if re.match("^[a-zA-Z0-9 ,.]+$",name_get) is None:
            data_verify = False
        if re.match("^[a-zA-Z0-9 ,.]+$",autor_get) is None:
            data_verify = False
        if re.match("^[a-zA-Z0-9 ,.]+$",type_get) is None:
            data_verify = False
        if re.match("^[a-zA-Z0-9 ,.]+$",description_get) is None:
            data_verify = False
        # si @volume_nb_get, @valuation_get
        # ne possède que des chiffres ou "."
        if re.match("^[0-9.]+$",volume_nb_get) is None:
            data_verify = False
        if re.match("^[0-9.]+$",valuation_get) is None:
            data_verify = False

        if data_verify:
            # Si un index a été donné
            if re.match("^[0-9]+$", str(index)):
                # modification du manga de rang @index
                self.library.modify_manga(Manga(name_get, autor_get, type_get, int(volume_nb_get), description_get, float(valuation_get)),index)
            # sinon index==""
            else:
                # ajout du manga à la bibliothèque
                self.library.add_manga(Manga(name_get, autor_get, type_get, volume_nb_get, description_get, valuation_get))
            
            # affichage de notre bibliothèque
            self.display_library()
            
    def create_tab(self, root_frame:tk.Frame, align_side="top"):
        # Frame général pour l'affichage du tableau
        frame_tab = tk.Frame(root_frame)
        frame_tab.pack(side=align_side)
        
        
        for key in Manga().__dict__:

            # Création des colonnes pour l'agencement et l'alignement des éléments
            frame_column = tk.Frame(frame_tab)
            frame_column.pack(side="left")
            
            # création de la frame case pour les entêtes
            frame_case = tk.Frame(frame_column,  height=1)
            frame_case.pack(side="top")

            # gestion des cas particuliers à cause du type et de la taille
            match key:
                case "description":
                    text = tk.Label(frame_case, text=key, width=20, height=1, borderwidth=2, relief="solid")
                    text.pack()
                case "modify":
                    # Création d'un bouton invisible 
                    # pour l'alignement avec les lignes du tableau
                    button = tk.Button(frame_case, text="", relief="flat")
                    button.pack(anchor="center")
                case _:
                    text = tk.Label(frame_case, text=key, width=15, height=1, borderwidth=2, relief="solid")
                    text.pack()
            
            # index de repérage dans le balayge
            index = 0
            # Création des cases avec les données en fonction de  @key
            # balayge de mangas enregistrés
            for elt in self.library.get():
                
                # Création de la cases pour la gestion d'affichage
                frame_case = tk.Frame(frame_column)
                frame_case.pack(fill="both", anchor="center")

                # gestion de cas particuliers à cause du type ou de la taille
                match key:
                        case "volume_number":
                            text = tk.Label(frame_case, text=elt.__dict__[key], width=15, height=4, borderwidth=2, relief="solid")
                            text.pack()
                        case "description":
                            text = tk.Label(frame_case, text=elt.__dict__[key], width=20, height=4, borderwidth=2, relief="solid")
                            text.pack()
                        case "modify":
                            button = tk.Button(frame_case, text="modify", command=lambda i=index: self.display_modification(i))
                            button.pack(pady=20, anchor="center")
                        case _:
                            text = tk.Label(frame_case, text=elt.__dict__[key], width=15, height=4, borderwidth=2, relief="solid")
                            text.pack()
                index += 1
    
    def delete_manga(self, index:int):
        self.library.del_manga(index=index)
        self.display_library()

    def clear(self):
        for widget in self.winfo_children():
            widget.pack_forget()