import pygame, sys
from tkinter.messagebox import showerror

instructions = ["walk", "left", "right", "jump", "getDirection", "setFunc", "callFunc",
                "getAttack", "setAttack", "setSprite", "getSprite", "setVar", "getVar",
                "loopif", "loop", "sayConsole", "if_", "getPosX", "getPosY", "shoot",
                "getEnnemyPosX", "getEnnemyPosY"]

class Script():
    """ Classe du script du robot"""
    def __init__(self, robot, game, fichier):
        """Initialisation du script"""
        self.fichier = fichier
        self.robot = robot
        self.game = game
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
            showerror("Fichier inconnu", "Le fichier "+self.fichier+" n'a pas pu être ouvert.")
            sys.exit()
        else:
            with open(self.fichier, 'r') as fichier:
                self.instruction = fichier.read().split("\n")

    def launch(self):
        """Lance une instruction"""
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
            elif self.instruction[self.avancement][0] == "#":
                self.avancement += 1
                return 1
            else:
                showerror("ERREUR", "Erreur sur l'instruction à la ligne n°"+str(self.avancement+1))
                pygame.quit()
                return 0
        else:
            return 1
    
    def getEnnemyPosX(self):
        """Récupère la position X de l'ennemi"""
        for i in self.robot.carte.player_list:
            if i.status != self.robot.status:
                return i.posX
    
    def getEnnemyPosY(self):
        """ Récupère la position Y de l'ennemi"""
        for i in self.robot.carte.player_list:
            if i.status != self.robot.status:
                return i.posY
    
    def shoot(self):
        """Fait tirer le robot"""
        if self.robot.attack:
            if self.robot.status == "Joueur":
                self.robot.carte.createBullet(self.robot.posX, self.robot.posY, self.robot.direction)
            else:
                self.robot.carte.createLazer(self.robot.posX, self.robot.posY, self.robot.direction)

    def jump(self):
        """Fait sauter le robot"""
        if self.last_instruction == "walk" or self.last_instruction == "jump":
            self.robot.tempPosX = self.robot.posX
            self.robot.tempPosY = self.robot.posY
            if self.robot.direction == 0:
                if self.robot.carte.getObj(self.robot.posX + 1, self.robot.posY).can_be_jump:
                    self.robot.posX += 2
                    if self.robot.posX > 10:
                        self.robot.posX -= 2
                        showerror("ERREUR", "Le robot est sorti de l'écran.")
                    else:
                        self.robot.posX -= 2
                        self.robot.posX += 1
                        self.robot.rect.x = 20 + 70 * (self.robot.posX - 1)
                        self.robot.rect.y -= 30
                        self.game.update()
                        pygame.time.wait(500)
                        self.robot.posX += 1
                        self.robot.rect.x = 20 + 70 * (self.robot.posX - 1)
                        self.robot.rect.y += 30
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nOn ne peut jump que les cailloux")
            elif self.robot.direction == 1:
                if self.robot.carte.getObj(self.robot.posX, self.robot.posY + 1).can_be_jump:
                    self.robot.posY += 2
                    if self.robot.posY > 10:
                        self.robot.posY -= 2
                        showerror("ERREUR", "Le robot est sorti de l'écran.")
                    self.robot.rect.y = 3 + 70 * (self.robot.posY - 1)
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nOn ne peut jump que les cailloux")
            elif self.robot.direction == 2:
                if self.robot.carte.getObj(self.robot.posX - 1, self.robot.posY).can_be_jump:
                    self.robot.posX -= 2
                    if self.robot.posX < 1:
                        self.robot.posX += 2
                        showerror("ERREUR", "Le robot est sorti de l'écran.")
                    self.robot.rect.x  = 20 + 70 * (self.robot.posX - 1)
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nOn ne peut jump que les cailloux")
            elif self.robot.direction == 3:
                if self.robot.carte.getObj(self.robot.posX, self.robot.posY - 1).can_be_jump:
                    self.robot.posY -= 2
                    if self.robot.posY < 1:
                        self.robot.posY += 2
                        showerror("ERREUR", "Le robot est sorti de l'écran.")
                    self.robot.rect.y = 3 + 70 * (self.robot.posY - 1)
                else:
                    showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nOn ne peut jump que les cailloux")
        else:
            print(self.last_instruction)
            showerror("ERREUR","Erreur sur l'instruction à la ligne n°"+str(self.avancement+1)+"\nIl n'est pas possible d'utiliser 'jump()' s'il n'y a pas un 'walk()' avant")

    def walk(self):
        """ Faire avancer le robot"""
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
        """ Tourner le robot à droite """
        self.robot.direction += 1
        if self.robot.direction == 4:
            self.robot.direction = 0
        if self.robot.direction == 0:
            if self.robot.strImage in ["files/robotD.png","files/robotB.png","files/robotG.png","files/robotH.png"]:
                self.robot.strImage = "files/robotD.png"
                self.robot.image = pygame.image.load("files/robotD.png")
            else:
                self.robot.strImage = "files/RbtFCo2.png"
                self.robot.image = pygame.image.load("files/RbtFCo2.png")
        elif self.robot.direction == 1:
            if self.robot.strImage in ["files/robotD.png", "files/robotB.png", "files/robotG.png", "files/robotH.png"]:
                self.robot.strImage = "files/robotB.png"
                self.robot.image = pygame.image.load("files/robotB.png")
            else:
                self.robot.strImage = "files/RbtF.png"
                self.robot.image = pygame.image.load("files/RbtF.png")
        elif self.robot.direction == 2:
            if self.robot.strImage in ["files/robotD.png","files/robotB.png","files/robotG.png","files/robotH.png"]:
                self.robot.strImage = "files/robotG.png"
                self.robot.image = pygame.image.load("files/robotG.png")
            else:
                self.robot.strImage = "files/RbtFCo.png"
                self.robot.image = pygame.image.load("files/RbtFCo.png")
        elif self.robot.direction == 3:
            if self.robot.strImage in ["files/robotD.png","files/robotB.png","files/robotG.png","files/robotH.png"]:
                self.robot.strImage = "files/robotH.png"
                self.robot.image = pygame.image.load("files/robotH.png")
            else:
                self.robot.strImage = "files/RbtFAr.png"
                self.robot.image = pygame.image.load("files/RbtFAr.png")

    def setAttack(self, boolean):
        """ Activer ou désactiver le mode attaque du robot """
        self.robot.attack = boolean

    def setFunc(self, name, *instructions_f):
        """ Créer une fonction <name> composé des instructions <*instructions_f>"""
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
        """ Lancer la fonction <name>"""
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
        """ Récupère si le robot est en mode attaque """
        return self.robot.attack

    def left(self):
        """ Tourner le robot a gauche """
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
        """ Changer le sprite du robot"""
        self.robot.strImage = sprite
        self.robot.image = pygame.image.load(sprite)

    def getSprite(self):
        """ Récupérer le sprite du robot"""
        return self.robot.strImage

    def getDirection(self):
        """ Récupérer la direction du robot"""
        if self.robot.direction == 0:
            return "droite"
        elif self.robot.direction == 1:
            return "bas"
        elif self.robot.direction == 2:
            return "gauche"
        elif self.robot.direction == 3:
            return "haut"

    def getPosX(self):
        """ Récupérer la position X du robot"""
        return self.robot.posX

    def getPosY(self):
        """ Récupérer la position Y du robot"""
        return self.robot.posY

    def getVar(self, name):
        """ Récupérer la variable <name>"""
        if name in self.variables.keys():
            return self.variables[name]
        else:
            showerror("ERREUR","Erreur sur l'instruction de la ligne n°"+str(self.avancement+1)+"\nLa variable "+name+" n'est pas définie")
            pygame.quit()

    def setVar(self, name, value, sorte = "str"):
        """ Créer la variable <name> avec la valeur <value> et de type <sorte>"""
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
        """ Print quelque chose"""
        for i in str(txt).split(" "):
            if i.split("(")[0] in instructions:
                txt = txt.replace(i, str(eval("self."+i)))
        print(txt)

    def loop(self, instruction = "walk()", nb = 1):
        """ Créer une boucle qui fait <instruction> <nb> fois"""
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
        """ Créer une boucle qui fait <instruction> tant que <condition> vraie"""
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
        """ Faire <instruction> si <condition> vraie"""
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
