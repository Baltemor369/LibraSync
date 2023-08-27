import re
from modules.const import PATTERNTOME

def tome_str_to_int(text:str) -> list[int]:
    result:list[int] = []
    if re.match(PATTERNTOME, text):
        text = text.split(",")
        for elt in text:
            try:
                result.append(int(elt))
            except ValueError:
                tmp = elt.split("-")
                try:
                    start = int(tmp[0])
                    end = int(tmp[1])+1
                    if start < end:
                        for i in range(start, end):
                            result.append(i)
                    else:
                        return []
                except ValueError:
                    return []
        return result