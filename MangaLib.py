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

class Manatheque:
    def __init__(self) -> None:
        self.biblio = [Manga()]
        self.biblio.pop()
    
    def __repr__(self) -> str:
        buff = ""
        for elt in self.biblio:
            buff += elt.__repr__()
        return buff

    def add_manga(self, manga:Manga) -> None:
        self.biblio.append(Manga(manga.name,manga.autor,manga.type,manga.tome_numero))
    
    def del_manga(self, name:str, autor="", type="") -> None:
        corresponding_manga = self.find_manga(name,autor,type)
        check = "N"
        while check.upper() != "Y":
            corresponding_manga = self.find_manga(name,autor,type)
            print(corresponding_manga)
            check = input("Is the good manga ? Y/N")
            if check.upper() == "Y":
                self.biblio.remove(corresponding_manga)
        
    def find_manga(self, name:str, autor="", type="") -> Manga:
        for elt in self.biblio:
            if elt.name == name:
                if elt.autor == autor: 
                    if elt.type == type:
                        yield elt
                yield elt