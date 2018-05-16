import pygame, threading, time
from html.parser import HTMLParser
from urllib.request import urlopen
from tkinter.messagebox import showerror

try:
    from files.python.RR_Class import *
except ImportError:
    from RR_Class import *

class Map():
    def __init__(self, objets, level, game, fichier="", ia = None):
        self.player_list = pygame.sprite.Group()
        self.finish_list = pygame.sprite.Group()
        self.rock_list = pygame.sprite.Group()
        self.lava_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.lazer_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()

        n = 0
        for i in objets:
            n += 1
            if i.split(", ")[0] == "0":
                pass
            elif i.split(", ")[0] == "player":
                try:
                    if game.mode == "IA" or game.mode == "Versus":
                        if i.split(", ")[4] == "Ennemi":
                            self.player = Player("Ennemi", "files/ia/"+str(ia)+".rev", game, level, self, int(i.split(", ")[3]))
                            self.player.posX = int(i.split(", ")[1])
                            self.player.posY = int(i.split(", ")[2])
                            self.player.rect.x = 20 + 70 * (self.player.posX - 1)
                            self.player.rect.y = 3 + 70 * (self.player.posY - 1)
                            self.player_list.add(self.player)
                        else:
                            self.player = Player("Joueur", fichier, game, level, self, int(i.split(", ")[3]))
                            self.player.posX = int(i.split(", ")[1])
                            self.player.posY = int(i.split(", ")[2])
                            self.player.rect.x = 20 + 70 * (self.player.posX - 1)
                            self.player.rect.y = 3 + 70 * (self.player.posY - 1)
                            self.player_list.add(self.player)
                    else:
                        self.player = Player("Joueur", fichier, game, level, self, int(i.split(", ")[3]))
                        self.player.posX = int(i.split(", ")[1])
                        self.player.posY = int(i.split(", ")[2])
                        self.player.rect.x = 20 + 70 * (self.player.posX - 1)
                        self.player.rect.y = 3 + 70 * (self.player.posY - 1)
                        self.player_list.add(self.player)
                except:
                    if game == "IA" or game == "Versus":
                        if i.split(", ")[4] == "Ennemi":
                            self.player = Player("Ennemi", fichier, game, level, self, int(i.split(", ")[3]))
                            self.player.posX = int(i.split(", ")[1])
                            self.player.posY = int(i.split(", ")[2])
                            self.player.rect.x = 20 + 70 * (self.player.posX - 1)
                            self.player.rect.y = 3 + 70 * (self.player.posY - 1)
                            self.player_list.add(self.player)
                        else:
                            self.player = Player("Joueur", fichier, game, level, self, int(i.split(", ")[3]))
                            self.player.posX = int(i.split(", ")[1])
                            self.player.posY = int(i.split(", ")[2])
                            self.player.rect.x = 20 + 70 * (self.player.posX - 1)
                            self.player.rect.y = 3 + 70 * (self.player.posY - 1)
                            self.player_list.add(self.player)
                    else:
                        self.player = Player("Joueur", fichier, game, level, self, int(i.split(", ")[3]))
                        self.player.posX = int(i.split(", ")[1])
                        self.player.posY = int(i.split(", ")[2])
                        self.player.rect.x = 20 + 70 * (self.player.posX - 1)
                        self.player.rect.y = 3 + 70 * (self.player.posY - 1)
                        self.player_list.add(self.player)
            elif i.split(", ")[0] == "finish":
                self.finish = Finish(
                    [int(i.split(", ")[1]), int(i.split(", ")[2])])
                self.finish_list.add(self.finish)
            elif i.split(", ")[0] == "rock":
                self.rock = Rock(
                    [int(i.split(", ")[1]), int(i.split(", ")[2])])
                self.rock_list.add(self.rock)
            elif i.split(", ")[0] == "lava":
                self.lava = Lava(
                    [int(i.split(", ")[1]), int(i.split(", ")[2])])
                self.lava_list.add(self.lava)
            elif i.split(", ")[0] == "wall":
                self.wall = Wall([int(i.split(", ")[1]), int(
                    i.split(", ")[2])], i.split(", ")[3])
                self.wall_list.add(self.wall)
            elif i.split(", ")[0] == "":
                pass
            else:
                showerror("ERREUR", "Le niveau " + str(level) +
                          " a un élément inconnu ("+i.split(", ")[0]+") (n°"+str(n)+")")

    def getObj(self, posX, posY):
        if self.player.posX == posX and self.player.posY == posY:
            return self.player
        elif self.finish.posX == posX and self.finish.posY == posY:
            return self.finish
        else:
            for i in self.rock_list:
                if i.posX == posX and i.posY == posY:
                    return i
            for i in self.lava_list:
                if i.posX == posX and i.posY == posY:
                    return i
            for i in self.wall_list:
                if i.posX == posX and i.posY == posY:
                    return i
            return None

    def createLazer(self, posX, posY, direction):
        self.lazer = Lazer(posX, posY, direction, self)
        self.lazer_list.add(self.lazer)
    
    def createBullet(self, posX, posY, direction):
        self.bullet = Bullet(posX, posY, direction, self)
        self.bullet_list.add(self.bullet)

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.getData = False
        self.result = []

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for i in attrs:
                if i[0]=="class" and i[1]=="level":
                    self.getData = True
                else:
                    self.getData = False
        if tag == "a":
            for i in range(0, len(attrs)):
                if attrs[i][0] == "class" and attrs[i][1] == "lien":
                    self.result.append(attrs[i+1][1])
                    
    
    def handle_endtag(self, tag):
        if tag == "div":
            self.getData = False

    def handle_data(self, data):
        if self.getData == True:
            if data != "- ":
                if " : " in data:
                    self.result.append(data.split(" : ")[1])
                else:
                    self.result.append(data)
    
    def get(self, text):
        resultF = self.getResult()
        resultTemp = []
        for i in resultF:
            resultTemp.append(i)
        for i in resultTemp:
            if i[7]=="Intelligence pour Versus" and text == "level":
                resultF.remove(i)
            elif i[7]=="Niveau pour Parcours" and text == "ia":
                resultF.remove(i)
        return resultF
    
    def getResult(self):
        nb = int(len(self.result)/8)
        resultF = []
        for i in range(nb):
            resultF.append([])
            for y in range(8):
                resultF[i].append(self.result[y])
            for i in range(8):
                self.result.remove(self.result[0])
        return resultF


