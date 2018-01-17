import pygame, sys
from tkinter.messagebox import *

instructions = ["walk", "left", "right", "setSprite", "loopif", "loop", "sayConsole","if_", "getPosX", "getPosY"]

class Script():
    def __init__(self, robot, fichier):
        self.fichier = fichier
        self.robot = robot
        self.avancement = 0
        self.temp_boucle_a_faire = -1
        try:
            with open(self.fichier):
                pass
        except IOError:
            showerror("Fichier inconnu", "Le fichier n'a pas pu être ouvert.")
            sys.exit()
        else:
            with open(self.fichier, 'r') as fichier:
                self.instruction = fichier.read().split("\n")
    
    def launch(self):
        if len(self.instruction)-1 >= self.avancement:
            if self.instruction[self.avancement].split("(")[0] in instructions:
                eval("self."+self.instruction[self.avancement])
                self.avancement += 1
                return 1
            elif self.instruction[self.avancement] == "":
                self.avancement += 1
                return 1
            else:
                showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1))
                pygame.quit()
                return 0
        else:
            return 1

    def walk(self):
        if self.robot.direction == 0:
            self.robot.rect.x += 60
            self.robot.posX += 1
        elif self.robot.direction == 1:
            self.robot.rect.y += 60
            self.robot.posY += 1
        elif self.robot.direction == 2:
            self.robot.rect.x -= 60
            self.robot.posX -= 1
        elif self.robot.direction == 3:
            self.robot.rect.y -= 60
            self.robot.posY -= 1
    
    def right(self):
        self.robot.direction += 1
        if self.robot.direction == 4:
            self.robot.direction = 0
        if self.robot.direction == 0:
            if self.robot.strImage in ["files/FlammyD.png","files/FlammyB.png","files/FlammyG.png","files/FlammyH.png"]:
                self.robot.strImage = "files/FlammyD.png"
                self.robot.image = pygame.image.load("files/FlammyD.png")
        elif self.robot.direction == 1:
            if self.robot.strImage in ["files/FlammyD.png","files/FlammyB.png","files/FlammyG.png","files/FlammyH.png"]:
                self.robot.strImage = "files/FlammyB.png"
                self.robot.image = pygame.image.load("files/FlammyB.png")
        elif self.robot.direction == 2:
            if self.robot.strImage in ["files/FlammyD.png","files/FlammyB.png","files/FlammyG.png","files/FlammyH.png"]:
                self.robot.strImage = "files/FlammyG.png"
                self.robot.image = pygame.image.load("files/FlammyG.png")
        elif self.robot.direction == 3:
            if self.robot.strImage in ["files/FlammyD.png","files/FlammyB.png","files/FlammyG.png","files/FlammyH.png"]:
                self.robot.strImage = "files/FlammyH.png"
                self.robot.image = pygame.image.load("files/FlammyH.png")
    
    def left(self):
        self.robot.direction -= 1
        if self.robot.direction == -1:
            self.robot.direction = 3
        if self.robot.direction == 0:
            if self.robot.strImage in ["files/FlammyD.png","files/FlammyB.png","files/FlammyG.png","files/FlammyH.png"]:
                self.robot.strImage = "files/FlammyD.png"
                self.robot.image = pygame.image.load("files/FlammyD.png")
        elif self.robot.direction == 1:
            if self.robot.strImage in ["files/FlammyD.png","files/FlammyB.png","files/FlammyG.png","files/FlammyH.png"]:
                self.robot.strImage = "files/FlammyB.png"
                self.robot.image = pygame.image.load("files/FlammyB.png")
        elif self.robot.direction == 2:
            if self.robot.strImage in ["files/FlammyD.png","files/FlammyB.png","files/FlammyG.png","files/FlammyH.png"]:
                self.robot.strImage = "files/FlammyG.png"
                self.robot.image = pygame.image.load("files/FlammyG.png")
        elif self.robot.direction == 3:
            if self.robot.strImage in ["files/FlammyD.png","files/FlammyB.png","files/FlammyG.png","files/FlammyH.png"]:
                self.robot.strImage = "files/FlammyH.png"
                self.robot.image = pygame.image.load("files/FlammyH.png")
                
    
    def setSprite(self, sprite = "files/FlammyD.png"):
        self.robot.strImage = sprite
        self.robot.image = pygame.image.load(sprite)
    
    def getPosX(self):
        return self.robot.posX
    
    def getPosY(self):
        return self.robot.posY
    
    def sayConsole(self, txt = "Bonjour"):
        print(txt)
    
    def loop(self, instruction = "walk()", nb = 1):
        if self.temp_boucle_a_faire == 0:
            self.temp_boucle_a_faire = -1
        elif self.temp_boucle_a_faire == -1:
            self.temp_boucle_a_faire = nb
            self.avancement -= 1
        else:
            if instruction.split("(")[0] in instructions:
                eval("self."+instruction)
                self.avancement -=1
                self.temp_boucle_a_faire -= 1
            else:
                showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                pygame.quit()
            
    def loopif(self, instruction = "walk()", condition = "True"):
        if condition.split("(")[0] in instructions:
            if eval("self."+condition):
                if instruction.split("(")[0] in instructions:
                    eval("self."+instruction)
                    self.avancement -=1
                    self.temp_boucle_a_faire -= 1
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                    pygame.quit()
        else:
            if eval(condition):
                if instruction.split("(")[0] in instructions:
                    eval("self."+instruction)
                    self.avancement -=1
                    self.temp_boucle_a_faire -= 1
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                    pygame.quit()
    def if_(self, instruction, condition = "True"):
        if condition.split("(")[0] in instructions:
            if eval("self."+condition):
                eval("self."+instruction)
        else:
            if eval(condition):
                eval("self."+instruction)
