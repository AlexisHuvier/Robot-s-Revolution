import pygame, random, sys
from files.YR_class import *
from tkinter.messagebox import *


class Game():
	def __init__(self, fichier, mode, level = 1):
		pygame.init()
        
		self.result = 0
		self.mode = mode

		self.screen=pygame.display.set_mode((1200, 800))
		pygame.display.set_caption("Your Robot")

		self.clock=pygame.time.Clock()

		self.done = True
		if self.mode == "Parcours":
			self.level = level
			self.player = Player(fichier, self.level)
			self.mode = mode
			self.player_list = pygame.sprite.Group()
			self.player_list.add(self.player)
			self.finish_list = pygame.sprite.Group()
			self.rock_list = pygame.sprite.Group()
			try:
				with open("levels/"+str(self.level)+".yr", 'r') as fichier:
					lignes = fichier.read().split("\n")
					self.player.rect.x = int(lignes[0].split(",")[0])
					self.player.rect.y = int(lignes[0].split(",")[1])
					self.finish = Finish([int(lignes[len(lignes)-1].split(",")[0]),int(lignes[len(lignes)-1].split(",")[1])])
					self.finish_list.add(self.finish)
					for i in range(1, len(lignes)-1):
						self.rock = Rock([int(lignes[i].split(",")[0]),int(lignes[i].split(",")[1])])
						self.rock_list.add(self.rock)
			except IOError:
				showerror("ERREUR","Le fichier du level "+str(self.level)+" est inaccessible")
				pygame.quit()
		else:
			showerror("ERREUR","MODE INCONNU")
			pygame.quit()
        
	def launch(self):
		while self.done :
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.done = False
					self.result = 0
				if event.type == pygame.QUIT:
					self.done = False
					self.result = 0

			self.result = self.player.update(self.rock_list, self.finish_list)
            
			if self.result == 1:
				self.screen.fill((0,0,0))
				self.clock.tick(60)
				self.screen.blit(pygame.image.load("files/background.png"), [0,0])
				self.player_list.draw(self.screen)
				self.rock_list.draw(self.screen)
				self.finish_list.draw(self.screen)
				pygame.display.update()
			else:
				self.done = False
		pygame.quit()
		if self.result >= 1:
			return self.result
		else:
			return self.level
