from tkinter.messagebox import showerror, showinfo
import pygame, sys
try:
    from files.RR_class import Map
except ImportError:
    from RR_class import Map


class Game():
    def __init__(self, script, mode, difficult = 0, level=1):
        self.result = 0
        self.difficult = difficult
        self.easy = 0
        self.medium = 0
        self.hard = 0
        self.nbInstruction = 0
        self.mode = mode

        self.screen = pygame.display.set_mode((700, 700))

        self.clock = pygame.time.Clock()

        self.done = True
        if self.mode == "Parcours" or self.mode == "IA":
            pygame.display.set_caption("RR - Level "+str(level))
            self.level = level
            self.mode = mode
            try:
                with open(script, "r") as fichier:
                    temp_instructions = fichier.read().split("\n")
                    for i in temp_instructions:
                        if i != "":
                            if i[0] != "#":
                                self.nbInstruction += 1
            except IOError as e:
                showerror("Fichier inconnu",
                          "Le fichier n'a pas pu être ouvert.")
                sys.exit()
            try:
                with open("levels/"+str(self.level)+".rev", 'r') as fichier:
                    lignes = fichier.read().split("\n")
                    if self.mode == "Parcours":
                        while lignes[0] == "" or lignes[0] == "\n":
                            lignes = lignes[1:]
                        self.easy, self.medium, self.hard = [
                            int(lignes[0].split(", ")[0]),
                            int(lignes[0].split(", ")[1]),
                            int(lignes[0].split(", ")[2])
                        ]
                        lignes = lignes[1:]
                    self.map = Map(lignes, level, self, script)
            except IOError:
                showerror("ERREUR", "Le fichier du level "+str(self.level)+" est inaccessible")
                pygame.quit()
            
        else:
            showerror("ERREUR", "MODE INCONNU")
            pygame.quit()
         
    def update(self):
        try:
            self.screen.fill((0, 0, 0))
            self.clock.tick(60)
            self.screen.blit(pygame.image.load("files/background.png"), [0, 0])
            self.map.rock_list.draw(self.screen)
            self.map.finish_list.draw(self.screen)
            self.map.lava_list.draw(self.screen)
            self.map.wall_list.draw(self.screen)
            self.map.player_list.draw(self.screen)
            self.map.lazer_list.draw(self.screen)
            self.map.bullet_list.draw(self.screen)
            pygame.display.update()
        except pygame.error:
            self.done = False
            self.result = 1

    def launch(self):
        while self.done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.done = False
                    self.result = 0
                if event.type == pygame.QUIT:
                    self.done = False
                    self.result = 0

            for character in self.map.player_list:
                if character.status == "Joueur":
                    self.result = character.update()
                else:
                    character.update()
            if self.result == 1:
                self.update()
            else:
                self.done = False
        pygame.quit()
        if self.mode == "Parcours":
            if ((self.difficult == 1 and self.nbInstruction <= self.easy) 
                or (self.difficult == 2 and self.nbInstruction <= self.medium) 
                or (self.difficult == 3 and self.nbInstruction <= self.hard)):
                if self.result > 1:
                    showinfo("Gagné", "Votre robot a atteint le point final !\nTemps d'exécution : XXs\nNombre d'instructions : "+str(self.nbInstruction)+"\nNombre minimum d'instruction (d'après le créateur du niveau) : "+str(self.hard))
                    return self.result
                else:
                    return self.level
            else:
                if self.difficult == 1:
                    showinfo(
                        "Désolé", "Votre robot a bien atteint le point final.\nMais la difficulté 'EASY' implique de faire ce parcours en "+str(self.easy)+" instructions")
                elif self.difficult == 2:
                    showinfo(
                        "Désolé", "Votre robot a bien atteint le point final.\nMais la difficulté 'MEDIUM' implique de faire ce parcours en "+str(self.medium)+" instructions")
                elif self.difficult == 3:
                    showinfo(
                        "Désolé", "Votre robot a bien atteint le point final.\nMais la difficulté 'HARD' implique de faire ce parcours en "+str(self.hard)+" instructions")
                return self.level
        elif self.mode == "IA":
            if len(self.map.player_list) == 1:
                showinfo("Gagné", "Votre robot a tué l'ennemi !\nTemps d'exécution : XXs\nNombre d'instructions : "+str(self.nbInstruction))
                return -12
            else:
                showinfo("Perdu", "Le robot ennemi n'a pas été tué")
                return self.level
