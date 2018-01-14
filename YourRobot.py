import pygame, random, sys, glob
from tkinter import *
from files.YR_class import *
from tkinter.messagebox import *

class Game():
    def __init__(self, fichier, mode):
        self.level = 1
        pygame.init()

        self.screen=pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Your Robot")

        self.clock=pygame.time.Clock()

        self.done = True
        self.player = Player(fichier)
        self.mode = mode
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        self.finish_list = pygame.sprite.Group()
        self.rock_list = pygame.sprite.Group()
        if self.mode == "Parcours":
            try:
                with open("levels/"+str(self.level)+".yr", 'r') as fichier:
                    lignes = fichier.read().split("\n")
                    self.player.rect.x = int(lignes[0].split(",")[0])
                    self.player.rect.y = int(lignes[0].split(",")[1])
                    self.finish = Finish([int(lignes[len(lignes)-1].split(",")[0]),int(lignes[len(lignes)-1].split(",")[1])])
                    self.finish_list.add(self.finish)
                    for i in range(1, len(lignes)-1):
                        self.rock = Rock([int(lignes[i].split(",")[0]),int(lignes[i].split(",")[1])])
                        self.rock_list.add(self.rock)
            except IOError:
                showerror("ERREUR","Le fichier du level "+str(self.level)+" est inaccessible")
                pygame.quit()
                        
        self.launch()
        
    def launch(self):
        while self.done :
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.done = False
                    pygame.quit()
                if event.type == pygame.QUIT:
                    self.done = False
                    pygame.quit()

            result = self.player.update(self.rock_list, self.finish_list)
            
            if result:
                self.screen.fill((0,0,0))
                self.clock.tick(60)
                self.player_list.draw(self.screen)
                self.rock_list.draw(self.screen)
                self.finish_list.draw(self.screen)
                pygame.display.update()
            else:
                self.done = False

def Quitter():    
    global Fenetre
    
    Fenetre.destroy()

def Jouer():
    global ENom
    
    if ENom.get() == "" :
        showerror("Your Robot","Veuillez écrire quelque chose !")
    elif ENom.get() == "Nom du script" :
        showerror("Your Robot","Veuillez changer le nom !")
    else:
        try:
            with open("scripts/"+ENom.get()+".yr"):
                pass
        except IOError:
            showerror("Fichier inconnu", "Le fichier n'a pas pu être ouvert.")
        else:
            game = Game("scripts/"+ENom.get()+".yr", "Parcours")

def FenScriptP():
    global ENom, Fenetre
    Fenetre.destroy()
    
    Fenetre = Tk()
    Fenetre.title("Your Robot")
    Fenetre.geometry("180x180")

    LTitre = Label(Fenetre,text="Your Robot",font=("Comic Sans MS",14,"bold"))
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
    global Fenetre
    Fenetre.destroy()
    
    Fenetre = Tk()
    Fenetre.title("Your Robot")
    Fenetre.geometry("180x180")

    LTitre = Label(Fenetre,text="Your Robot",font=("Comic Sans MS",14,"bold"))

    BParcours = Button(Fenetre, text="Parcours", width = 9, command = FenScriptP)
    BVersus = Button(Fenetre, text="Versus IA", width = 9, command = FenScriptVersus)
    BQuitterF = Button(Fenetre,text="Quitter",width = 9,command = Menu)

    LTitre.place(x=40,y=20)
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
    Fenetre.title("Your Robot")
    Fenetre.geometry("180x180")

    LTitre = Label(Fenetre,text="Your Robot",font=("Comic Sans MS",14,"bold"))

    BSolo = Button(Fenetre, text="Singleplayer", width = 9, command = Solo)
    BMulti = Button(Fenetre, text="Multiplayer", width = 9, command = Multi)
    BQuitterF = Button(Fenetre,text="Quitter",width = 9,command = Quitter)

    LTitre.place(x=40,y=20)
    BSolo.place(x=10,y=90)
    BMulti.place(x=100,y=90)
    BQuitterF.place(x=50,y=140)

    Fenetre.mainloop()

Menu()
