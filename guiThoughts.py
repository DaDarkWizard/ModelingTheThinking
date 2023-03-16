import cmlparser
import os
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo

def createFile():
    hi = 0
    
def browseFiles():
    # Open file explorer in directory of program
    path = os.getcwd()
    fileName = filedialog.askopenfilename(initialdir=path, title='Select a file', filetypes=(('CML files','*.cml*'), ('All files','*.*')))
    
    # If there was a file chosen, run this
    if fileName != '':
    
        showinfo(title='Selected File', message=fileName)
    
        input_text = open(fileName).read()
        parser = cmlparser.CMLParser()
        parser.reset()
        parser.parse_string(input_text)
    

def saveFile():
    hi = 0

def menu():
    """
    Creates a menu bar\n
    Args:\n
        root (_type_): _description_
    """    
    # Create menu bar
    menubar = Menu(root)
    
    # Add File submenu to menu bar w/ New, Open, Save, and Exit options
    fileMenu = Menu(menubar, tearoff=0)
    fileMenu.add_command(label = "New File", command=createFile)
    fileMenu.add_command(label = "Open...", command=browseFiles)
    fileMenu.add_command(label = "Save", command=saveFile)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=fileMenu)
    
    # Add File submenu w/ New, Open, Save, and Exit options
    helpMenu = Menu(menubar, tearoff=0)
    helpMenu.add_command(label = "Help Index")
    helpMenu.add_command(label = "About...")
    menubar.add_cascade(label="Help", menu=helpMenu)
    
    root.config(menu=menubar)

# create GUI
root = Tk()

root.option_add('*tearOff', FALSE)

# set title of window
root.title("Modeling The Thinking")

# set window with size 720p
root.geometry("1280x720")

# add menubar to window
menu()

# run GUI
root.mainloop()
