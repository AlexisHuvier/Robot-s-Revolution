from tkinter.messagebox import showerror
import pygame
try:
    from files.RR_class import Map
except ImportError:
    from RR_class import Map


class Game():
    def __init__(self, script, mode, level=1):
        self.result = 0
        self.mode = mode

        self.screen = pygame.display.set_mode((700, 700))

        self.clock = pygame.time.Clock()

        self.done = True
        if self.mode == "Parcours":
            pygame.display.set_caption("RR - Level "+str(level))
            self.level = level
            self.mode = mode
            try:
                with open("levels/"+str(self.level)+".rev", 'r') as fichier:
                    lignes = fichier.read().split("\n")
                    self.map = Map(lignes, level, self, script)
            except IOError:
                showerror("ERREUR", "Le fichier du level "+str(self.level)+" est inaccessible")
                pygame.quit()
        else:
            showerror("ERREUR", "MODE INCONNU")
            pygame.quit()
         
    def update(self):
        self.screen.fill((0, 0, 0))
        self.clock.tick(60)
        self.screen.blit(pygame.image.load("files/background.png"), [0, 0])
        self.map.rock_list.draw(self.screen)
        self.map.finish_list.draw(self.screen)
        self.map.lava_list.draw(self.screen)
        self.map.wall_list.draw(self.screen)
        self.map.player_list.draw(self.screen)
        pygame.display.update()

    def launch(self):
        while self.done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.done = False
                    self.result = 0
                if event.type == pygame.QUIT:
                    self.done = False
                    self.result = 0

            self.result = self.map.player.update()

            if self.result == 1:
                self.update()
            else:
                self.done = False
        pygame.quit()
        if self.result > 1:
            return self.result
        else:
            return self.level
