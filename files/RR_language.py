import pygame, sys
from tkinter.messagebox import showerror

instructions = ["walk", "left", "right", "jump", "getDirection", "setFunc", "callFunc",
                "getAttack", "setAttack", "setSprite", "getSprite", "setVar", "getVar",
                "loopif", "loop", "sayConsole", "if_", "getPosX", "getPosY"]

class Script():
    def __init__(self, robot, fichier):
        self.fichier = fichier
        self.robot = robot
        self.avancement = 0
        self.temp_boucle_a_faire = -1
        self.temp_fonction_a_faire = -1
        self.temp_instruction = ""
        self.last_instruction = ""
        self.variables = {}
        self.fonctions = {}
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
                self.temp_instruction = self.instruction[self.avancement].split("(")[0]
                eval("self."+self.instruction[self.avancement])
                self.last_instruction = self.temp_instruction
                self.avancement += 1
                return 1
            elif self.instruction[self.avancement] == "":
                self.avancement += 1
                return 1
            else:
                showerror("ERREUR", "Erreur sur l'instruction à la ligne n°"+str(self.avancement+1))
                pygame.quit()
                return 0
        else:
            return 1

    def jump(self):
        if self.last_instruction == "walk":
            self.robot.tempPosX = self.robot.posX
            self.robot.tempPosY = self.robot.posY
            if self.robot.carte.getObj(self.robot.posX + 1, self.robot.posY).can_be_jump:
                if self.robot.direction == 0:
                    self.robot.posX += 2
                    if self.robot.posX > 10:
                        self.robot.posX -= 2
                        showerror("ERREUR", "Le robot est sorti de l'écran.")
                    self.robot.rect.x = 20 + 70 * (self.robot.posX - 1)
                elif self.robot.direction == 1:
                    self.robot.posY += 2
                    if self.robot.posY > 10:
                        self.robot.posY -= 2
                        showerror("ERREUR", "Le robot est sorti de l'écran.")
                    self.robot.rect.y = 3 + 70 * (self.robot.posY - 1)                        
                elif self.robot.direction == 2:
                    self.robot.posX -= 2
                    if self.robot.posX < 1:
                        self.robot.posX += 2
                        showerror("ERREUR", "Le robot est sorti de l'écran.")
                    self.robot.rect.x  = 20 + 70 * (self.robot.posX - 1)                        
                elif self.robot.direction == 3:
                    self.robot.posY -= 2
                    if self.robot.posY < 1:
                        self.robot.posY += 2
                        showerror("ERREUR", "Le robot est sorti de l'écran.")
                    self.robot.rect.y = 3 + 70 * (self.robot.posY - 1)
            else:
                showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nOn ne peut jump que les cailloux")
        else:
            showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nIl n'est pas possible d'utiliser 'jump()' s'il n'y a pas un 'walk()' avant")
            
    def walk(self):
        self.robot.tempPosX = self.robot.posX
        self.robot.tempPosY = self.robot.posY
        if self.robot.direction == 0:
            self.robot.posX += 1
            if self.robot.posX > 10:
                self.robot.posX -= 1
                showerror("ERREUR", "Le robot est sorti de l'écran.")
            self.robot.rect.x  = 20 + 70 * (self.robot.posX - 1)
        elif self.robot.direction == 1:
            self.robot.posY += 1
            if self.robot.posY > 10:
                self.robot.posY -= 1
                showerror("ERREUR", "Le robot est sorti de l'écran.")
            self.robot.rect.y = 3 + 70 * (self.robot.posY - 1)
        elif self.robot.direction == 2:
            self.robot.posX -= 1
            if self.robot.posX < 1:
                self.robot.posX += 1
                showerror("ERREUR", "Le robot est sorti de l'écran.")
            self.robot.rect.x  = 20 + 70 * (self.robot.posX - 1)
        elif self.robot.direction == 3:
            self.robot.posY -= 1
            if self.robot.posY < 1:
                self.robot.posY += 1
                showerror("ERREUR", "Le robot est sorti de l'écran.")
            self.robot.rect.y = 3 + 70 * (self.robot.posY - 1)
    
    def right(self):
        self.robot.direction += 1
        if self.robot.direction == 4:
            self.robot.direction = 0
        if self.robot.direction == 0:
            if self.robot.strImage in ["files/robotD.png","files/robotB.png","files/robotG.png","files/robotH.png"]:
                self.robot.strImage = "files/robotD.png"
                self.robot.image = pygame.image.load("files/robotD.png")
        elif self.robot.direction == 1:
            if self.robot.strImage in ["files/robotD.png", "files/robotB.png", "files/robotG.png", "files/robotH.png"]:
                self.robot.strImage = "files/robotB.png"
                self.robot.image = pygame.image.load("files/robotB.png")
        elif self.robot.direction == 2:
            if self.robot.strImage in ["files/robotD.png","files/robotB.png","files/robotG.png","files/robotH.png"]:
                self.robot.strImage = "files/robotG.png"
                self.robot.image = pygame.image.load("files/robotG.png")
        elif self.robot.direction == 3:
            if self.robot.strImage in ["files/robotD.png","files/robotB.png","files/robotG.png","files/robotH.png"]:
                self.robot.strImage = "files/robotH.png"
                self.robot.image = pygame.image.load("files/robotH.png")
    
    def setAttack(self, boolean):
        self.robot.attack = boolean
    
    def setFunc(self, name, *instructions_f):
        if len(instructions_f) == 0:
            showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nLa fonction créée n'a pas d'instructions")
            pygame.quit()
        else:
            for i in instructions_f:
                if i.split("(")[0] in instructions:
                    pass
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nL'instruction "+i+" n'existe pas")
                    pygame.quit()
                    return
            self.fonctions[name] = instructions_f
    
    def callFunc(self, name):
        try:
            instructions_f = self.fonctions[name]
        except KeyError:
            showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nLa fonction "+name+" n'existe pas")
            pygame.quit()
        else:
            if self.temp_fonction_a_faire == 0:
                self.temp_fonction_a_faire = -1
            elif self.temp_fonction_a_faire == -1:
                self.temp_fonction_a_faire = len(instructions_f)
                self.avancement -= 1
            else:
                instruction = instructions_f[abs(self.temp_fonction_a_faire-len(instructions_f))]
                if instruction.split("(")[0] in instructions:
                    if instruction.split("(")[0] == "loop" or instruction.split("(")[0] == "loopif" :
                        self.temp_instruction = instruction.split("(")[0]
                        result = eval("self."+instruction)
                        self.avancement -= 1
                        if result:
                            self.temp_fonction_a_faire -= 1
                    else:
                        self.temp_instruction = instruction.split("(")[0]
                        eval("self."+instruction)
                        self.avancement -=1
                        self.temp_fonction_a_faire -= 1
                else:
                    showerror("ERREUR","Erreur sur l'instruction "+instruction+" de la fonction "+name+" appelée ligne n°"+str(self.avancement+1))
                    pygame.quit()
    
    def getAttack(self):
        return self.robot.attack
    
    def left(self):
        self.robot.direction -= 1
        if self.robot.direction == -1:
            self.robot.direction = 3
        if self.robot.direction == 0:
            if self.robot.strImage in ["files/robotD.png", "files/robotB.png", "files/robotG.png", "files/robotH.png"]:
                self.robot.strImage = "files/robotD.png"
                self.robot.image = pygame.image.load("files/robotD.png")
        elif self.robot.direction == 1:
            if self.robot.strImage in ["files/robotD.png", "files/robotB.png", "files/robotG.png", "files/robotH.png"]:
                self.robot.strImage = "files/robotB.png"
                self.robot.image = pygame.image.load("files/robotB.png")
        elif self.robot.direction == 2:
            if self.robot.strImage in ["files/robotD.png", "files/robotB.png", "files/robotG.png", "files/robotH.png"]:
                self.robot.strImage = "files/robotG.png"
                self.robot.image = pygame.image.load("files/robotG.png")
        elif self.robot.direction == 3:
            if self.robot.strImage in ["files/robotD.png", "files/robotB.png", "files/robotG.png", "files/robotH.png"]:
                self.robot.strImage = "files/robotH.png"
                self.robot.image = pygame.image.load("files/robotH.png")
                
    def setSprite(self, sprite= "files/robotD.png"):
        self.robot.strImage = sprite
        self.robot.image = pygame.image.load(sprite)
    
    def getSprite(self):
        return self.robot.strImage
    
    def getDirection(self):
        if self.robot.direction == 0:
            return "droite"
        elif self.robot.direction == 1:
            return "bas"
        elif self.robot.direction == 2:
            return "gauche"
        elif self.robot.direction == 3:
            return "haut"
    
    def getPosX(self):
        return self.robot.posX
    
    def getPosY(self):
        return self.robot.posY
    
    def getVar(self, name):
        if name in self.variables.keys():
            return self.variables[name]
        else:
            showerror("ERREUR","Erreur sur l'instruction de la ligne n°"+str(self.avancement+1)+"\nLa variable "+name+" n'est pas définie")
            pygame.quit()
    
    def setVar(self, name, value, sorte = "str"):
        if sorte == "str":
            try:
                for i in value.split(" "):
                    if i.split("(")[0] in instructions:
                        value = value.replace(i, str(eval("self."+i)))
                self.variables[name] = str(value)
            except:
                showerror("ERREUR","Erreur sur l'instruction de la ligne n°"+str(self.avancement+1)+"\nLa variable "+name+" n'est pas une chaine de caractères")
                pygame.quit()
        elif sorte == "int":
            try:
                result = 0
                if "+" in value.split(" "):
                    for i in value.split(" "):
                        if i != "+":
                            if i.split("(")[0] in instructions:
                                result += int(eval("self."+i))
                            else:
                                result += int(i)
                elif "-" in value.split(" "):
                    for i in value.split(" "):
                        if i != "-":
                            if i.split("(")[0] in instructions:
                                result -= int(eval("self."+i))
                            else:
                                result -= int(i)
                elif "*" in value.split(" "):
                    for i in value.split(" "):
                        if i != "*":
                            if i.split("(")[0] in instructions:
                                result *= int(eval("self."+i))
                            else:
                                result *= int(i)
                elif "/" in value.split(" "):
                    for i in value.split(" "):
                        if i != "/":
                            if i.split("(")[0] in instructions:
                                result /= int(eval("self."+i))
                            else:
                                result /= int(i)
                else:
                    result = value
                value = result
                self.variables[name] = int(value)
            except:
                showerror("ERREUR","Erreur sur l'instruction de la ligne n°"+str(self.avancement+1)+"\nLa variable "+name+" n'est pas un entier")
                pygame.quit()
        elif sorte == "float":
            try:
                result = 0
                if "+" in value.split(" "):
                    for i in value.split(" "):
                        if i != "+":
                            if i.split("(")[0] in instructions:
                                result += float(eval("self."+i))
                            else:
                                result += float(i)
                elif "-" in value.split(" "):
                    for i in value.split(" "):
                        if i != "-":
                            if i.split("(")[0] in instructions:
                                result -= float(eval("self."+i))
                            else:
                                result -= float(i)
                elif "*" in value.split(" "):
                    for i in value.split(" "):
                        if i != "*":
                            if i.split("(")[0] in instructions:
                                result *= float(eval("self."+i))
                            else:
                                result *= float(i)
                elif "/" in value.split(" "):
                    for i in value.split(" "):
                        if i != "/":
                            if i.split("(")[0] in instructions:
                                result /= float(eval("self."+i))
                            else:
                                result /= float(i)
                else:
                    result = value
                value = result
                self.variables[name] = float(value)
            except:
                showerror("ERREUR","Erreur sur l'instruction de la ligne n°"+str(self.avancement+1)+"\nLa variable "+name+" n'est pas un flottant")
                pygame.quit()
        else:
            showerror("ERREUR","Erreur sur l'instruction de la ligne n°"+str(self.avancement+1)+"\nLa variable "+name+" n'a pas un type connu")
            pygame.quit()
    
    def sayConsole(self, txt = "Bonjour"):
        for i in str(txt).split(" "):
            if i.split("(")[0] in instructions:
                txt = txt.replace(i, str(eval("self."+i)))
        print(txt)
    
    def loop(self, instruction = "walk()", nb = 1):
        if self.temp_boucle_a_faire == 0:
            if instruction.split("(")[0] in instructions:
                self.temp_instruction = instruction.split("(")[0]
            else:
                showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                pygame.quit()
            self.temp_boucle_a_faire = -1
            return 1
        elif self.temp_boucle_a_faire == -1:
            self.temp_boucle_a_faire = nb
            self.avancement -= 1
            return 0
        else:
            if instruction.split("(")[0] in instructions:
                self.temp_instruction = instruction.split("(")[0]
                eval("self."+instruction)
                self.avancement -=1
                self.temp_boucle_a_faire -= 1
                return 0
            else:
                showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                pygame.quit()
            
    def loopif(self, instruction = "walk()", condition = "True"):
        if condition.split("(")[0] in instructions:
            if eval("self."+condition):
                if instruction.split("(")[0] in instructions:
                    self.temp_instruction = instruction.split("(")[0]
                    eval("self."+instruction)
                    self.avancement -=1
                    self.temp_boucle_a_faire -= 1
                    return 0
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                    pygame.quit()
            else:
                if instruction.split("(")[0] in instructions:
                    self.temp_instruction = instruction.split("(")[0]
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                    pygame.quit()
                self.temp_boucle_a_faire = -1
                return 1
        else:
            if eval(condition):
                if instruction.split("(")[0] in instructions:
                    self.temp_instruction = instruction.split("(")[0]
                    eval("self."+instruction)
                    self.avancement -=1
                    self.temp_boucle_a_faire -= 1
                    return 0
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                    pygame.quit()
            else:
                if instruction.split("(")[0] in instructions:
                    self.temp_instruction = instruction.split("(")[0]
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la loop de la ligne n°"+str(self.avancement+1))
                    pygame.quit()
                self.temp_boucle_a_faire = -1
                return 1
    def if_(self, instruction, condition = "True"):
        if condition.split("(")[0] in instructions:
            if eval("self."+condition):
                if instruction.split("(")[0] in instructions:
                    self.temp_instruction = instruction.split("(")[0]
                    eval("self."+instruction)
                else:
                    showerror("ERREUR","Erreur sur l'instruction du if_ de la ligne n°"+str(self.avancement+1))
                    pygame.quit()
        else:
            if eval(condition):
                if instruction.split("(")[0] in instructions:
                    self.temp_instruction = instruction.split("(")[0]
                    eval("self."+instruction)
                else:
                    showerror("ERREUR","Erreur sur l'instruction du if_ de la ligne n°"+str(self.avancement+1))
                    pygame.quit()
