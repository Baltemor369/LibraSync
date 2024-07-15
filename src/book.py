class Book:
    def __init__(self, ref:str, name:str="", author:str="", tome:int=-1, family:str="", read_status:str="no") -> None:
        self.ref = ref
        self.name = name
        self.author = author
        self.tome = tome
        self.read_status = bool(read_status)
        self.family = family

    def __str__(self):
        return self.ref + " " + self.name + " " + self.author + " " + str(self.tome) + " " + self.family