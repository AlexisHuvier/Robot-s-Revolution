import sys
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from PIL import ImageTk, Image
try:
    from files.RR_Editor import Editor
except ImportError:
    sys.path.append("files")
    from RR_Editor import Editor

LEVEL = 1
FENETRE = None
ENOM = None
LTITRE = None

def FenScriptP():
    global FENETRE, LEVEL
    FENETRE.destroy()
    
    FENETRE = Editor(LEVEL, "Parcours")
    while FENETRE.on:
        pass
    Solo()
    

def FenScriptVersus():
    showerror("Coming Soon", "Le mode Versus IA viendra plus tard")

def Quitter():
    global FENETRE
    FENETRE.destroy()

def Solo():
    global FENETRE, LEVEL
    try:
        FENETRE.destroy()
    except TclError:
        pass
    LEVEL = 1

    FENETRE = Tk()
    FENETRE.title("Robot's Revolution")
    FENETRE.geometry("300x200")

    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(FENETRE,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/bg.png"))
    canvas.create_image(220, 150, image = backgroundImage)
    canvas.create_text(140, 50, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FFFFFF')

    image = Image.open("files/Camp.png")
    photo = ImageTk.PhotoImage(image)
    BSolo = Button(FENETRE, image = photo, relief = FLAT, command = FenScriptP)
    BSolo.place(x=10, y=90)

    image2 = Image.open("files/Com.png")
    photo2 = ImageTk.PhotoImage(image2)
    BMulti = Button(FENETRE, image = photo2, relief = FLAT, command = Community)
    BMulti.place(x=140, y=90)

    image3 = Image.open("files/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExit = Button(FENETRE, image = photo3, relief = FLAT, command = Menu)
    BExit.place(x=70, y=140)

    canvas.pack()
    
    FENETRE.mainloop()
        
def Multi():
    global FENETRE

    try:
        FENETRE.destroy()
    except TclError:
        pass
    except AttributeError:
        pass
    FENETRE = Tk()
    FENETRE.title("Robot's Revolution")
    FENETRE.geometry("300x200")
    
    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(FENETRE,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/bg.png"))
    canvas.create_image(220, 150, image = backgroundImage)
    canvas.create_text(140, 50, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FFFFFF')

    image = Image.open("files/bouton_sin.png")
    photo = ImageTk.PhotoImage(image)
    BParcours = Button(FENETRE, image = photo, relief = FLAT, command = IA)
    BParcours.place(x=10, y=90)

    image2 = Image.open("files/bouton_multi.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(FENETRE, image=photo2,relief = FLAT, command=Serveur)
    BVersus.place(x=140, y=90)

    image3 = Image.open("files/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExitF = Button(FENETRE, image = photo3, relief = FLAT, command =Menu )
    BExitF.place(x=70, y=140)

    canvas.pack()

    FENETRE.mainloop()

def FenScriptVersus():
    showerror("Coming Soon", "Le mode Versus IA viendra plus tard")
    
def Community():
    showerror("Coming Soon", "Le mode Levels Community viendra plus tard")
    
def IA():
    global FENETRE
    FENETRE.destroy()

    FENETRE = Editor("mp", "IA")
    while FENETRE.on:
        pass
    Multi()
    
def Serveur():
    showerror("Coming Soon", "Le mode serveur viendra plus tard")
    
def FenScriptP():
    global FENETRE, LEVEL
    FENETRE.destroy()

    FENETRE = Editor(LEVEL, "Parcours")
    while FENETRE.on:
        pass
    Solo()
        
def Menu():
    global FENETRE
    try:
        FENETRE.destroy()
    except TclError:
        pass
    except AttributeError:
        pass

    FENETRE = Tk()
    FENETRE.title("Robot's Revolution")
    FENETRE.geometry("300x200")

    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(FENETRE,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/bg.png"))
    canvas.create_image(220, 150, image = backgroundImage)
    canvas.create_text(140, 50, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FFFFFF')

    image = Image.open("files/bouton_parc.png")
    photo = ImageTk.PhotoImage(image)
    BParcours = Button(FENETRE, image = photo, relief = FLAT, command = Solo)
    BParcours.place(x=10, y=90)

    image2 = Image.open("files/bouton_Vers.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(FENETRE, image=photo2,relief = FLAT, command=Multi)
    BVersus.place(x=140, y=90)

    image3 = Image.open("files/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExitF = Button(FENETRE, image = photo3, relief = FLAT, command =Quitter )
    BExitF.place(x=70, y=140)

    canvas.pack()

    FENETRE.mainloop()

try:
    with open("files/config.txt", "r") as fichier:
        lignes = fichier.read().split("\n")
except IOError:
    showwarning("ATTENTION", "Le fichier de config n'a pas été trouvé et va être recréer")
    with open("files/config.txt", "w") as fichier:
            fichier.write("Timer Instruction : 20")

Menu()
