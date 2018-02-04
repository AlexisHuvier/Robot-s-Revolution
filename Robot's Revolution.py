import sys
from tkinter import *
from tkinter.messagebox import showerror, showinfo
try:
    from files.RR_Editor import Editor
except ImportError:
    sys.path.append("files")
    from RR_Editor import Editor

LEVEL = 1
FENETRE = None
ENOM = None
LTITRE = None

def Quitter():
    global FENETRE

    FENETRE.destroy()

def FenScriptP():
    global FENETRE, LEVEL
    FENETRE.destroy()
    
    FENETRE = Editor(LEVEL)
    while FENETRE.on:
        pass
    Solo()

def FenScriptVersus():
    showerror("Coming Soon", "Le mode Versus IA viendra plus tard")

def Solo():
    global FENETRE, LEVEL
    try:
        FENETRE.destroy()
    except TclError:
        pass
    LEVEL = 1

    FENETRE = Tk()
    FENETRE.title("Robot's Revolution")
    FENETRE.geometry("180x180")

    LTITRE = Label(FENETRE, text="Robot's Revolution",
                   font=("Comic Sans MS", 14, "bold"))

    BParcours = Button(FENETRE, text="Parcours", width=9, command=FenScriptP)
    BVersus = Button(FENETRE, text="Versus IA", width=9, command=FenScriptVersus)
    BQuitterF = Button(FENETRE, text="Quitter", width=9, command=Menu)

    LTITRE.place(x=5,y=20)
    BParcours.place(x=10,y=90)
    BVersus.place(x=100,y=90)
    BQuitterF.place(x=50,y=140)

    FENETRE.mainloop()

def Multi():
    showerror("Coming Soon","Le mode Multiplayer viendra plus tard")

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
    FENETRE.geometry("180x180")

    LTITRE = Label(FENETRE,text="Robot's Revolution",font=("Comic Sans MS",14,"bold"))

    BSolo = Button(FENETRE, text="Singleplayer", width = 9, command = Solo)
    BMulti = Button(FENETRE, text="Multiplayer", width = 9, command = Multi)
    BQuitterF = Button(FENETRE, text="Quitter", width=9, command=Quitter)

    LTITRE.place(x=5, y=20)
    BSolo.place(x=10,y=90)
    BMulti.place(x=100,y=90)
    BQuitterF.place(x=50,y=140)

    FENETRE.mainloop()

try:
    with open("files/config.txt", "r") as fichier:
        lignes = fichier.read().split("\n")
except IOError:
    showwarning("ATTENTION", "Le fichier de config n'a pas été trouvé et va être recréer")
    with open("files/config.txt", "w") as fichier:
        fichier.write("Timer Instruction : 20")
Menu()