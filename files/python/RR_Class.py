import pygame
from tkinter.messagebox import showinfo, showerror, showwarning
try:
    from files.python.RR_Language import Script
    from files.python.RR_Utils import TimeThread
except ImportError:
    from RR_Language import Script
    from RR_Utils import TimeThread


class Player(pygame.sprite.Sprite):
    def __init__(self, status, fichier, game, level, carte, direction):
        super(Player, self).__init__()

        self.game = game
        self.status = status
        self.timeThread = None
        if fichier != "":
            self.script = Script(self, game, fichier)
            self.timeThread = TimeThread(self.game)
            self.timeThread.start()
        else:
            self.script = ""
        self.direction = direction
        if self.direction == 0:
            if self.status == "Joueur":
                self.strImage = "files/images/robotD.png"
            else:
                self.strImage = "files/images/RbtFCo2.png"
        elif self.direction == 1:
            if self.status == "Joueur":
                self.strImage = "files/images/robotB.png"
            else:
                self.strImage = "files/images/RbtF.png"
        elif self.direction == 2:
            if self.status == "Joueur":
                self.strImage = "files/images/robotG.png"
            else:
                self.strImage = "files/images/RbtFCo.png"
        elif self.direction == 3:
            if self.status == "Joueur":
                self.strImage = "files/images/robotH.png"
            else:
                self.strImage = "files/images/RbtFAr.png"
        self.image = pygame.image.load(self.strImage)
        self.rect = self.image.get_rect()
        self.attack = False
        self.posX = 1
        self.posY = 1
        self.rect.x = 10
        self.rect.y = 10
        self.tempPosX = self.posX
        self.tempPosY = self.posY
        try:
            with open("files/config.txt", "r") as fichier:
                lignes = fichier.read().split("\n")
                self.timerT = int(lignes[0].split(" : ")[1])
        except IOError:
            self.timerT = 20
            showwarning(
                "ATTENTION", "Le fichier de config n'a pas été trouvé et va être recréer")
            with open("files/config.txt", "w") as fichier:
                fichier.write("Timer Instruction : 20")
        self.timer = self.timerT
        self.level = level
        self.carte = carte

    def update(self):
        self.timer -= 1
        result = 1
        if self.timer == 0:
            if self.script != "":
                if self.status == "Joueur":
                    for bullet in self.carte.bullet_list:
                        bullet.update()
                else:
                    for lazer in self.carte.lazer_list:
                        lazer.update()
                result = self.script.launch()
            self.timer = self.timerT
        collision_list = pygame.sprite.spritecollide(
            self, self.carte.player_list, False, None)
        for collided_object in collision_list:
            if collided_object != self:
                self.script.last_instruction = ""
                self.posX = self.tempPosX
                self.posY = self.tempPosY
                self.rect.x = 20 + 70 * (self.posX - 1)
                self.rect.y = 3 + 70 * (self.posY - 1)
        collision_list = pygame.sprite.spritecollide(
            self, self.carte.lazer_list, False, None)
        for collided_object in collision_list:
            if self.status == "Joueur":
                if self.timeThread != None:
                    self.timeThread.stopThread()
                    self.timeThread.join()
                    self.timeThread = None
                pygame.quit()
                showinfo("Perdu", "Votre robot a percuté un lazer !")
        collision_list = pygame.sprite.spritecollide(
            self, self.carte.bullet_list, False, None
        )
        for collided_object in collision_list:
            if self.status == "Joueur":
                pass
            else:
                if self.timeThread != None:
                    self.timeThread.stopThread()
                    self.timeThread.join()
                    self.timeThread = None
                pygame.quit()
                self.carte.player_list.remove(self)
                result = self.level.split("_")[0] + str(int(self.level.split("_")[1])+1)
        collision_list = pygame.sprite.spritecollide(
            self, self.carte.lava_list, False, None)
        for collided_object in collision_list:
            if self.status == "Joueur":
                if self.timeThread != None:
                    self.timeThread.stopThread()
                    self.timeThread.join()
                    self.timeThread = None
                pygame.quit()
                showinfo("Perdu", "Votre robot a fondu dans la lave !")
            else:
                if self.timeThread != None:
                    self.timeThread.stopThread()
                    self.timeThread.join()
                    self.timeThread = None
                pygame.quit()
                self.carte.player_list.remove(self)
                result = self.level.split("_")[0] + str(int(self.level.split("_")[1])+1)
        if self.game != "" and (self.game.mode == "Parcours" or self.game.mode == "Community"):
            collision_list = pygame.sprite.spritecollide(
                self, self.carte.finish_list, False, None)
            for collided_object in collision_list:
                if self.timeThread != None:
                    self.timeThread.stopThread()
                    self.timeThread.join()
                    self.timeThread = None
                pygame.quit()
                if self.game.mode == "Parcours":
                    result = self.level + 1
                else:
                    result = 2
        collision_list = pygame.sprite.spritecollide(
            self, self.carte.rock_list, False, None)
        for collided_object in collision_list:
            self.script.last_instruction = ""
            self.posX = self.tempPosX
            self.posY = self.tempPosY
            self.rect.x = 20 + 70 * (self.posX - 1)
            self.rect.y = 3 + 70 * (self.posY - 1)
        collision_list = pygame.sprite.spritecollide(
            self, self.carte.wall_list, False, None)
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

        self.image = pygame.image.load("files/images/rocher.png")
        self.rect = self.image.get_rect()
        self.posX = pos[0]
        self.posY = pos[1]
        self.rect.x = 10 + 70 * (self.posX - 1)
        self.rect.y = 15 + 70 * (self.posY - 1)
        self.can_be_jump = True


