import sys, os
from tkinter import *
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, showinfo
import pygame
from pygame.locals import *
try:
    from files.RR_Editor import Editor
    from files.RR_Community import CommunityFen
    from files.RR_class import downloadFile
except ImportError:
    sys.path.append("files")
    from RR_Editor import Editor
    from RR_Community import CommunityFen
    from RR_class import downloadFile

LEVEL = 1
FENETRE = None
file = 'files/compo.wav'
pygame.mixer.init()
play = True
son = pygame.mixer.Sound(file)
son.play(loops=-1, maxtime=0, fade_ms=0)

def Quitter():
    global FENETRE
    try:
        pygame.mixer.stop()
    except:
        pass
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
    FENETRE.geometry("406x360")


    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(FENETRE,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/fond_intro.jpg"))
    canvas.create_image(300, 305, image = backgroundImage)
    canvas.create_text(200, 120, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FA6C00')

    image = Image.open("files/Camp.png")
    photo = ImageTk.PhotoImage(image)
    BParcours = Button(FENETRE, image = photo, relief = FLAT, command = FenScriptP,activebackground="grey")
    BParcours.place(x=10, y=150)

    image2 = Image.open("files/Com.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(FENETRE, image=photo2,relief = FLAT, command=Community,activebackground="grey")
    BVersus.place(x=265, y=150)

    image3 = Image.open("files/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExitF = Button(FENETRE, image = photo3, relief = FLAT, command =Menu,activebackground="grey" )
    BExitF.place(x=135, y=210)

    if play:
        image4 = Image.open("files/sonO.png")
    else:
        image4 = Image.open("files/sonX.png")
    photo4 = ImageTk.PhotoImage(image4)
    Bson = Button(FENETRE, image = photo4, relief = FLAT, command =son )
    Bson.place(x=355, y=310)
   
    image5 = Image.open("files/bt_edit.png")
    photo5 = ImageTk.PhotoImage(image5)
    BEdit = Button(FENETRE, image = photo5, relief = FLAT, command=popen)
    BEdit.place(x = 10, y=310)
    

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
    FENETRE.geometry("406x360")

    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(FENETRE,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/fond_intro.jpg"))
    canvas.create_image(300, 305, image = backgroundImage)
    canvas.create_text(200, 120, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FA6C00')

    image = Image.open("files/bouton_sin.png")
    photo = ImageTk.PhotoImage(image)
    BParcours = Button(FENETRE, image = photo, relief = FLAT, command = IA,activebackground="grey")
    BParcours.place(x=10, y=150)

    image2 = Image.open("files/bouton_multi.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(FENETRE, image=photo2,relief = FLAT, command=Serveur,activebackground="grey")
    BVersus.place(x=265, y=150)

    image3 = Image.open("files/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExitF = Button(FENETRE, image = photo3, relief = FLAT, command =Menu,activebackground="grey" )
    BExitF.place(x=135, y=210)

    if play:
        image4 = Image.open("files/sonO.png")
    else:
        image4 = Image.open("files/sonX.png")
    photo4 = ImageTk.PhotoImage(image4)
    Bson = Button(FENETRE, image = photo4, relief = FLAT, command =son)
    Bson.place(x=355, y=310)
   
    image5 = Image.open("files/bt_edit.png")
    photo5 = ImageTk.PhotoImage(image5)
    BEdit = Button(FENETRE, image = photo5, relief = FLAT, command=popen)
    BEdit.place(x = 10, y=310)
    

    canvas.pack()

    FENETRE.mainloop()

    
def Community():
    global FENETRE
    FENETRE.destroy()
    pygame.mixer.stop()

    FENETRE = CommunityFen()
    while FENETRE.on:
        pass
    if FENETRE.choix != "Quit":
        result = downloadFile(FENETRE.choix[3])
        if result:
            FENETRE = Editor(FENETRE.choix[3], "Community")
            while FENETRE.on:
                pass
        else:
            showerror("ERREUR", "Le téléchargement n'a pu être fait.\nVeuillez vérifier votre connection et l'existance du niveau")
    Solo()
    
def IA() :
    global FENETRE
    FENETRE.destroy()
    pygame.mixer.stop()

    FENETRE = Editor("mp", "IA")
    while FENETRE.on:
        pass
    Multi()
    
def Serveur() :
    showerror("Coming Soon", "Le mode serveur viendra plus tard")
    
def son () :
    global play, FENETRE
    if play:
        pygame.mixer.pause()
        play = False
        image5 = Image.open("files/sonX.png")
        photo5 = ImageTk.PhotoImage(image5)
        BsonX = Button(FENETRE, image = photo5, relief = FLAT, command = son)
        BsonX.place(x=355, y=310)
            
    else:
        pygame.mixer.unpause()
        play = True
        image4 = Image.open("files/sonO.png")
        photo4 = ImageTk.PhotoImage(image4)
        Bson = Button(FENETRE, image = photo4, relief = FLAT, command =son )
        Bson.place(x=355, y=310)
    FENETRE.mainloop()
    
def FenScriptP():
    global FENETRE, LEVEL
    FENETRE.destroy()
    pygame.mixer.stop()

    FENETRE = Editor(LEVEL, "Parcours")
    while FENETRE.on:
            pass
    Solo()

def popen():
	os.popen("Level Editor.py")

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
    FENETRE.geometry("406x360")


    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(FENETRE,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/fond_intro.jpg"))
    canvas.create_image(300, 305, image = backgroundImage)
    canvas.create_text(200, 120, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FA6C00')

    image = Image.open("files/bouton_parc.png")
    photo = ImageTk.PhotoImage(image)
    BParcours = Button(FENETRE, image = photo, relief = FLAT, command = Solo,activebackground="grey")
    BParcours.place(x=10, y=150)

    image2 = Image.open("files/bouton_Vers.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(FENETRE, image=photo2,relief = FLAT, command=Multi,activebackground="grey")
    BVersus.place(x=265, y=150)



    image3 = Image.open("files/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExitF = Button(FENETRE, image = photo3, relief = FLAT, command =Quitter,activebackground="grey" )
    BExitF.place(x=135, y=210)

    if play:
        image4 = Image.open("files/sonO.png")
    else:
        image4 = Image.open("files/sonX.png")
    photo4 = ImageTk.PhotoImage(image4)
    Bson = Button(FENETRE, image = photo4, relief = FLAT, command =son )
    Bson.place(x=355, y=310)
   
    image5 = Image.open("files/bt_edit.png")
    photo5 = ImageTk.PhotoImage(image5)
    BEdit = Button(FENETRE, image = photo5, relief = FLAT, command=popen)
    BEdit.place(x = 10, y=310)
    

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
