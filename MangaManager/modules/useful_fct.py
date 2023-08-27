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
    generate a pop up with a Label, to alert user of evenements or any important information
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


class PromptWindow:
    def __init__(self, root:tkinter.Tk, title:str="Window", labelsText:list[str]|tuple[str]=("Text : "), inputsInsert:list[str]|tuple[str]=(), windowConfig:dict={}, labelParam:dict={}, inputParam:dict={}, caseParam:dict={}, buttonParam:dict={}, margin:tuple=(20,20)) -> None:
        """
        A class to create a window with labeled inputs.
        Get the entry values in "self.values".
        Get the occured errors in "self.errorLog"

        Args:
            title (str): The title of the window. Defaults to "Window".
            labelsText (list[str]): List of labels for each input field. Defaults to ["Text : "].
            inputsInsert (list[str]): List of default insert values for each input field. Defaults to ["Text"].
            windowConfig (dict): Configuration parameters for the window. Defaults to {}.
            labelParam (dict): Configuration parameters for the Labels. Defaults to {}.
            inputParam (dict): Configuration parameters for the Entry fields. Defaults to {}.
            caseParam (dict): Configuration parameters for the input cases. Defaults to {}.
            buttonParam (dict): Configuration parameters for the buttons. Defaults to {}.
            margin (tuple): Margin values for the window (vertical, horizontal). Defaults to (20, 20).
        """
        self.window = tkinter.Toplevel(root)
        self.window.title(title)

        self.window.bind("<Escape>", lambda e: self.window.destroy())

        # data var
        self.errorLog:dict = {}
        self._entryList:list = []
        self.values = []

        try:
            self.window.configure(**windowConfig)
        except Exception as e:
            # unexpected param given
            self.errorLog["Window Configure"] = e

        try:
            mainFrame = tkinter.Frame(self.window, bg=windowConfig["bg"])
        except KeyError:
            # no "bg" param given
            mainFrame = tkinter.Frame(self.window)
        mainFrame.pack(fill="both", expand=True, pady=margin[0], padx=margin[1])

        tabFrame = tkinter.Frame(mainFrame)
        tabFrame.pack(fill="both", expand=True)
        if len(inputsInsert) != len(labelsText) and len(inputsInsert) != 0:
            # cannot guess which "Insert" corresponds to which "Input".
            self.errorLog["Input & label"] = "Error : the two string lists have not the same length or ."
            self.window.destroy()
        else:
            for i in range(len(labelsText)):
                try:
                    rowFrame = tkinter.Frame(mainFrame, bg=windowConfig["bg"])
                except KeyError:
                    rowFrame = tkinter.Frame(mainFrame)
                rowFrame.pack(fill="x", expand=True)

                LeftcaseFrame = tkinter.Frame(rowFrame, **caseParam)
                LeftcaseFrame.pack(fill="x", expand=True, side="right")

                label = tkinter.Label(LeftcaseFrame, text=labelsText[i], **labelParam)
                label.pack(side="left")

                RightcaseFrame = tkinter.Frame(rowFrame, **caseParam)
                RightcaseFrame.pack(fill="x", expand=True, side="right")
                
                self._entryList.append(tkinter.Entry(LeftcaseFrame, **inputParam))
                if len(inputsInsert)>0:
                    self._entryList[-1].insert(0,  inputsInsert[i])
                
                self._entryList[-1].pack(side="left")
                self._entryList[-1].bind("<Return>", self.confirm)
            
            try:
                footerFrame = tkinter.Frame(mainFrame, bg=windowConfig["bg"])
            except KeyError:
                footerFrame = tkinter.Frame(mainFrame)
            footerFrame.pack(fill="x", expand=True, anchor="s", pady=5)

            confirmButton = tkinter.Button(footerFrame, text="Confirm", command=self.confirm, **buttonParam)
            confirmButton.pack(side="left")

            cancelButton = tkinter.Button(footerFrame, text="Cancel", command=self.window.destroy, **buttonParam)
            cancelButton.pack(side="right")
            
            
            set_geometry(self.window, marginNS=margin[0],  marginEW=margin[1])
    
    def confirm(self, e=None):
        self.save_values()
        self.window.destroy()

    def get_errors(self) -> dict:
        return self.errorLog

    def save_values(self) -> list[str]:
        self.values= [elt.get() for elt in self._entryList]
        return self.values
            
    def destroy(self):
        self.window.destroy()