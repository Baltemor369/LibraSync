from src.book import Book
import sqlite3

class Library:
    def __init__(self, data:list[Book]=[]) -> None:
        self.list_books:list[Book] = data
    
    def isIn(self, book:Book)->bool:
        for elt in self.list_books:
            if elt.ref == book.ref:
                return True
        return False

    def addBook(self, book:Book)->bool:
        if not self.isIn(book):
            self.list_books.append(book)
            return True 
        return False
    
    def removeBook(self, ref:str):
        for elt in self.list_books:
            if elt.ref == ref:
                self.list_books.remove(elt)

    def getByRef(self, reference:str)-> Book|None:
        for elt in self.list_books:
            if elt.ref == reference:
                return elt
        return None
    
    def getByName(self, name:str)-> list[Book]:
        result:list[Book] = []
        for book in self.list_books:
            if book.name.capitalize() == name.capitalize():
                result.append(book)
        return result

    def select(self, start:int=0, count:int=-1, where:dict={}):
        selection:list[Book] = []
        for book in self.list_books[start:]:
            try:
                # verify : value empty = True || value == book.value = True || value in book.value = True 
                if all(getattr(book, key) == value or value == "" or value.lower() in getattr(book, key).lower() for key, value in where.items()):
                    selection.append(book)
                    count -= 1
            except Exception as e :
                print(e)
            
            if count == 0:
                break
        return selection
    
    def save_to_db(self, db_name: str):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        for book in self.list_books:
            cursor.execute('SELECT * FROM books WHERE ref = ?', (book.ref,))
            row = cursor.fetchone()
            if row is None:
                cursor.execute('''
                    INSERT INTO books (ref, name, author, tome, read_status, family)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (book.ref, book.name, book.author, book.tome, book.read_status, ','.join(book.family)))
            else:
                if (row[1], row[2], row[3], row[4], row[5]) != (book.name, book.author, book.tome, book.read_status, ','.join(book.family)):
                    cursor.execute('''
                        UPDATE books
                        SET name = ?, author = ?, tome = ?, read_status = ?, family = ?
                        WHERE ref = ?
                    ''', (book.name, book.author, book.tome, book.read_status, ','.join(book.family), book.ref))
        conn.commit()
        conn.close()

    def load_from_db(self, db_name: str):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT ref, name, author, tome, read_status, family FROM books')
        rows = cursor.fetchall()
        self.list_books = []
        for row in rows:
            ref, name, author, tome, read_status, family = row
            families = family.split(',') if family else []
            book = Book(ref, name, author, tome, read_status, families)
            self.list_books.append(book)
        conn.close()
    
    def init_db(self, db_name:str):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ref TEXT,
                name TEXT,
                author TEXT,
                tome INT,
                read_status BOOLEAN,
                family TEXT
            )
        ''')
        conn.close()