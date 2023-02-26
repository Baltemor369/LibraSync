import datetime

class Manga:
    def __init__(self, name="",  creator="", type="", tome_nb=0) -> None:
        self.name = name
        self.autor = creator
        self.type = type
        self.tome_numero = tome_nb
        self.data={}

    def __repr__(self) -> str:
        buff = f"Name : {self.name} \nAutor : {self.autor} \nType : {self.type} \nNumber of tome : {self.tome_numero} \n"
        for key in self.data:
            buff += str(key)+" : "+self.data[key]+"\n"
        buff += "\n"
        return buff

    def change_tome_numero(self, new_value:int) -> None:
        self.tome_numero = new_value
    
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
        buff_manga=Manga(manga.name,manga.autor,manga.type,manga.tome_numero)
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
    
    def get(self):
        return self.list_manga