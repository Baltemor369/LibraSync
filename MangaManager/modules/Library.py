from modules.Book import Book
from modules.const import HEADERS
from modules.search_str_to_dict import search_str_to_dict
import re
import sqlite3 as sql

class Library:
    def __init__(self) -> None:
        self.connection = sql.connect("data/data.db")
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
        self.connection.commit()

        self.key_priority = HEADERS.copy()
        for elt in self.key_priority:
            elt = elt.lower()
        self.reverse = False

    def get_all(self):
        query = self.cursor.execute("SELECT * FROM books")
        return query.fetchall()

    def get(self, start:int, limit:int, text:str=""):
        # param check in
        try:
            start = int(start)
            limit = int(limit)
        except ValueError:
            return []    
        
        request = "SELECT * FROM books"

        reverse = " DESC" if self.reverse else ""
        self.key_priority[0] += reverse
        key_tmp = ", ".join(self.key_priority)

        # WHERE
        if re.match("^[\w;: ]*$", text):
            buff = search_str_to_dict(text)
            if buff:
                request += " WHERE "
                i = 0
                for key,val in buff.items():
                    request += f"{key} LIKE '{val}%' "
                    if i < len(buff)-1:
                        request += "AND "
                    i += 1

        # ORDER BY
        request += " ORDER BY " + key_tmp

        # LIMIT OFFSET
        request += "  LIMIT " + str(limit) + " OFFSET " + str(start)
        query = self.cursor.execute(request)
        return query.fetchall()
    
    def get_key_sort(self):
        return self.key_priority[0]

    def is_in(self, book:Book) -> bool:
        query = self.cursor.execute("SELECT * FROM books WHERE title=? AND author=? AND type=? AND tome=?", (book.title, book.author, book.type, book.tome))
        return query.fetchall() != []

    def set_sort_order(self, key:str):
        if key in HEADERS:
            # put the key in the first position and keep the original order of other key
            self.key_priority = HEADERS.copy()
            self.key_priority.remove(key)
            self.key_priority.insert(0, key)
            
            for elt in self.key_priority:
                elt = elt.lower()

    def set_reverse(self, val:bool):
        if val==True or val==False:
            self.reverse = val
    
    def add_books(self, data: list[Book]) -> bool:
        """
        Add multiple books to the database, ignoring duplicates.

        Args:
            data (list[Book]): A list of Book objects to be added.

        Returns:
            bool: True if all books were added successfully, False if there was an error.
        """
        try:
            for book in data:
                if isinstance(book, Book):
                    if not self.is_in(book):
                        self.cursor.execute(
                            "INSERT INTO books(title, author, type, tome) VALUES (?,?,?,?)",
                            (book.title, book.author, book.type, book.tome))
                else:
                    return False  # Invalid data type in the list
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            return False
    

    def delete_book(self, data: list[Book]) -> bool:
        """
        Delete a book from the database.

        Args:
            data (list[Book]): A list of Book objects to be deleted.

        Returns:
            bool: True if the books was deleted successfully, False if there was an error.
        """
        try:
            for book in data:
                if isinstance(book, Book):
                    if self.is_in(book):
                        self.cursor.execute(
                            "DELETE FROM books WHERE title=? AND author=? AND type=? AND tome=?",
                            (book.title, book.author, book.type, book.tome)
                        )
                    else:
                        return False
                else:
                    return False  # Invalid data type
            self.connection.commit()
            return True
        except Exception:
            self.connection.rollback()
            return False

    def update_book(self, old_book: Book, new_book: Book) -> bool:
        """
        Update a book's information in the database.

        Args:
            old_book (Book): The existing Book object to be updated.
            new_book (Book): The new Book object with updated information.

        Returns:
            bool: True if the book was updated successfully, False if there was an error.
        """
        try:
            if isinstance(old_book, Book) and isinstance(new_book, Book):
                if self.is_in(old_book):
                    self.cursor.execute(
                        "UPDATE books SET title=?, author=?, type=?, tome=? WHERE title=? AND author=? AND type=? AND tome=?",
                        (new_book.title, new_book.author, new_book.type, new_book.tome,
                        old_book.title, old_book.author, old_book.type, old_book.tome)
                    )
                    self.connection.commit()
                    return True
                else:
                    return False
            else:
                return False  # Invalid data types
        except Exception:
            self.connection.rollback()
            return False

    def close(self):
        self.connection.close()