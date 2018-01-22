import pygame
from RR_language import *

class Player(pygame.sprite.Sprite):
			pygame.quit()
			result = 0
			showinfo("Perdu", "Votre robot a touché un caillou !")
    def __init__(self, fichier, level, map):
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
        self.timer = 10
        self.level = level
        self.map = map
    
    def update(self, collidable = pygame.sprite.Group(), collidable2 = pygame.sprite.Group()):
        self.timer -= 1
        result = 1
        if self.timer == 0:
            result = self.script.launch()
            self.timer = 10
        collision_list = pygame.sprite.spritecollide(self, self.map.rock_list, False, None)
        for collided_object in collision_list:
        collision_list_2 = pygame.sprite.spritecollide(self, self.map.finish_list, False, None)
        for collided_object in collision_list_2:
            pygame.quit()
            result = self.level + 1
            showinfo("Gagné", "Votre robot a atteint le point final !")
        return result

class Rock(pygame.sprite.Sprite):
    def __init__(self, pos = [10,10]):
        super(Rock, self).__init__()
        
        self.image = pygame.image.load("files/Caillou.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Finish(pygame.sprite.Sprite):
    def __init__(self, pos = [10,10]):
        super(Finish, self).__init__()
        
        self.image = pygame.image.load("files/finish.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Map():
    def __init__(self, objets, fichier, level):
        self.player = Player(fichier, level, self)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        self.finish_list = pygame.sprite.Group()
        self.rock_list = pygame.sprite.Group()
        self.player.rect.x = int(objets[0].split(",")[0])
        self.player.rect.y = int(objets[0].split(",")[1])
        self.finish = Finish([int(objets[len(objets)-1].split(",")[0]),int(objets[len(objets)-1].split(",")[1])])
        self.finish_list.add(self.finish)
        for i in range(1, len(objets)-1):
            self.rock = Rock([int(objets[i].split(",")[0]),int(objets[i].split(",")[1])])
            self.rock_list.add(self.rock)
        
