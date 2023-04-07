import cmlparser
import os
from tkinter import *
from tkinter import ttk


# Be able to use all 18 widgets in Tkinter 
# Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar, Spinbox, Combobox, Notebook, Progressbar, Separator, Sizegrip and Treeview
#from tkinter.ttk import *

from tkinter import filedialog # To be able to open file explorer and open a file
from tkinter.messagebox import showinfo # For dialogue box

def createFile():
    hi = 0
    
def browseFiles():
    """
    Browse for files on system and open it
    """    
    
    # Open file explorer in directory of program
    path = os.getcwd()
    fileName = filedialog.askopenfilename(initialdir=path, title='Select a file', filetypes=(('CML files','*.cml*'), ('All files','*.*')))
    
    # If there was a file chosen, run this
    if fileName != '':
    
        # Pop-up to show user the chosen file
        showinfo(title='Selected File', message="Opened file at \"" + fileName + "\"")
    
        # This portion will probably be moved to a different function
        input_text = open(fileName).read()
        parser = cmlparser.CMLParser()
        parser.reset()
        parser.parse_string(input_text)

        # Very sloppy code but it gets the job done for now
        dims = list(map(lambda w: w.dimension, list(parser.scope.dimensions().values())))
        units = list(map(lambda y: y.name, list(parser.scope.units().values())))
        unitvalues = list(map(lambda z: z.value.to_string(), list(parser.scope.units().values())))
        modelfrags = list(map(lambda x: x.name, list(parser.scope.modelfragments().values())))
        for x in dims:
            bottom_tree.insert('dims', 'end', text=x)
        i = 0
        for x in units:
            i = i + 1
            bottom_tree.insert('units', 'end', i, text=x)
        j = 0
        for x in unitvalues:
            j = j + 1
            bottom_tree.insert(j, 'end', text=x)
        for x in modelfrags:
            bottom_tree.insert('modelfrags','end', text=x)
    

def saveFile():
    hi = 0

def menu():
    """
    Creates a menu bar
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

def diagramPane():
    style = ttk.Style()
    style.configure("DiaPane.TPanedwindow", padding=100, sashrelief=5)
    style.configure("DiaPane.TLabel", foreground="red")
    diaPane = ttk.PanedWindow(orient=HORIZONTAL, style="DiaPane.TPanedwindow")
    #diaPane = PanedWindow(bg="black", borderwidth=10)
    #diaPane.pack(side=LEFT, fill="y")
    diaPane.pack()
    diaPane.add(ttk.Label(diaPane, text="Diagram Pane", style="DiaPane.TLabel"))
    
def createBox(event):
    main_canvas.create_rectangle(event.x, event.y, event.x+80, event.y+80, width=4, fill='white')
    print("Created Box")

# create GUI
root = Tk()

# Get current session's screen width and height
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

# tkinter docs told me to add this line
root.option_add('*tearOff', FALSE)

# set title of window
root.title("Modeling The Thinking")

# set window with size 800x600 (4:3) (maybe add option later that lets user change default opening res)
root.geometry("800x600")

# add menubar to window
menu()

# add paned window to left hand side of root for tools

# add paned window to right hand side of root for diagrams
# diagramPane()

# Main paned window, oriented horizontal to stack items left and right
# "pw" --> "paned window"
pw = ttk.PanedWindow(orient='horizontal')

# left paned window to hold three widgets on top of one another
# "lpw" --> "left paned window"
lpw = ttk.PanedWindow(orient='vertical', width=200)

# Right paned window to hold main diagram viewer and info at bottom
# "rpw" --> "right paned window"
rpw = ttk.PanedWindow(orient='vertical')

# Create basic listboxes to hold leftside elements
# Later will be different types of tkinter widgets. https://tkdocs.com/tutorial/widgets.html
# The height of listboxes is number of text elements to show, not pixels
top_lb = Listbox(root, height=8)
top_lb.insert(1, "Tools to use")
top_lb.insert(2, "  Drag and Move Tool")
top_lb.insert(3, "  Add Relations")
top_lb.insert(4, "  Select a bunch at once tool")
top_lb.insert(5, "  etc")
top_lb.pack()
lpw.add(top_lb)

middle_lb = Listbox(root, height=8)
middle_lb.insert(1, "Drag and drop area to simply")
middle_lb.insert(2, "click type of tool to add to dia")
middle_lb.pack()
lpw.add(middle_lb)

bottom_tree = ttk.Treeview(root)
bottom_tree.insert("", 0, 'dims', text='Dimensions')
bottom_tree.insert("", 'end', 'units', text='Units')
bottom_tree.insert("", 'end', 'modelfrags', text='Model Fragments')
bottom_tree.pack()
lpw.add(bottom_tree)

lpw.pack(fill=BOTH, expand=True)
pw.add(lpw)

# Right Canvas to make up entire right side of window
main_canvas = Canvas(root, height=550, bg="#9febed")
main_canvas.bind("<Button-1>", createBox)
main_canvas.pack(side=RIGHT)
rpw.add(main_canvas)

right_text = Label(text="Additional Info (count of entities, etc) ?")
right_text.pack(side=RIGHT)
rpw.add(right_text)
rpw.pack(fill=BOTH, expand=True)
pw.add(rpw)

# place the panedwindow on the root window
pw.pack(fill=BOTH, expand=True)

# run GUI
root.mainloop()