class PreviewThread(threading.Thread):
    def __init__(self, level, tkinter, mode = "Textuel"):
        threading.Thread.__init__(self)
        self.level = level
        self.tkinter = tkinter
        self.mode = mode
        self.go = True
        self.ImageB = pygame.image.load("files/images/background.png")
    
    def run(self):
        self.screen = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Preview - Level "+str(self.level))
        try:
            with open("levels/"+str(self.level)+".rev", 'r') as fichier:
                lignes = fichier.read().split("\n")
                if self.tkinter.mode == "Parcours" or self.tkinter.mode == "Community": 
                    while lignes[0] == "" or lignes[0] == "\n":
                        lignes = lignes[1:]
                    if self.mode == "Textuel":
                        self.tkinter.aide = "#"+lignes[0]
                        self.tkinter.code.delete('1.0', 'end')
                        self.tkinter.code.insert("1.0", self.tkinter.aide)
                        self.tkinter.coloration()
                    lignes = lignes[2:]
                self.map = Map(lignes, self.level, self.tkinter.mode)
        except IOError:
            showerror("ERREUR", "Le fichier du level "+str(self.level)+" est inaccessible")
            pygame.quit()
        while self.go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.ImageB, [0, 0])
            self.map.player_list.draw(self.screen)
            self.map.rock_list.draw(self.screen)
            self.map.finish_list.draw(self.screen)
            self.map.lava_list.draw(self.screen)
            self.map.wall_list.draw(self.screen)
            self.clock.tick(60)
            pygame.display.update()
        pygame.quit()
    
    def stopThread(self):
        self.go = False

class TimeThread(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.game = game
        self.time = 0
        self.go = True
    
    def run(self):
        while self.go:
            time.sleep(1)
            self.time += 1
    
    def stopThread(self):
        self.go = False
        self.game.time = self.time


def downloadFile(name, info):
    try:
        url = "http://robot-s-revolution.fr.nf/upload/"+name+".rev"
        if info == "level":
            with open('levels/'+name+'.rev', 'w') as img:
                texte = urlopen(url)
                texte = texte.read().decode("utf-8")
                texte = texte.replace("\r", "")
                texte = texte.replace("\n", "\n")
                img.write(texte)
        if info == "ia":
            with open('files/ia/'+name+'.rev', 'w') as img:
                texte = urlopen(url)
                texte = texte.read().decode("utf-8")
                texte = texte.replace("\r", "")
                texte = texte.replace("\n", "\n")
                img.write(texte)
        return True
    except:
        return False