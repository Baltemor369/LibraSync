class Manga:
    def __init__(self, name="",  creator="", type="", tome_nb=0) -> None:
        self.name = name
        self.autor = creator
        self.type = type
        self.tome_numero = tome_nb

    def __repr__(self) -> str:
        return f"Name : {self.name} \nAutor : {self.autor} \nType : {self.type} \nNumber of tome : {self.tome_numero} \n\n"

    def change_tome_numero(self, new_value:int) -> None:
        self.tome_numero = new_value
    
    def change_type(self, new_type:str) -> None:
        self.type = new_type
    
    def change_autor(self, new_autor:str) -> None:
        self.autor = new_autor

    def change_name(self, new_name:str) -> None:
        self.name = new_name

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
        self.list_manga.append(Manga(manga.name,manga.autor,manga.type,manga.tome_numero))
    
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

    def sort_MangaLib(self,sort_category="name"):
        match sort_category:
            case "name":
                self.list_manga.sort(key=lambda Manga: Manga.name)
