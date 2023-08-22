import datetime
import re
from modules.Book import Book


class Library:
    def __init__(self,all_manga:list[Book]=[]) -> None:
        self.book_lib:list[Book] = all_manga.copy()
        self.sort_by = "title"
        self.reverse = False

    def is_in(self, given_book:Book) -> bool:
        """ verify if the given manga is in the list """
        for book in self.book_lib:
            if book == given_book:
                return True
        return False
    
    def add_book(self, book:Book) -> None:
        """add a book if it's not already in"""
        if not self.is_in(book):
            self.book_lib.append(book) # adds the manga to the list
    
    def del_book(self,ID:int) -> None:
        """erase a book from the list with the ID"""
        try:
            self.book_lib.pop(self.id_to_index(ID))
        except:
            pass

    def modify_manga(self, id:int, data:dict) -> bool:
        """Modify the attributs of the book found with the ID"""
        try:
            book_to_modify = self.get_by_id(id)
            for key,val in data.items():
                if type(book_to_modify.get()[key]) == type(val):
                    book_to_modify.get()[key] = val
            return True
        except:
            return False
        
    def find_title(self, title:str) -> list[Book]:
        """finds and return every books corresponding to the given title"""
        if title == "":
            return self.get_all_manga()
        else:
            result = []
            for elt in self.book_lib:
                if len(title)<=len(elt.title):
                    check_char = True
                    # check char by char
                    for char_title,char_elt in zip(title.lower(),elt.title.lower()):
                        if char_title != char_elt:
                            check_char = False
                    if check_char:
                        result.append(elt)
            return result
    
    def find_author(self, author:str) -> list[Book]:
        """finds and return every books corresponding to the given title"""
        if author == "":
            return self.get_all_manga()
        else:
            result = []
            for elt in self.book_lib:
                if len(author)<=len(elt.author):
                    check_char = True
                    # check char by char
                    for char_title,char_elt in zip(author.lower(),elt.author.lower()):
                        if char_title != char_elt:
                            check_char = False
                    if check_char:
                        result.append(elt)
            return result
    
    def set_lib(self, new_lib:list[Book]) -> None:
        self.book_lib = new_lib.copy()
    
    def manga_to_id(self,manga:Book) -> int:
        """
        return the id corresponding to the given manga
        """
        for elt in self.get_all_manga():
            if manga == elt:
                return elt.id
        return -1

    def manga_to_index(self,manga:Book) -> int:
        """
        return the index corresponding to the given manga
        """
        i = 0
        for elt in self.get_all_manga():
            if manga == elt:
                return i
            i+=1
        return -1

    def id_to_index(self, id:int) -> int:
        """
        return the index where the id appear in the list
        """
        for i,elt in enumerate(self.get_all_manga()):
            if elt.id == id:
                return i
        return -1
    
    def id_to_manga(self, ID:int=-1) -> Book:
        """
        return the manga corresponding to the given ID
        """
        if ID != -1:
            for book in self.book_lib:
                if book.id == ID:
                    return book

    def get_all_titles(self) -> list[Book]:
        """
        return all the differents titles in the list
        """
        buffer = []
        buffer_title = []
        for elt in self.book_lib:
            if elt.title not in buffer_title:
                buffer.append(elt)
                buffer_title.append(elt.title)
        return buffer
    
    def get_compact_lib(self):
        """
        return a lib with only different title/author/type, volume are zip in one number(the higher from a collection)
        """
        buffer = []
        buffer_title = []
        for elt in self.book_lib:
            if elt.title not in buffer_title:
                buffer_title.append(elt.title)
                buffer.append(Book(elt.id, elt.title, elt.author, elt.type, len(self.get_collection(elt.title)), elt.description, elt.valuation, elt.time))
        return buffer
    
    def get_collection(self, titles:str, author:str="", type:str="") -> list[Book]:
        """
        return all manga corresponding to the title, and author&type if given
        """
        buffer = []
        for elt in self.book_lib:
            if elt.title == titles and (author == "" or elt.author == author) and (type == "" or elt.type == type):
                buffer.append(elt)
        return buffer

    def get_sample(self, index=0, interval=10) -> list[Book]:
        """Return a list of books from the given index to index + interval"""
        buffer = []
        
        if interval >= len(self.book_lib)-index:
            interval = len(self.book_lib)-index
        for i in range(index, index + interval):
            buffer.append(self.book_lib[i])
        return buffer

    def get_all_manga(self):
        """
        return all manga saved in the list
        """
        return self.book_lib.copy()
    
    def get_all_titles(self) -> list[str]:
        """
        return all manga's title without duplicate
        """
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.title)
        return buff
    
    def get_all_authors(self) -> list[str]:
        """
        return all manga's authors without duplicate
        """
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.author)
        return buff
    
    def get_all_types(self) -> list[str]:
        """
        return all manga's types without duplicate
        """
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.type)
        return buff
    
    def get_all_id(self) -> list[int]:
        """
        return all id         
        """
        buff = []
        for elt in self.get_all_manga():
            buff.append(elt.id)
        return buff
    
    def sort_manga(self,sort_category="title") -> None:
        match sort_category:
            case "title":
                self.book_lib.sort(key=lambda Book: Book.title, reverse=self.reverse) 
            case "type":
                self.book_lib.sort(key=lambda Book: Book.type, reverse=self.reverse)
            case "volume_number":
                self.book_lib.sort(key=lambda Book: Book.volume_number, reverse=self.reverse)
            case "author":
                self.book_lib.sort(key=lambda Book: Book.author, reverse=self.reverse)
            case "ID_key":
                self.book_lib.sort(key=lambda Book: Book.id, reverse=self.reverse)            

    def get_free_id(self):
        self.sort_manga("ID_key")

        Id = 0
        for elt in self.get_all_id():
            if elt == Id:
                Id += 1
            else:
                return Id
        return Id