class Finish(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Finish, self).__init__()

        self.image = pygame.image.load("files/images/finish.png")
        self.rect = self.image.get_rect()
        self.posX = pos[0]
        self.posY = pos[1]
        self.rect.x = 18 + 70 * (self.posX - 1)
        self.rect.y = 70 * (self.posY - 1)
        self.can_be_jump = False


class Lava(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Lava, self).__init__()

        self.image = pygame.image.load("files/images/lave.png")
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
            self.image = pygame.image.load("files/images/Mur.png")
            self.setPos(0, 35)
        elif sorte == "H":
            self.image = pygame.image.load("files/images/MurH.png")
            self.setPos(32, 0)
        elif sorte == "+":
            self.image = pygame.image.load("files/images/Mur+.png")
            self.setPos(0, 0)
        else:
            self.image = ""

        if self.image == "":
            pygame.quit()
            showerror("ERREUR", "Le type "+sorte +
                      " pour les murs n'est pas connu.")

    def setPos(self, offsetX, offsetY):
        self.rect = self.image.get_rect()
        self.rect.x = offsetX + 70 * (self.posX - 1)
        self.rect.y = offsetY + 70 * (self.posY - 1)


class Lazer(pygame.sprite.Sprite):
    def __init__(self, posX, posY, direction, map):
        super(Lazer, self).__init__()
        
        self.posX = posX
        self.posY = posY
        self.map = map
        self.direction = direction
        if direction == 0 or direction == 2:
            self.image = pygame.image.load("files/images/lazer.png")
            self.setPos()
        elif direction == 1 or direction == 3:
            self.image = pygame.image.load("files/images/lazer.png")
            self.image = pygame.transform.rotate(self.image, 90)
            self.setPos()
    
    def setPos(self):
        self.rect = self.image.get_rect()
        self.rect.x = 20 + 70 * (self.posX - 1)
        self.rect.y = 5 + 70 * (self.posY - 1)
    
    def update(self):
        if self.direction == 0:
            self.posX += 1
            if self.posX >= 11:
                self.map.lazer_list.remove(self)
            else:
                self.setPos()
        elif self.direction == 1:
            self.posY += 1
            if self.posY >= 11:
                self.map.lazer_list.remove(self)
            else:
                self.setPos()
        elif self.direction == 2:
            self.posX -= 1
            if self.posX <= 0:
                self.map.lazer_list.remove(self)
            else:
                self.setPos()
        elif self.direction == 3:
            self.posY -= 1
            if self.posY <= 0:
                self.map.lazer_list.remove(self)
            else:
                self.setPos()
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, posX, posY, direction, map):
        super(Bullet, self).__init__()
        
        self.posX = posX
        self.posY = posY
        self.map = map
        self.direction = direction
        self.image = pygame.image.load("files/images/bullet.png")
        if direction == 0:
            self.setPos()
        elif direction == 2:
            self.image = pygame.transform.rotate(self.image, 45)
            self.setPos()
        elif direction == 1:
            self.image = pygame.transform.rotate(self.image, 90)
            self.setPos()
        elif direction == 3:
            self.image = pygame.transform.rotate(self.image, 135)
            self.setPos()
    
    def setPos(self):
        self.rect = self.image.get_rect()
        self.rect.x = 20 + 70 * (self.posX - 1)
        self.rect.y = 20 + 70 * (self.posY - 1)
    
    def update(self):
        if self.direction == 0:
            self.posX += 1
            if self.posX >= 11:
                self.map.bullet_list.remove(self)
            else:
                self.setPos()
        elif self.direction == 1:
            self.posY += 1
            if self.posY >= 11:
                self.map.bullet_list.remove(self)
            else:
                self.setPos()
        elif self.direction == 2:
            self.posX -= 1
            if self.posX <= 0:
                self.map.bullet_list.remove(self)
            else:
                self.setPos()
        elif self.direction == 3:
            self.posY -= 1
            if self.posY <= 0:
                self.map.bullet_list.remove(self)
            else:
                self.setPos()