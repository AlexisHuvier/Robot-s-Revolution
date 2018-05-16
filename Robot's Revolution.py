import sys, os, time
import pygame
from tkinter import Tk
from tkinter.messagebox import showwarning
try:
    from files.python.RR_Menus import MenuPrincipal, init
except ImportError:
    sys.path.append("files/python")
    from RR_Menus import MenuPrincipal, init

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
    

MenuPrincipal(init())
