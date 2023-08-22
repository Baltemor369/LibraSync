import tkinter

def set_geometry(self:tkinter.Tk|tkinter.Toplevel, margin_EW:int=100, margin_NS:int=20, center:bool=True):
    """resize and center the window"""
    self.update_idletasks()
    width = self.winfo_reqwidth() + margin_EW  # margin E-W
    height = self.winfo_reqheight() + margin_NS  # margin N-S

    x = (self.winfo_screenwidth() // 2) - (width // 2)
    y = (self.winfo_screenheight() // 2) - (height // 2)
    if center:
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    else:
        self.geometry('{}x{}'.format(width, height))

def clear(self:tkinter.Tk|tkinter.Frame):
    """destroy all widget in the given window"""
    for widget in self.winfo_children():
            widget.destroy()

def undisplay(self:tkinter.Tk|tkinter.Frame):
     """undisplay all widget in the given window without destroy it"""
     for widget in self.winfo_children():
            widget.pack_forget()
        

def popup(self:tkinter.Tk|tkinter.Frame, text:str|dict, title:str="Alert", bg:str="#333333", fg:str="#FFFFFF", font=("Helvetica",20)):
    """
    generate a pop up with a Label
    """
    popup = tkinter.Toplevel(self, bg=bg)
    popup.title(title)
    popup.focus()
    popup.bind("<Return>", lambda e: popup.destroy())
    popup.bind("<Escape>", lambda e: popup.destroy())
    if str == type(text):
        label = tkinter.Label(popup, text=text, bg=bg, fg=fg, font=font)
        label.pack(pady=10)
    elif dict == type(text):
        Lframe = tkinter.Frame(popup, bg=bg)
        Lframe.pack(side="left", fill="both",expand=True)
        Rframe = tkinter.Frame(popup, bg=bg)
        Rframe.pack(side="right", fill="both",expand=True)

        for key,val in text.items():
            frame = tkinter.Frame(Lframe, bg=bg)
            frame.pack(pady=5)

            label = tkinter.Label(frame, text=key, bg=bg, fg=fg, font=font)
            label.pack()

            frame = tkinter.Frame(Rframe, bg=bg)
            frame.pack(pady=5)

            label = tkinter.Entry(frame, bg="#555555", fg=fg, font=font)
            label.insert(0, val)
            label.pack()

    set_geometry(popup)


def adjust_cell_sizes(data:list[list[str]], tab_to_adjust:list[list[tkinter.Label]]):
    """adjust the size of the cases depending on the text inside"""
    for row in range(len(data)):
        for col in range(len(data[row])):
            cell = tab_to_adjust[row][col]
            cell.config(width=len(data[row][col]))
            cell.grid(row=row, column=col)