class Book:
    def __init__(self, ref:str, name:str="", author:str="", tome:int=-1, read_status:str="no", family:list[str]=[]) -> None:
        self.ref = ref
        self.name = name
        self.author = author
        self.tome = tome
        self.read_status = bool(read_status)
        self.family = family

    def info(self):
        return self.ref + " " + self.name + " " + self.author + " " + str(self.tome) + " ".join(self.family)