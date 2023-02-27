import datetime, tkinter as tk

class Manga:
    def __init__(self, name="",  creator="", type="", volume_nb=0) -> None:
        self.name = name
        self.autor = creator
        self.type = type
        self.volume_number = volume_nb
        # un dictionnaire dans lequel on peut ajouter toutes données connaissable apres l'initialisation comme l'heure d'ajout à la manga library 
        self.data={}

    def __repr__(self) -> str:
        buff = f"Name : {self.name} \nAutor : {self.autor} \nType : {self.type} \nNumber of volume : {self.volume_number} \n"
        for key in self.data:
            buff += str(key)+" : "+self.data[key]+"\n"
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
    
    def add_attr(self, key:str, value:str) -> None:
        self.data[key] = value

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
        buff_manga.add_attr("time","{}-{}-{} {}:{}:{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second))
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
                self.list_manga.sort(key=lambda Manga: Manga.data["time"])
            case "type":
                self.list_manga.sort(key=lambda Manga: Manga.type)
            case "volume number":
                self.list_manga.sort(key=lambda Manga: Manga.volume_number)
            case "autor":
                self.list_manga.sort(key=lambda Manga: Manga.autor)
    
    def get(self):
        return self.list_manga
    
class UI(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title("Manga Library")

        self.mangalibrary = MangaLib()

    def display_library(self):
        # faire un tableau : nom, auteur, type, numero de tome, date d'ajout
        pass