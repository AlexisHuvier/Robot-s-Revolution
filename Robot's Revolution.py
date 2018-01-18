import pygame, random, sys, os
from tkinter import *
from tkinter.messagebox import *

sys.path.append("files")
from RR_Game import *

level = 1

def Quitter():    
    global Fenetre
    
    Fenetre.destroy()

def Jouer():
    global ENom, level, LTitre
    
    if ENom.get() == "" :
        showerror("Your Robot","Veuillez écrire quelque chose !")
    elif ENom.get() == "Nom du script" :
        showerror("Your Robot","Veuillez changer le nom !")
    else:
        try:
            with open("scripts/"+ENom.get()+".rev"):
                pass
        except IOError:
            showerror("Fichier inconnu", "Le fichier n'a pas pu être ouvert.")
        else:
            game = Game("scripts/"+ENom.get()+".rev", "Parcours", level)
            level = game.launch()
            try:
                with open("levels/"+str(level)+".rev"):
                    pass
            except IOError:
                showinfo("Bravo !", "Vous avez fini tous les niveaux de ce mode !")
                Solo()
            else:
                showinfo("Suivant", "C'est parti pour le niveau "+str(level))
                LTitre['text'] = "Level "+str(level)

def FenScriptP():
    global ENom, Fenetre, LTitre
    Fenetre.destroy()
    
    Fenetre = Tk()
    Fenetre.title("Robot's Revolution")
    Fenetre.geometry("180x180")

    LTitre = Label(Fenetre,text="Level "+str(level),font=("Comic Sans MS",14,"bold"))
    ENom = Entry(Fenetre)
    ENom.insert(END,"Nom du script")
    BQuitterF = Button(Fenetre,text="Quitter",width = 9,command = Solo)
    BEnregistrer = Button(Fenetre,text="Lancer",width = 9,command = Jouer)

    LTitre.place(x=40,y=20)
    ENom.place(x=30,y=100)
    BEnregistrer.place(x=10,y=140)
    BQuitterF.place(x=100,y=140)

    Fenetre.mainloop()
    
def FenScriptVersus():
    showerror("Coming Soon","Le mode Versus IA viendra plus tard")

def Solo():
    global Fenetre, level
    Fenetre.destroy()
    level = 1
    
    Fenetre = Tk()
    Fenetre.title("Robot's Revolution")
    Fenetre.geometry("180x180")

    LTitre = Label(Fenetre,text="Robot's Revolution",font=("Comic Sans MS",14,"bold"))

    BParcours = Button(Fenetre, text="Parcours", width = 9, command = FenScriptP)
    BVersus = Button(Fenetre, text="Versus IA", width = 9, command = FenScriptVersus)
    BQuitterF = Button(Fenetre,text="Quitter",width = 9,command = Menu)

    LTitre.place(x=5,y=20)
    BParcours.place(x=10,y=90)
    BVersus.place(x=100,y=90)
    BQuitterF.place(x=50,y=140)

    Fenetre.mainloop()

def Multi():
    showerror("Coming Soon","Le mode Multiplayer viendra plus tard")

def Menu():
    global Fenetre
    try:
        Fenetre.destroy()
    except:
        pass
    
    Fenetre = Tk()
    Fenetre.title("Robot's Revolution")
    Fenetre.geometry("180x180")

    LTitre = Label(Fenetre,text="Robot's Revolution",font=("Comic Sans MS",14,"bold"))

    BSolo = Button(Fenetre, text="Singleplayer", width = 9, command = Solo)
    BMulti = Button(Fenetre, text="Multiplayer", width = 9, command = Multi)
    BQuitterF = Button(Fenetre,text="Quitter",width = 9,command = Quitter)

    LTitre.place(x=5,y=20)
    BSolo.place(x=10,y=90)
    BMulti.place(x=100,y=90)
    BQuitterF.place(x=50,y=140)

    Fenetre.mainloop()

Menu()
