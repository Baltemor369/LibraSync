class Book:
    def __init__(self, ref:str, name:str="", author:str="", read_status:bool=False, family:list[str]=[]) -> None:
        self.ref = ref
        self.name = name
        self.author = author
        self.read_status = bool(read_status)
        self.family = family

    def info(self):
        return self.ref + " " + self.name + " " + self.author + " " + self.family