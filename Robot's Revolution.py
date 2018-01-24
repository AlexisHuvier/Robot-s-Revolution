import sys
from tkinter import Entry, Tk, Label, Button, END, TclError
from tkinter.messagebox import showerror, showinfo
try:
    from files.RR_Game import Game
except ImportError:
    sys.path.append("files")
    from RR_Game import Game

LEVEL = 1
FENETRE = None
ENOM = None
LTITRE = None

def Quitter():
    global FENETRE

    FENETRE.destroy()

def Jouer():
    global ENOM, LEVEL, LTITRE

    if ENOM.get() == "":
        showerror("Your Robot", "Veuillez écrire quelque chose !")
    elif ENOM.get() == "Nom du script":
        showerror("Your Robot", "Veuillez changer le nom !")
    else:
        try:
            with open("scripts/"+ENOM.get()+".rev"):
                pass
        except IOError:
            showerror("Fichier inconnu", "Le fichier n'a pas pu être ouvert.")
        else:
            game = Game("scripts/"+ENOM.get()+".rev", "Parcours", LEVEL)
            LEVEL = game.launch()
            try:
                with open("levels/"+str(LEVEL)+".rev"):
                    pass
            except IOError:
                showinfo("Bravo !", "Vous avez fini tous les niveaux de ce mode !")
                Solo()
            else:
                showinfo("Suivant", "C'est parti pour le niveau "+str(LEVEL))
                LTITRE['text'] = "Level "+str(LEVEL)

def FenScriptP():
    global ENOM, FENETRE, LTITRE
    FENETRE.destroy()

    FENETRE = Tk()
    FENETRE.title("Robot's Revolution")
    FENETRE.geometry("180x180")

    LTITRE = Label(FENETRE, text="Level "+str(LEVEL),
                   font=("Comic Sans MS", 14, "bold"))
    ENOM = Entry(FENETRE)
    ENOM.insert(END, "Nom du script")
    BQuitterF = Button(FENETRE, text="Quitter", width=9, command=Solo)
    BEnregistrer = Button(FENETRE, text="Lancer", width=9, command=Jouer)

    LTITRE.place(x=40, y=20)
    ENOM.place(x=30, y=100)
    BEnregistrer.place(x=10, y=140)
    BQuitterF.place(x=100, y=140)

    FENETRE.mainloop()

def FenScriptVersus():
    showerror("Coming Soon", "Le mode Versus IA viendra plus tard")

def Solo():
    global FENETRE, LEVEL
    FENETRE.destroy()
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

Menu()
