from src.interface import *
import os

if not os.path.exists("data"):
    os.mkdir("data")

if __name__ == "__main__":
    Interface()