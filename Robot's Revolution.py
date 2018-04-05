import sys, os, time
from tkinter import *
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, showinfo, showwarning
import pygame
from pygame.locals import *
try:
    from files.RR_Editor import Editor
    from files.RR_Community import CommunityFen
    from files.RR_Versus import VersusFen
    from files.RR_class import downloadFile
except ImportError:
    sys.path.append("files")
    from RR_Editor import Editor
    from RR_Community import CommunityFen
    from RR_Versus import VersusFen
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

def history(mode):
    global FENETRE
    try:
        FENETRE.destroy()
    except TclError:
        pass
    file = 'files/compo.wav'
    FENETRE = Tk()
    canvas = Canvas(FENETRE, width=1100, height=550, bg='black')
    canvas.pack()
    if mode == "Parcours":
        try:
            with open('files/histoireParcours.txt', 'r') as fichier:
                texte = fichier.read()
            canvas.create_text(500, 680, text=texte, font=("Comic Sans MS", 20, "bold"), fill='white')
        except:
            showerror("ERREUR", "Impossible de trouver l'histoire. Passage aux modes Parcours.")
            Solo()
    else:
        try:
            with open('files/histoireVersus.txt', 'r') as fichier:
                texte = fichier.read()
            canvas.create_text(500, 680, text=texte, font=("Comic Sans MS", 20, "bold"), fill='white')
        except:
            showerror("ERREUR", "Impossible de trouver l'histoire. Passage aux modes Versus.")
            Multi()

    if mode == "Parcours":
        FENETRE.bind_all("<KeyPress-F5>", Solo)
        FENETRE.bind_all("<KeyPress-Return>", Solo)
    else:
        FENETRE.bind_all("<KeyPress-F5>", Multi)
        FENETRE.bind_all("<KeyPress-Return>", Multi)
    for x in range(0, 200):
        canvas.move(1, 0, -5)
        FENETRE.update()
        time.sleep(0.1)
    
    FENETRE.mainloop()
    if mode == "Parcours":
        Solo()
    else:
        Multi()
        


def Solo(evt=None):
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
    
def Multi(evt = None):
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
    try:
        pygame.mixer.pause()
    except:
        pass

    FENETRE = CommunityFen()
    while FENETRE.on:
        pass
    if FENETRE.choix != "Quit":
        result = downloadFile(FENETRE.choix[3], "level")
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
    try:
        pygame.mixer.pause()
    except:
        pass

    FENETRE = Editor("mp", "IA", "mp_1")
    while FENETRE.on:
        pass
    Multi()
    
def Serveur() :
    global FENETRE
    FENETRE.destroy()
    try:
        pygame.mixer.pause()
    except:
        pass

    FENETRE = VersusFen()
    while FENETRE.on:
        pass
    if FENETRE.choix != "Quit":
        result = downloadFile(FENETRE.choix[3], "ia")
        if result:
            FENETRE = Editor("mp", "Versus", FENETRE.choix[3])
            while FENETRE.on:
                pass
        else:
            showerror(
                "ERREUR", "Le téléchargement n'a pu être fait.\nVeuillez vérifier votre connection et l'existance du niveau")
    Multi()
    
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
    try:
        pygame.mixer.pause()
    except:
        pass

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
    BParcours = Button(FENETRE, image = photo, relief = FLAT, command = lambda: history("Parcours"),activebackground="grey")
    BParcours.place(x=10, y=150)

    image2 = Image.open("files/bouton_Vers.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(FENETRE, image=photo2,relief = FLAT, command=lambda: history("Versus"),activebackground="grey")
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
        pass
except IOError:
    t = Tk()
    showwarning("ATTENTION", "Le fichier de config n'a pas été trouvé et va être recréer")
    with open("files/config.txt", "w") as fichier:
        fichier.write("Timer Instruction : 20")
    t.destroy()
        
try:
    with open("files/saves.txt", "r") as fichier:
        pass
except IOError:
    t = Tk()
    showwarning("ATTENTION", "Le fichier des sauvegardes n'a pas été trouvé et va être recréer")
    with open("files/saves.txt", "w") as fichier:
        fichier.write("Mode - Nom - Difficulté - NombreLigne")
    t.destroy()
    

Menu()
