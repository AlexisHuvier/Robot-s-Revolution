import pygame
from tkinter.messagebox import showinfo
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
        collision_list = pygame.sprite.spritecollide(self, self.carte.rock_list, False, None)
        for collided_object in collision_list:
            self.posX = self.tempPosX
            self.posY = self.tempPosY
            self.rect.x = 20 + 70 * (self.posX - 1) 
            self.rect.y = 3 + 70 * (self.posY - 1)
        collision_list_2 = pygame.sprite.spritecollide(self, self.carte.finish_list, False, None)
        for collided_object in collision_list_2:
            pygame.quit()
            result = self.level + 1
            showinfo("Gagné", "Votre robot a atteint le point final !")
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
        self.rect.x = 10 + 70 * (self.posX - 1)
        self.rect.y = 10 + 70 * (self.posY - 1)
        self.can_be_jump = False

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
            else:
                showerror("ERREUR", "Le niveau "+ level+" a un élément inconnu (n°"+n)
    
    def getObj(self, posX, posY):
        if self.player.posX == posX and self.player.posY == posY:
            return self.player
        elif self.finish.posX == posX and self.finish.posY == posY:
            return self.finish
        else:
            for i in self.rock_list:
                if i.posX == posX and i.posX == posY:
                    return i
            return None
        
