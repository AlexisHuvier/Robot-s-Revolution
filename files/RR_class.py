import pygame
from tkinter.messagebox import showinfo
try:
    from files.RR_language import Script
except ImportError:
    from RR_language import Script

class Player(pygame.sprite.Sprite):
    def __init__(self, fichier, level, carte):
        super(Player, self).__init__()
        
        self.strImage = "files/FlammyD.png"
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
        self.map = map
    
    def update(self):
        self.timer -= 1
        result = 1
        if self.timer == 0:
            result = self.script.launch()
            self.timer = 20
        collision_list = pygame.sprite.spritecollide(self, self.map.rock_list, False, None)
        for collided_object in collision_list:
            self.posX = self.tempPosX
            self.posY = self.tempPosY
            self.rect.x = 15 + 60 * (self.posX - 1) 
            self.rect.y = 10 + 60 * (self.posY - 1) 
        collision_list_2 = pygame.sprite.spritecollide(self, self.map.finish_list, False, None)
        for collided_object in collision_list_2:
            pygame.quit()
            result = self.level + 1
            showinfo("Gagné", "Votre robot a atteint le point final !")
        return result

class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Rock, self).__init__()
        
        self.image = pygame.image.load("files/Caillou.png")
        self.rect = self.image.get_rect()
        self.posX = pos[0]
        self.posY = pos[1]
        self.rect.x = 5 + 60 * (self.posX - 1) 
        self.rect.y = 5 + 60 * (self.posY - 1) 

class Finish(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Finish, self).__init__()
        
        self.image = pygame.image.load("files/finish.png")
        self.rect = self.image.get_rect()
        self.posX = pos[0]
        self.posY = pos[1]
        self.rect.x = 5 + 60 * (self.posX - 1) 
        self.rect.y = 5 + 60 * (self.posY - 1)

class Map():
    def __init__(self, objets, fichier, level):
        self.player = Player(fichier, level, self)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        self.finish_list = pygame.sprite.Group()
        self.rock_list = pygame.sprite.Group()
        self.player.posX = int(objets[0].split(",")[0])
        self.player.posY = int(objets[0].split(",")[1])
        self.player.rect.x = 15 + 60 * (self.player.posX - 1) 
        self.player.rect.y = 10 + 60 * (self.player.posY - 1) 
        self.finish = Finish([int(objets[len(objets)-1].split(",")[0]), int(objets[len(objets)-1].split(",")[1])])
        self.finish_list.add(self.finish)
        for i in range(1, len(objets)-1):
            self.rock = Rock([int(objets[i].split(",")[0]),int(objets[i].split(",")[1])])
            self.rock_list.add(self.rock)
    
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
        
