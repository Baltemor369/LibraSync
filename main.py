from src.interface import *
from src.const import *
from src.googleDrive import GoogleAuth

if __name__ == "__main__":
    auth = GoogleAuth()
    if auth.authentification():
        print(f"Google authentification successful")
        if auth.load:
            Interface()
            auth.save()