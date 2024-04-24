from book import Book
import json
import csv

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

    def select(self, start:int=0, count:int=1, where:dict={}):
        selection:list[Book] = []
        for book in self.list_books[start:]:
            # verify : value empty = True || value == book.value = True || value can be found in book.value = True (like book ~= book1)
            try:
                if all(getattr(book, key) == value or value == "" or value.lower() in getattr(book, key).lower() for key, value in where.items()):
                    selection.append(book)
                    count -= 1
            except:
                if all(getattr(book, key) == value or value == "" or value.lower() in ' '.join(getattr(book, key)).lower() for key, value in where.items()):
                    selection.append(book)
                    count -= 1
            
            if count == 0:
                break
        return selection

    def saveFile(self, db:list[Book], file_name:str):
        try:
            with open(file_name, 'w') as file:
                for book in db:
                    families = [elt for elt in book.family]
                    file.write(f"${book.ref}-{book.name}-{book.author}-{book.read_status}-{families}\n")
            return True
        except:
            return False

    def loadFile(self, file_name:str):
        db:list[Book] = []
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    if line[0]=="$":
                        book = line[1:-1]
                        bookArgs = book.split("-")
                        bookArgs[-2] = bookArgs[-2].lower() == "True"
                        bookArgs[-1] = eval(bookArgs[-1])
                        db.append(Book(*bookArgs))
            self.list_books = db.copy()
            return True
        except:
            return False
    
    def export_to_csv(self, tree, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tree["columns"])
            for child in tree.get_children(""):
                writer.writerow(tree.item(child, "values"))

    def export_to_json(tree, filename):
        data = []
        for child in tree.get_children(""):
            values = tree.item(child, "values")
            item = {col: value for col, value in zip(tree["columns"], values)}
            data.append(item)
        
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

lib = Library()
lib.loadFile("save.txt")