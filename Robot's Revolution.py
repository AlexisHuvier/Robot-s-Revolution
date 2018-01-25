import sys
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from PIL import Image, ImageTk
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

def Jouer(name):
    global LEVEL, SCREEN, CANVAS

    if name == "":
        showerror("Your Robot", "Veuillez écrire quelque chose !")
    elif name == "Nom du script":
        showerror("Your Robot", "Veuillez changer le nom !")
    else:
        try:
            with open("scripts/"+name+".rev"):
                pass
        except IOError:
            showerror("Fichier inconnu", "Le fichier n'a pas pu être ouvert.")
        else:
            game = Game("scripts/"+name+".rev", "Parcours", LEVEL)
            LEVEL = game.launch()
            try:
                with open("levels/"+str(LEVEL)+".rev"):
                    pass
            except IOError:
                showinfo("Bravo !", "Vous avez fini tous les niveaux de ce mode !")
                Solo()
            else:
                showinfo("Suivant", "C'est parti pour le niveau "+str(LEVEL))
                image = Image.open("files/l"+str(LEVEL)+".png")
                photo = ImageTk.PhotoImage(image)
                item = CANVAS.create_image(300, 300, image=photo)

def Execute():
    global FENETRE, NOM, COD, CANVAS
    if NOM.get() != "Nom Script" or NOM.get() != "":
        if " " in NOM.get():
            showerror("ERROR","Le nom du script a un espace")
        else:
            with open("scripts/"+NOM.get()+".rev","w") as fichier:
                fichier.write(CODE.get("1.0","end"))
            Jouer(NOM.get())
    else:
        showerror("ERROR","Il faut changer le nom du script ou lui en donner un")

def FenScriptP():
    global FENETRE, LTITRE, NOM, SCREEN, CODE, CANVAS
    FENETRE.destroy()
    
    FENETRE = Tk()
    FENETRE.title("Revolt IDE")
    
    CODE = Text(FENETRE,font=("Comic Sans MS", 14), wrap='none',tabs=('1c', '2c'))
    CODE.insert('1.0','#Votre code')
    s1 = Scrollbar(FENETRE)
    s2 = Scrollbar(FENETRE)
    NOM = Entry()
    NOM.insert(END,"Nom Script")
    executer = Button(FENETRE, text="Exécuter", command=Execute)
    CODE.config(yscrollcommand = s1.set, xscrollcommand = s2.set)
    s2.config(orient="horizontal")
    s2.config(command = CODE.xview)
    s1.config(command = CODE.yview)
    
    CODE.grid(row=0, column=0, sticky="NSEW")
    s1.grid(row=0, column=1, stick="NSEW")
    s2.grid(row=1, column=0, columnspan=2, stick="NSEW")
    NOM.grid(row=2, column=0, stick="NSEW")
    executer.grid(row=2, column=1, stick="NSEW")
    CODE.focus_set()    
    
    SCREEN = Toplevel(FENETRE)
    SCREEN.title("Level"+str(LEVEL))
    SCREEN.geometry("620x650")

    LTITRE = Label(SCREEN, text="Level "+str(LEVEL),
                   font=("Comic Sans MS", 14, "bold"))

    CANVAS = Canvas(SCREEN,width=600,height=600,bg="black")
    image = Image.open("files/l"+str(LEVEL)+".png") 
    photo = ImageTk.PhotoImage(image) 
    item = CANVAS.create_image(300, 300, image=photo)

    LTITRE.place(x=260, y=5)
    CANVAS.place(x=10, y=40)

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
