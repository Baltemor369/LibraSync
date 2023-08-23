from modules.Book import Book
from tkinter import messagebox
import sqlite3 as sql

class Library:
    def __init__(self, all_book:list[Book]=[], path:str="data/data.db") -> None:
        self.book_lib:list[Book] = all_book.copy()
        self.sort_by:str = "title"
        self.reverse:bool = False
        self.path:str = path

        self.init_sql()

    def is_in(self, given_book:Book) -> bool:
        """ verify if the given book is in the list """
        for book in self.book_lib:
            if book == given_book:
                return True
        return False
    
    def add_book(self, book:Book) -> bool:
        """add a book if it's not already in"""
        if not self.is_in(book):
            self.book_lib.append(book)
            return True
        return False
    
    def del_book(self,ID:int) -> bool:
        """erase a book from the list with the ID"""
        tmp = self.id_to_index(ID)
        if tmp > -1:
            self.book_lib.pop(tmp)
            return True
        # id not found in the list
        return False

    def modify_book(self, id:int, data:dict) -> bool:
        """Modify the attributs of the book found with the ID"""
        book_to_modify = self.id_to_book(id)
        if type(book_to_modify) == Book:
            for key,val in data.items():
                try:
                    if type(book_to_modify.get()[key]) == type(val):
                        book_to_modify.get()[key] = val
                except KeyError:
                    # key not found
                    return False
            # all modification done
            return True
        # book not found
        return False
        
    def find_title(self, title:str) -> list[Book]:
        """finds and return every books corresponding to the given title"""
        if title == "":
            return self.get_all_book()
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
            return self.get_all_book()
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
    
    def find_type(self, type:str) -> list[Book]:
        """finds and return every books corresponding to the given type"""
        if type == "":
            return self.get_all_book()
        else:
            result = []
            for elt in self.book_lib:
                if len(type)<=len(elt.type):
                    check_char = True
                    # check char by char
                    for char_type,char_elt in zip(type.lower(),elt.type.lower()):
                        if char_type != char_elt:
                            check_char = False
                    if check_char:
                        result.append(elt)
            return result
    
    def set_lib(self, new_lib:list[Book]) -> None:
        self.book_lib = new_lib.copy()
    
    def clear_lib(self) -> None:
        self.book_lib = []
    
    def book_to_id(self,book:Book) -> int:
        """
        return the id corresponding to the given book
        """
        for elt in self.get_all_book():
            if book == elt:
                return elt.id
        # book not found
        return -1

    def book_to_index(self,book:Book) -> int:
        """
        return the index corresponding to the given book
        """
        i = 0
        for elt in self.get_all_book():
            if book == elt:
                return i
            i+=1
        # book not found
        return -1

    def id_to_index(self, id:int) -> int:
        """
        return the index where the id appear in the list
        """
        for i,elt in enumerate(self.get_all_book()):
            if elt.id == id:
                return i
        # id not found
        return -1
    
    def id_to_book(self, ID:int=-1) -> Book|bool:
        """
        return the book corresponding to the given ID
        """
        if ID != -1:
            for book in self.book_lib:
                if book.id == ID:
                    return book
        return False

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
        return all book corresponding to the title, and author&type if given
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

    def get_all_book(self):
        """
        return all book saved in the list
        """
        return self.book_lib.copy()
    
    def get_all_titles(self) -> list[str]:
        """
        return all book's title without duplicate
        """
        buff = []
        for elt in self.get_all_book():
            buff.append(elt.title)
        return buff
    
    def get_all_authors(self) -> list[str]:
        """
        return all book's authors without duplicate
        """
        buff = []
        for elt in self.get_all_book():
            buff.append(elt.author)
        return buff
    
    def get_all_types(self) -> list[str]:
        """
        return all book's types without duplicate
        """
        buff = []
        for elt in self.get_all_book():
            buff.append(elt.type)
        return buff
    
    def get_all_id(self) -> list[int]:
        """
        return all id         
        """
        buff = []
        for elt in self.get_all_book():
            buff.append(elt.id)
        return buff
    
    def sort_book(self,sort_category="title") -> None:
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
        self.sort_book("ID_key")

        Id = 0
        for elt in self.get_all_id():
            if elt == Id:
                Id += 1
            else:
                return Id
        return Id

    def init_sql(self) -> bool:
        try:
            self.connection = sql.connect(self.path)
            self.cursor = self.connection.cursor()

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    type TEXT,
                    tome INTEGER
                    )
                    ''')
            self.conn.commit()
            return True
        except:
            return False
    
    def close(self) -> None:
        self.connection.close()
    
    def load_data(self) -> bool:
        try:    
            self.cursor.execute('''SELECT * FROM books''')
            data = self.cursor.fetchall()
            for elt in data:
                bk = Book(self.get_free_id(), elt[0], elt[2], elt[3], elt[4])
                self.add_book(bk)
            return True
        except:
            return False
    
    def add_data(self, data:list[Book]) -> bool:
        """
        Add manga data to the database based on a list of manga objects.

        Args:
            data (List[Book]): A list of manga objects to be added to the database.

        Returns:
            bool: Returns True if the data was successfully added, False otherwise.
        """
        try:
            for bk in data:
                self.cursor.execute(
                    "INSERT INTO books (id,title,author,type,tome) VALUES (?,?,?,?,?)",
                    (bk.id, bk.title, bk.author, bk.type, bk.tome)
                    )
                self.connection.commit()
            return True
        except (TypeError,ValueError) as e:
            messagebox.showerror("Error", f"An error occurred : {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred : {e}")
        return False

    def del_data(self, data:list[Book]|list[int]) -> None:
        """
        Delete mangas from the database based on either a list of manga objects or a list of IDs.

        Args:
            mangas_or_ids (List[Book] or List[int]): A list of manga objects or manga IDs to be deleted.

        Returns:
            None: This function doesn't return any value.
        """
        if isinstance(data[0],int):
            for elt in data:
                self.cursor.execute("DELETE FROM books WHERE id=?",(elt,))
        elif isinstance(data[0],Book):
            for elt in data:
                self.cursor.execute("DELETE FROM books WHERE title=? AND author=? AND type=? AND tome=?",(elt.title, elt.author, elt.type, elt.tome))
        else:
            messagebox.showerror("Error", f"An error occurred : no acceptable data given")
        self.connection.commit()
        