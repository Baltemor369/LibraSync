import tkinter

def set_geometry(self:tkinter.Tk|tkinter.Toplevel, width:int=0, height:int=0, marginEW:int=100, marginNS:int=20, center:bool=True):
    """resize and center the window"""
    self.update_idletasks()
    if width == 0:
        width = self.winfo_reqwidth() + marginEW  # margin Est-West
    if height == 0:
        height = self.winfo_reqheight() + marginNS  # margin North-South

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
        

def popup(self:tkinter.Tk|tkinter.Frame, text:str|list|dict, title:str="Alert", bg:str="#333333", fg:str="#FFFFFF", font=("Helvetica",20), allow_editing:bool=False):
    """
    generate a pop up with a Label
    """
    popup = tkinter.Toplevel(self, bg=bg)
    popup.title(title)
    popup.focus()
    # key bind to escape quickly the window
    popup.bind("<Return>", lambda e: popup.destroy())
    popup.bind("<Escape>", lambda e: popup.destroy())

    # Alert only
    if str == type(text):
        label = tkinter.Label(popup, text=text, bg=bg, fg=fg, font=font)
        label.pack(pady=10)
    
    elif list == type(text):
        for line in text:
            rowFrame = tkinter.Frame(popup, bg=bg)
            rowFrame.pack()

            label = tkinter.Label(rowFrame, text=line, bg=bg, fg=fg, font=font)
            label.pack()
    
    # display more data like a table
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
            if allow_editing:
                label = tkinter.Entry(frame, bg="#555555", fg=fg, font=font)
                label.insert(0, val)
            else:
                 label = tkinter.Label(frame, text=val, bg="#555555", fg=fg, font=font)
            label.pack()

    set_geometry(popup)

# not tested yet
#def adjust_cell_sizes(data:list[list[str]], tab_to_adjust:list[list[tkinter.Label]]):
#    """adjust the size of the cases depending on the text inside"""
#    for row in range(len(data)):
#        for col in range(len(data[row])):
#            cell = tab_to_adjust[row][col]
#            cell.config(width=len(data[row][col]))
#            cell.grid(row=row, column=col)
