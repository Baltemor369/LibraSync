import re

def search_str_to_dict(text:str):
    result = {}
    patterns = {
        "title": r"(?:[\w :;]+;)?title ?: ?([\w ]+)(?:;[\w ]+)?",
        "author": r"(?:[\w :;]+;)?author ?: ?([\w ]+)(?:;[\w ]+)?",
        "type": r"(?:[\w :;]+;)?type ?: ?([\w ]+)(?:;[\w ]+)?",
        "tome": r"(?:[\w :;]+;)?tome ?: ?([\d ]+)(?:;[\w ]+)?"
    }
    
    for key,val in patterns.items():
        match = re.match(val,text)
        if match:
            result[key] = match.group(1)
    if not result:
        result["title"] = text
    return result
