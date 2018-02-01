import pygame
from tkinter.messagebox import showinfo, showerror
try:
    from files.RR_language import Script
except ImportError:
    from RR_language import Script

class Player(pygame.sprite.Sprite):
    def __init__(self, fichier, level, carte):
        super(Player, self).__init__()
        
        self.strImage = "files/robotD.png"
        self.image = pygame.image.load(self.strImage)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.script = Script(self, fichier)
        self.direction = 0
        self.attack = False
        self.posX = 1
        self.posY = 1
        self.tempPosX = self.posX
        self.tempPosY = self.posY
        self.timer = 20
        self.level = level
        self.carte = carte
    
    def update(self):
        self.timer -= 1
        result = 1
        if self.timer == 0:
            result = self.script.launch()
            self.timer = 20
        collision_list = pygame.sprite.spritecollide(self, self.carte.lava_list, False, None)
        for collided_object in collision_list:
            pygame.quit()
            showinfo("Perdu", "Votre robot a fondu dans la lave !")
        collision_list = pygame.sprite.spritecollide(self, self.carte.finish_list, False, None)
        for collided_object in collision_list:
            pygame.quit()
            result = self.level + 1
            showinfo("Gagné", "Votre robot a atteint le point final !")
        collision_list = pygame.sprite.spritecollide(self, self.carte.rock_list, False, None)
        for collided_object in collision_list:
            self.script.last_instruction = ""
            self.posX = self.tempPosX
            self.posY = self.tempPosY
            self.rect.x = 20 + 70 * (self.posX - 1) 
            self.rect.y = 3 + 70 * (self.posY - 1)
        collision_list = pygame.sprite.spritecollide(self, self.carte.wall_list, False, None)
        for collided_object in collision_list:
            self.script.last_instruction = ""
            self.posX = self.tempPosX
            self.posY = self.tempPosY
            self.rect.x = 20 + 70 * (self.posX - 1)
            self.rect.y = 3 + 70 * (self.posY - 1)
        return result

class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Rock, self).__init__()
        
        self.image = pygame.image.load("files/rocher.png")
        self.rect = self.image.get_rect()
        self.posX = pos[0]
        self.posY = pos[1]
        self.rect.x = 10 + 70 * (self.posX - 1)
        self.rect.y = 15 + 70 * (self.posY - 1)
        self.can_be_jump = True

class Finish(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Finish, self).__init__()
        
        self.image = pygame.image.load("files/finish.png")
        self.rect = self.image.get_rect()
        self.posX = pos[0]
        self.posY = pos[1]
        self.rect.x = 18 + 70 * (self.posX - 1)
        self.rect.y = 70 * (self.posY - 1)
        self.can_be_jump = False
    
class Lava(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Lava, self).__init__()

        self.image = pygame.image.load("files/lave.png")
        self.rect = self.image.get_rect()
        self.posX = pos[0]
        self.posY = pos[1]
        self.rect.x = 3 + 70 * (self.posX - 1)
        self.rect.y = 3 + 70 * (self.posY - 1)
        self.can_be_jump = True

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, sorte):
        super(Wall, self).__init__()

        self.posX = pos[0]
        self.posY = pos[1]
        self.can_be_jump = False
        if sorte == "V":
            self.image = pygame.image.load("files/Mur.png")
            self.setPos(0, 35)
        elif sorte == "H":
            self.image = pygame.image.load("files/MurH.png")
            self.setPos(32, 0)  
        elif sorte == "+":
            self.image = pygame.image.load("files/Mur+.png")
            self.setPos(0, 0)
        else:
            self.image = ""
        
        if self.image == "":
            pygame.quit()
            showerror("ERREUR", "Le type "+sorte+" pour les murs n'est pas connu.")
    
    def setPos(self, offsetX, offsetY):
        self.rect = self.image.get_rect()
        self.rect.x = offsetX + 70 * (self.posX - 1)
        self.rect.y = offsetY + 70 * (self.posY - 1)


class Map():
    def __init__(self, objets, fichier, level):
        self.player_list = pygame.sprite.Group()
        self.finish_list = pygame.sprite.Group()
        self.rock_list = pygame.sprite.Group()
        self.lava_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()

        n=0
        for i in objets:
            n+=1
            if i.split(", ")[0] == "player":
                self.player = Player(fichier, level, self)
                self.player.posX = int(i.split(", ")[1])
                self.player.posY = int(i.split(", ")[2])
                self.player.rect.x = 20 + 70 * (self.player.posX - 1)
                self.player.rect.y = 3 + 70 * (self.player.posY - 1)
                self.player_list.add(self.player)
            elif i.split(", ")[0] == "finish":
                self.finish = Finish([int(i.split(", ")[1]), int(i.split(", ")[2])])
                self.finish_list.add(self.finish)
            elif i.split(", ")[0] == "rock":
                self.rock = Rock([int(i.split(", ")[1]), int(i.split(", ")[2])])
                self.rock_list.add(self.rock)
            elif i.split(", ")[0] == "lava":
                self.lava=Lava([int(i.split(", ")[1]), int(i.split(", ")[2])])
                self.lava_list.add(self.lava)
            elif i.split(", ")[0] == "wall":
                self.wall = Wall([int(i.split(", ")[1]), int(i.split(", ")[2])], i.split(", ")[3])
                self.wall_list.add(self.wall)
            else:
                showerror("ERREUR", "Le niveau "+ level+" a un élément inconnu (n°"+n)
    
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
        
