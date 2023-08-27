from modules.Book import Book
from tkinter import messagebox
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

    def get_all(self, cmd: str = "", param: tuple = ()):
        """
        Retrieve all records from the database based on a provided SQL query and parameters.

        Args:
            cmd (str): The additional SQL query to be appended (e.g., "WHERE title=?").
            param (tuple): The parameters to be used in the SQL query.

        Returns:
            list: A list of fetched records.
        """
        try:
            query = self.cursor.execute(f"SELECT * FROM books {cmd}", param)
            return query.fetchall()
        except Exception:
            return []
    
    def get_many(self, start:int, limit:int):
        query = self.cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?",(limit,start))
        return query.fetchall()
    
    def get_by_title(self, title:str):
        query = self.cursor.execute("SELECT * FROM books WHERE title=?",(title,))
        return query.fetchall()
    
    def get_by_author(self, author:str):
        query = self.cursor.execute("SELECT * FROM books WHERE author=?",(author,))
        return query.fetchall()
    
    def get_by_type(self, type:str):
        query = self.cursor.execute("SELECT * FROM books WHERE type=?",(type,))
        return query.fetchall()
    
    def get_by_id(self, id:str):
        query = self.cursor.execute("SELECT * FROM books WHERE id=?",(id,))
        return query.fetchall()

    def get_elt(self, book:Book):
        query = self.cursor.execute("SELECT * FROM books WHERE title=? AND author=? AND type=? AND tome=?", (book.title, book.author, book.type, book.tome))
        return query.fetchone()
    
    def get_sort_by(self, key_sort:str, reverse:bool):
        if not reverse:
            match key_sort:
                case "id":
                    return self.cursor.execute("SELECT * FROM books ORDER BY id")
                case "title":
                    return self.cursor.execute("SELECT * FROM books ORDER BY title")
                case "author":
                    return self.cursor.execute("SELECT * FROM books ORDER BY author")
                case "type":
                    return self.cursor.execute("SELECT * FROM books ORDER BY type")
                case "tome":
                    return self.cursor.execute("SELECT * FROM books ORDER BY tome")


    def is_in(self, book:Book) -> bool:
        """ verify if the given book is in the list """
        query = self.cursor.execute("SELECT * FROM books WHERE title=? AND author=? AND type=? AND tome=?", (book.title, book.author, book.type, book.tome))
        return query.fetchall() != []
    
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