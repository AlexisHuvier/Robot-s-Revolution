import pygame
from files.YR_language import *

class Player(pygame.sprite.Sprite):
	def __init__(self, fichier, level):
		super(Player, self).__init__()
		
		self.strImage = "files/FlammyD.png"
		self.image = pygame.image.load(self.strImage)
		self.rect = self.image.get_rect()
		self.rect.x = 10
		self.rect.y = 10
		self.script = Script(self, fichier)
		self.direction = 0
		self.posX = 1
		self.posY = 1
		self.timer = 10
		self.level = level
	
	def update(self, collidable = pygame.sprite.Group(), collidable2 = pygame.sprite.Group()):
		self.timer -= 1
		result = 1
		if self.timer == 0:
			result = self.script.launch()
			self.timer = 10
		collision_list = pygame.sprite.spritecollide(self, collidable, False, None)
		for collided_object in collision_list:
			pygame.quit()
			result = 0
			showinfo("Perdu", "Votre robot a touché un caillou !")
		collision_list_2 = pygame.sprite.spritecollide(self, collidable2, False, None)
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
