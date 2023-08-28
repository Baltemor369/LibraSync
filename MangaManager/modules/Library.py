from modules.Book import Book
from modules.const import KEYORDER
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

        self.key_priority = KEYORDER
        self.reverse = False

    def get_all(self):
        """
        Retrieve all records from the database based on a provided SQL query and parameters.

        Args:
            cmd (str): The additional SQL query to be appended (e.g., "WHERE title=?").
            param (tuple): The parameters to be used in the SQL query.

        Returns:
            list: A list of fetched records.
        """
        try:
            key = ", ".join(self.key_priority)
            reverse = "DESC" if self.reverse else ""
            query = self.cursor.execute(f"SELECT * FROM books ORDER BY {key} {reverse}")
            return query.fetchall()
        except Exception:
            return []
    
    def get_many(self, start:int, limit:int):
        if self.reverse:
            reverse = " DESC" 
        else:
            reverse = ""
        self.key_priority[0] += reverse
        key = ", ".join(self.key_priority)
        request = f"SELECT * FROM books  ORDER BY {key}  LIMIT ? OFFSET ?"
        query = self.cursor.execute(request,(limit, start))
        return query.fetchall()
    
    def get_by_title(self, title:str):
        reverse = " DESC" if self.reverse else ""
        self.key_priority[0] += reverse
        key = ", ".join(self.key_priority)
        query = self.cursor.execute("SELECT * FROM books WHERE title=? ORDER BY ?",(title,key))
        return query.fetchall()
    
    def get_by_author(self, author:str):
        reverse = " DESC" if self.reverse else ""
        self.key_priority[0] += reverse
        key = ", ".join(self.key_priority)
        query = self.cursor.execute("SELECT * FROM books WHERE author=? ORDER BY ?",(author,key))
        return query.fetchall()
    
    def get_by_type(self, type:str):
        reverse = " DESC" if self.reverse else ""
        self.key_priority[0] += reverse
        key = ", ".join(self.key_priority)
        query = self.cursor.execute("SELECT * FROM books WHERE type=? ORDER BY ?",(type,key))
        return query.fetchall()
    
    def get_by_id(self, id:str):
        query = self.cursor.execute("SELECT * FROM books WHERE id=?",(id,))
        return query.fetchall()

    def get_elt(self, book:Book):
        query = self.cursor.execute("SELECT * FROM books WHERE title=? AND author=? AND type=? AND tome=?", (book.title, book.author, book.type, book.tome))
        return query.fetchone()
    
    def get_key_sort(self):
        return self.key_priority[0]

    def is_in(self, book:Book) -> bool:
        """ verify if the given book is in the list """
        query = self.cursor.execute("SELECT * FROM books WHERE title=? AND author=? AND type=? AND tome=?", (book.title, book.author, book.type, book.tome))
        return query.fetchall() != []

    def change_sort_order(self, key:str):
        if key in KEYORDER:
            # put the key in the first position and keep the original order of other key
            self.key_priority = KEYORDER.copy()
            self.key_priority.remove(key)
            self.key_priority.insert(0, key)
    
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