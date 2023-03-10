import datetime
import re
from typing import List
from Manga import Manga

# To do :
# + volume "1-4"=> du volume 1 au 4
# + faire alignement affichage statistique
# + développer module historique(moyenne par semaine/mois voir combien ont été ajout pendant une semaine donnée)
# + verifier que le dossier data existe (os .path.exists .makedirs)

"""
faire un executable : in cmd
- pyinstaller --name=mon_programme --onefile --windowed mon_programme.py
- pyinstaller mon_programme.spec

"""

FILE_PATH = "data/data.txt"
class MangaLib:
    def __init__(self,all_manga:List[Manga]=[]) -> None:
        self.list_manga:List[Manga] = all_manga.copy()

    def __repr__(self) -> str:
        buff = ""
        for elt in self.list_manga:
            buff += elt.__repr__() +"\n"
        return buff

    def add_manga(self, manga:Manga) -> None:
        self.list_manga.append(manga) # adds the manga to the list
    
    def del_manga(self,ID=-1) -> None:
        if 0 <= ID < len(self.get()):
            self.list_manga.pop(self.get_index(ID))

    def modify_manga(self, manga:Manga, id:int) -> None:
        #recherche de l'index avec id
        index = self.get_index(id)
        self.list_manga[index].change_name(manga.name)
        self.list_manga[index].change_author(manga.author)
        self.list_manga[index].change_type(manga.type)
        self.list_manga[index].change_volume_number(manga.volume_number)
        self.list_manga[index].change_description(manga.description)
        self.list_manga[index].change_valuation(manga.valuation)    
        
    def find_manga(self, name:str) -> List[Manga]:
        if name=="":
            return self.get()
        else:
            result = []
            for elt in self.list_manga:
                if len(name)<=len(elt.name):
                    check_char = True
                    for char_name,char_elt in zip(name.lower(),elt.name.lower()):
                        if char_name != char_elt:
                            check_char = False
                    if check_char:
                        result.append(elt)
            return result
    
    def set_mangas(self, mangas:List[Manga]) -> None:
        self.list_manga = mangas

    # return a copy of all mangas
    def get(self) -> List[Manga]:
        return self.list_manga.copy()

    # return the manga's @id of @manga
    def get_id(self,manga:Manga) -> int:
        for elt in self.get():
            if manga == elt:
                return elt.Primary_key
        return -1 # code error

    # return the manga's index by id research
    def get_index(self, id:int) -> int:
        for i,elt in enumerate(self.get()):
            if elt.Primary_key == id:
                return i
        return -1 # code error
    
    # return a manga depends on a id or index given
    def get_manga(self, id:int=-1, index:int=-1):
        if id != -1:
            for elt in self.get():
                if elt.Primary_key == id:
                    return elt
        elif index != -1:
            return self.get()[index]
        else:
            return -1 # code error
                  
    # sort the list of mangas by a sort_key @sort_category and a order @reverse
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
            case "ID":
                self.list_manga.sort(key=lambda Manga: Manga.Primary_key, reverse=reverse)
    
    # return a list of all names
    def get_all_names(self) -> List[str]:
        buff = []
        for elt in self.get():
            buff.append(elt.name)
        return buff
    
    # return a list of all authors
    def get_all_authors(self) -> List[str]:
        buff = []
        for elt in self.get():
            buff.append(elt.author)
        return buff
    
    # return a list of all types
    def get_all_types(self) -> List[str]:
        buff = []
        for elt in self.get():
            buff.append(elt.type)
        return buff
    
    # return a list of all valuations
    def get_all_valuations(self) -> List[float]:
        buff = []
        for elt in self.get():
            buff.append(elt.valuation)
        return buff
    
    def get_all_id(self) -> List[int]:
        buff = []
        for elt in self.get():
            buff.append(elt.Primary_key)
        return buff

    # Function to save the datas in a file
    def save_data(self) -> None:
        with open(FILE_PATH,"w") as file:
            self.sort_manga("name")
            for i,elt in enumerate(self.get()):
                elt.time = elt.time.replace(microsecond=0)
                file.write(f"@#ID-{str(elt.Primary_key)}#N-{str(elt.name)}#A-{str(elt.author)}#TY-{str(elt.type)}#VN-{str(elt.volume_number)}#D-{str(elt.description)}#VA-{str(elt.valuation)}#TI-{str(elt.time)}#@\n")
    
    # Function to retrieve the datas saved
    def backup(self) -> None:
        self.read_file(FILE_PATH)

    def read_file(self, file_name:str):
        list_mangas = []
        with open(file_name,"r") as file:
            while 1:
                buffer = file.readline()
                if buffer != "":
                    list_mangas.append(buffer)
                else:
                    break
        self.convert_data(list_mangas)

    def convert_data(self, mangas:List[str]):
        id_r = r"#ID-(\d+)#"
        name_r = r"#N-([\w,\.\- ^_]+)#"
        author_r = r"#A-([\w,\.\- ^_]+)#"
        type_r = r"#TY-([\w,\.\- ^_]+)#"
        volume_nb_r = r"#VN-(\d{1,3})#"
        description_r = r"#D-([\w ,\.\-^_]+)#"
        valuation_r = r"#VA-(10(?:\.0)?|\d(?:\.\d)?)#"
        time_r = r"#TI-(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})#"

        format_string = "%Y-%m-%d %H:%M:%S"
        
        for elt in mangas:
            ID = re.search(id_r,elt).group(1)
            name = re.search(name_r,elt).group(1)
            author = re.search(author_r,elt).group(1)
            type = re.search(type_r,elt).group(1)
            volume_nb = re.search(volume_nb_r,elt).group(1)
            description = re.search(description_r,elt).group(1)
            valuation = re.search(valuation_r,elt).group(1)
            time = re.search(time_r,elt).group(1)
            time = datetime.datetime.strptime(time,format_string)

            self.add_manga(Manga(int(ID), name, author, type, int(volume_nb), description, float(valuation), time))
    
    def get_new_id(self):
        self.sort_manga("ID")

        ID = 0
        for elt in self.get():
            if elt.Primary_key == ID:
                ID += 1
            else:
                return ID
        return ID