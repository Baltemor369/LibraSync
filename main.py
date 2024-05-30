from src.interface import *
import os

if not os.path.exists("data"):
    os.mkdir("data")

if __name__ == "__main__":
    Interface()

# reminds 
# self.value = tk.StringVar(value="Yes")  # Valeur par défaut
# self.combobox = ttk.Combobox(self, textvariable=self.value, values=["Yes", "No"])
# self.combobox.pack(fill="x", padx=5, pady=5)
# self.value.get()  