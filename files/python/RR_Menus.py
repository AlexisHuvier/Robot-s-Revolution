from tkinter import *
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, showinfo, showwarning
import pygame, os, time
try:
    from files.python.RR_Editor import Editor
    from files.python.RR_VEditor import VEditor
    from files.python.RR_Utils import downloadFile
    from files.python.RR_MenusMulti import *
except ImportError:
    from RR_Editor import Editor
    from RR_VEditor import VEditor
    from RR_Utils import downloadFile
    from RR_MenusMulti import *

def Campagne(Fen, Level, play):
    Fen.destroy()
    try:
        pygame.mixer.pause()
        play = False
    except:
        pass
    window = True
    while window:
        Fen = Editor(Level, "Parcours")
        while Fen.on:
                pass
        if Fen.visuel:
            Fen = VEditor(Level, "Parcours")
            while Fen.on:
                pass
            if Fen.visuel:
                window = False
        else:
            window = False
    Parcours(Fen, Level, play)

def Community(Fen, Level, play):
    Fen.destroy()
    try:
        pygame.mixer.pause()
        play = False
    except:
        pass
    Fen = CommunityFen()
    while Fen.on:
        pass
    if Fen.choix != "Quit":
        result = downloadFile(Fen.choix[3], "level")
        if result:
            window = True
            while window:
                Fen = Editor(Fen.choix[3], "Community")
                while Fen.on:
                        pass
                if Fen.visuel:
                    Fen = VEditor(Fen.choix[3], "Community")
                    while Fen.on:
                        pass
                    if Fen.visuel:
                        window = False
                else:
                    window = False
        else:
            showerror("ERREUR", "Le téléchargement n'a pu être fait.\nVeuillez vérifier votre connection et l'existance du niveau")
    Parcours(Fen, Level, play)


