from tkinter import *
from tkinter.messagebox import showerror, showinfo, askquestion
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import pygame, glob, random
try:
    from files.RR_Game import Game
    from files.RR_class import Map, PreviewThread
except ImportError:
    from RR_class import Map, PreviewThread
    from RR_Game import Game

class VEditor(Tk):
    """Editeur de script"""
    def __init__(self, level, mode, ia = None):
        super(VEditor, self).__init__()
        self.visuel = True
        self.dOn = False
        self.preview = None
        self.mode = mode
        self.difficultScreen = ""
        self.difficult = "MP"
        self.aide = ""
        self.on = True
        self.levels = []
        try:
            with open("files/saves.txt", "r") as fichier:
                temp = fichier.read().split("\n")
                for i in temp:
                    self.levels.append(i.split(" - "))
        except IOError:
            showwarning("ATTENTION", "Le fichier des sauvegardes n'a pas été trouvé et va être recréer")
            with open("files/saves.txt", "w") as fichier:
                fichier.write("Mode - Nom - Difficulté - NombreLigne")
        if self.mode == "IA" or self.mode == "Versus":
            nb = len(glob.glob("levels/mp_*.rev"))
            if nb == 1 or nb == 0:
                self.level = "mp_1"
            else:
                self.level = "mp_"+str(random.randint(1, nb))
            if ia == None:
                self.ia = "ia_1"
            else:
                self.ia = ia
            while True:
                find = False
                for i in self.levels:
                    if i[0] == self.mode:
                        if str(self.ia) == i[1]:
                            find = True
                            if askquestion("Jouer", "Vous avez déjà battu "+i[1]+ " avec "+i[3]+" lignes de codes.\nVoulez vous rejouer ?") == "yes":
                                find = False
                                break
                            else:
                                if "ia_" in self.ia:
                                    self.ia = "ia_"+str(int(self.ia[3:])+1)
                                    try:
                                        with open("files/ia/"+self.ia+".rev"):
                                            pass
                                    except:
                                        showerror("ERREUR", "Il n'y a plus d'IA à battre")
                                        showinfo("Fermeture", "Fermeture du jeu")
                                        self.on = False
                                        self.destroy()
                                        if self.preview != None:
                                            self.preview.stopThread()
                                            self.preview.join()
                                            self.preview = None
                                else:
                                    showinfo("Fermeture", "Fermeture du jeu")
                                    self.on = False
                                    self.destroy()
                                    if self.preview != None:
                                        self.preview.stopThread()
                                        self.preview.join()
                                        self.preview = None
                if find == False:
                    break

        else:
            self.level = level
            while True:
                find = False
                for i in self.levels:
                    if i[0] == self.mode:
                        if str(self.level) == i[1]:
                            find = True
                            if askquestion("Jouer", "Vous avez fini le level "+i[1]+ " avec "+i[3]+" lignes de codes.\nVoulez vous rejouer ?") == "yes":
                                find = False
                                break
                            else:
                                if self.mode == "Parcours":
                                    self.level = self.level+1
                                    try:
                                        with open("levels/"+str(self.level)+".rev"):
                                            pass
                                    except:
                                        showerror("ERREUR", "Il n'y a plus de niveau")
                                        self.quitter()
                if find == False:
                    break
        self.title("Revolt IDE - Untitled")
        self.mainloop()