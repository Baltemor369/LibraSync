import random as rd
from Manga import Manga

LETTER = "azertyuiopmlkjhfdsqwxcvbn"

def random_manga(ID:int):
    name = ""
    for i in range(rd.randrange(10)):
        name += rd.choice(LETTER)
    
    author = ""
    for i in range(rd.randrange(10)):
        name += rd.choice(LETTER)
    
    type = ""
    for i in range(rd.randrange(10)):
        name += rd.choice(LETTER)
    
    volume_number = int(rd.randrange(100))
    
    valuation = float(rd.randrange(10))
        
    return Manga(ID,str(name),str(author),str(type),volume_number,"None",valuation)