import datetime, tkinter as tk, tkinter.ttk as tkk,pickle

class Manga:
    def __init__(self, name="",  creator="", type="", volume_nb=0) -> None:
        self.name = name
        self.autor = creator
        self.type = type
        self.volume_number = volume_nb
        self.time = ""
        self.description = ""
        self.valuation = 0.0

    def __repr__(self) -> str:
        buff = f"Name : {self.name} \nAutor : {self.autor} \nType : {self.type} \n"
        buff += f"Number of volume : {self.volume_number} \nDescription : {self.description} \n"
        buff += f"Valuation : {self.valuation}/10 \nTime : {self.time} \n"
        buff += "\n"
        return buff

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
        buff_manga=Manga(manga.name,manga.autor,manga.type,manga.volume_number)
        now=datetime.datetime.now()
        buff_manga.time = "{}-{}-{} {}:{}:{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.list_manga.append(buff_manga)
    
    def del_manga(self, name:str, autor="", type="") -> None:
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

    def get_manga_attr(self):
        return Manga().__dict__()
    
class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Manga Library")

        self.mangalibrary = MangaLib()

    def create_case(self, root_frame:tk.Frame, text="", bordertype="solid"):
        label = tk.Label(root_frame, text=text,borderwidth=2, relief=bordertype)
        return label

    def create_ligne(self, root_frame:tk.Frame, nb_case=1, text="", bordertype="solid"):
        frame = tk.Frame(root_frame)
        for i in range(nb_case):
            self.create_case(frame,text,bordertype)
    
    # il faut continuer ici ▼
    def create_tab(self, root_frame:tk.Frame, columns=):
        

    def display_library(self):
        # faire un tableau : nom, auteur, type, numero de tome, date d'ajout
        self.frame_manga = tk.Frame(self)
    