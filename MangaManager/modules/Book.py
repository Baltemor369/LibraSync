

from typing import Any


class Book:
    def __init__(self, title="",  author="", type="", tome=0) -> None:
        self.title = title
        self.author = author
        self.type = type
        self.tome = tome

    def __eq__(self, __o: object) -> bool:
        check = True
        if self.title != __o.title :
            check = False
        if self.author != __o.author :
            check = False
        if self.tome != __o.tome:
            check = False
        return check

    def modify(self, new_title:str="", new_author:str="", new_type:str="", new_volume:int=-1) -> None:
        if new_title: 
            self.title = new_title
        if new_author:
            self.author = new_author
        if new_type:
            self.type = new_type
        if new_volume!=-1:
            self.tome = new_volume
        