def Parcours(Fen, Level, play, evt=None):
    try:
        Fen.destroy()
    except TclError:
        pass
    Level = 1

    Fen = Tk()
    Fen.title("Robot's Revolution")
    Fen.geometry("406x360")


    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(Fen,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/images/fond_intro.jpg"))
    canvas.create_image(300, 305, image = backgroundImage)
    canvas.create_text(200, 120, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FA6C00')

    image = Image.open("files/images/Camp.png")
    photo = ImageTk.PhotoImage(image)
    BParcours = Button(Fen, image = photo, relief = FLAT, command = lambda: Campagne(Fen, Level, play),activebackground="grey")
    BParcours.place(x=10, y=150)

    image2 = Image.open("files/images/Com.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(Fen, image=photo2,relief = FLAT, command=lambda: Community(Fen, Level, play),activebackground="grey")
    BVersus.place(x=265, y=150)

    image3 = Image.open("files/images/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExitF = Button(Fen, image = photo3, relief = FLAT, command =lambda: MenuPrincipal([Level, Fen, play]),activebackground="grey" )
    BExitF.place(x=135, y=210)

    if play:
        image4 = Image.open("files/images/sonO.png")
    else:
        image4 = Image.open("files/images/sonX.png")
    photo4 = ImageTk.PhotoImage(image4)
    Bson = Button(Fen, image = photo4, relief = FLAT, command =lambda: son(play, Fen) )
    Bson.place(x=355, y=310)
   
    image5 = Image.open("files/images/bt_edit.png")
    photo5 = ImageTk.PhotoImage(image5)
    BEdit = Button(Fen, image = photo5, relief = FLAT, command=popen)
    BEdit.place(x = 10, y=310)
    

    canvas.pack()

    Fen.mainloop()

def Singleplayer(Fen, Level, play) :
    Fen.destroy()
    try:
        pygame.mixer.pause()
        play = False
    except:
        pass
    window = True
    while window:
        Fen = Editor("mp", "IA", "ia_1")
        while Fen.on:
                pass
        if Fen.visuel:
            Fen = VEditor("mp", "IA", "ia_1")
            while Fen.on:
                pass
            if Fen.visuel:
                window = False
        else:
            window = False
    Versus(Fen, Level, play)
    
def Multiplayer(Fen, Level, play) :
    Fen.destroy()
    try:
        pygame.mixer.pause()
        play = False
    except:
        pass

    Fen = VersusFen()
    while Fen.on:
        pass
    if Fen.choix != "Quit":
        result = downloadFile(Fen.choix[3], "ia")
        if result:
            window = True
            while window:
                Fen = Editor("mp", "Versus", Fen.choix[3])
                while Fen.on:
                        pass
                if Fen.visuel:
                    Fen = VEditor("mp", "Versus", Fen.choix[3])
                    while Fen.on:
                        pass
                    if Fen.visuel:
                        window = False
                else:
                    window = False
        else:
            showerror(
                "ERREUR", "Le téléchargement n'a pu être fait.\nVeuillez vérifier votre connection et l'existance du niveau")
    Versus(Fen, Level, play)
    
def Versus(Fen, Level, play, evt = None):

    try:
        Fen.destroy()
         
    except TclError:
        pass
    except AttributeError:
        pass
    
    Fen = Tk()
    Fen.title("Robot's Revolution")
    Fen.geometry("406x360")

    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(Fen,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/fond_intro.jpg"))
    canvas.create_image(300, 305, image = backgroundImage)
    canvas.create_text(200, 120, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FA6C00')

    image = Image.open("files/images/bouton_sin.png")
    photo = ImageTk.PhotoImage(image)
    BParcours = Button(Fen, image = photo, relief = FLAT, command = lambda: Singleplayer(Fen, Level, play),activebackground="grey")
    BParcours.place(x=10, y=150)

    image2 = Image.open("files/images/bouton_multi.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(Fen, image=photo2,relief = FLAT, command=lambda: Multiplayer(Fen, Level, play),activebackground="grey")
    BVersus.place(x=265, y=150)

    image3 = Image.open("files/images/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExitF = Button(Fen, image = photo3, relief = FLAT, command =lambda: MenuPrincipal([Level, Fen, play]),activebackground="grey" )
    BExitF.place(x=135, y=210)

    if play:
        image4 = Image.open("files/images/sonO.png")
    else:
        image4 = Image.open("files/images/sonX.png")
    photo4 = ImageTk.PhotoImage(image4)
    Bson = Button(Fen, image = photo4, relief = FLAT, command =lambda: son(play, Fen) )
    Bson.place(x=355, y=310)
   
    image5 = Image.open("files/images/bt_edit.png")
    photo5 = ImageTk.PhotoImage(image5)
    BEdit = Button(Fen, image = photo5, relief = FLAT, command=popen)
    BEdit.place(x = 10, y=310)
    

    canvas.pack()

    Fen.mainloop()

def showHistory(mode, Fen, Level, play):
    try:
        Fen.destroy()
    except TclError:
        pass
    Fen = Tk()
    canvas = Canvas(Fen, width=1100, height=550, bg='black')
    canvas.pack()
    if mode == "Parcours":
        try:
            with open('files/python/histoireParcours.txt', 'r') as fichier:
                texte = fichier.read()
            canvas.create_text(500, 680, text=texte, font=("Comic Sans MS", 20, "bold"), fill='white')
        except:
            showerror("ERREUR", "Impossible de trouver l'histoire. Passage aux modes Parcours.")
            Parcours(Fen, Level, play)
    else:
        try:
            with open('files/python/histoireVersus.txt', 'r') as fichier:
                texte = fichier.read()
            canvas.create_text(500, 680, text=texte, font=("Comic Sans MS", 20, "bold"), fill='white')
        except:
            showerror("ERREUR", "Impossible de trouver l'histoire. Passage aux modes Versus.")
            Versus(Fen, Level, play)

    if mode == "Parcours":
        Fen.bind_all("<KeyPress-F5>", lambda evt: Parcours(Fen, Level, play))
        Fen.bind_all("<KeyPress-Return>", lambda evt: Parcours(Fen, Level, play))
    else:
        Fen.bind_all("<KeyPress-F5>", lambda evt: Versus(Fen, Level, play))
        Fen.bind_all("<KeyPress-Return>", lambda evt: Versus(Fen, Level, play))
    for x in range(0, 200):
        canvas.move(1, 0, -5)
        Fen.update()
        time.sleep(0.1)
    
    Fen.mainloop()
    if mode == "Parcours":
        Parcours(Fen, Level, play)
    else:
        Versus(Fen, Level, play)

def MenuPrincipal(Liste):
    Level, Fen, play = Liste

    try:
        Fen.destroy()
    except TclError:
        pass
    except AttributeError:
        pass

    Fen = Tk()
    Fen.title("Robot's Revolution")
    Fen.geometry("406x360")


    canvasWidth=600
    canvasHeight=400
    canvas=Canvas(Fen,width=canvasWidth,height=canvasHeight)
    backgroundImage=ImageTk.PhotoImage(Image.open("files/images/fond_intro.jpg"))
    canvas.create_image(300, 305, image = backgroundImage)
    canvas.create_text(200, 120, text="Robot's Revolution", font=("Comic Sans MS", 20, "bold"), fill = '#FA6C00')

    image = Image.open("files/images/bouton_parc.png")
    photo = ImageTk.PhotoImage(image)
    BParcours = Button(Fen, image = photo, relief = FLAT, command = lambda: showHistory("Parcours", Fen, Level, play),activebackground="grey")
    BParcours.place(x=10, y=150)

    image2 = Image.open("files/images/bouton_Vers.png")
    photo2 = ImageTk.PhotoImage(image2)
    BVersus = Button(Fen, image=photo2,relief = FLAT, command=lambda: showHistory("Versus", Fen, Level, play),activebackground="grey")
    BVersus.place(x=265, y=150)



    image3 = Image.open("files/images/bouton_exit.png")
    photo3 = ImageTk.PhotoImage(image3)
    BExitF = Button(Fen, image = photo3, relief = FLAT, command =lambda: Quitter(Fen),activebackground="grey" )
    BExitF.place(x=135, y=210)

    if play:
        image4 = Image.open("files/images/sonO.png")
    else:
        image4 = Image.open("files/images/sonX.png")
    photo4 = ImageTk.PhotoImage(image4)
    Bson = Button(Fen, image = photo4, relief = FLAT, command =lambda: son(play, Fen) )
    Bson.place(x=355, y=310)
   
    image5 = Image.open("files/images/bt_edit.png")
    photo5 = ImageTk.PhotoImage(image5)
    BEdit = Button(Fen, image = photo5, relief = FLAT, command=popen)
    BEdit.place(x = 10, y=310)
    

    canvas.pack()

    Fen.mainloop()

def init():
    Level = 1
    Fen = None
    file = 'files/sound/compo.wav'
    pygame.mixer.init()
    play = True
    son = pygame.mixer.Sound(file)
    son.play(loops=-1, maxtime=0, fade_ms=0)
    return Level, Fen, play

def popen():
	os.popen("Level Editor.py")

def son (play, Fen) :
    if play:
        pygame.mixer.pause()
        play = False
        image5 = Image.open("files/images/sonX.png")
        photo5 = ImageTk.PhotoImage(image5)
        BsonX = Button(Fen, image = photo5, relief = FLAT, command = lambda: son(play, Fen))
        BsonX.place(x=355, y=310)
            
    else:
        pygame.mixer.unpause()
        play = True
        image4 = Image.open("files/images/sonO.png")
        photo4 = ImageTk.PhotoImage(image4)
        Bson = Button(Fen, image = photo4, relief = FLAT, command =lambda: son(play, Fen) )
        Bson.place(x=355, y=310)
    Fen.mainloop()

def Quitter(Fen):
    try:
        pygame.mixer.stop()
    except:
        pass
    Fen.destroy()