import pygame
from tkinter.messagebox import showinfo, showerror, showwarning
try:
    from files.RR_language import Script
except ImportError:
    from RR_language import Script


class Player(pygame.sprite.Sprite):
    def __init__(self, status, fichier, game, level, carte, direction):
        super(Player, self).__init__()

        self.game = game
        self.status = status
        if fichier != "":
            self.script = Script(self, game, fichier)
        else:
            self.script = ""
        self.direction = direction
        if direction == 0:
            self.strImage = "files/robotD.png"
        elif direction == 1:
            self.strImage = "files/robotB.png"
        elif direction == 2:
            self.strImage = "files/robotG.png"
        elif direction == 3:
            self.strImage = "files/robotH.png"
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
                pygame.quit()
                showinfo("Perdu", "Votre robot a percuté un lazer !")
        collision_list = pygame.sprite.spritecollide(
            self, self.carte.bullet_list, False, None
        )
        for collided_object in collision_list:
            if self.status == "Joueur":
                pass
            else:
                pygame.quit()
                self.carte.player_list.remove(self)
                result = self.level.split("_")[0] + str(int(self.level.split("_")[1])+1)
        collision_list = pygame.sprite.spritecollide(
            self, self.carte.lava_list, False, None)
        for collided_object in collision_list:
            if self.status == "Joueur":
                pygame.quit()
                showinfo("Perdu", "Votre robot a fondu dans la lave !")
            else:
                pygame.quit()
                result = self.level.split("_")[0] + str(int(self.level.split("_")[1])+1)
        if self.game != "" and self.game.mode == "Parcours":
            collision_list = pygame.sprite.spritecollide(
                self, self.carte.finish_list, False, None)
            for collided_object in collision_list:
                pygame.quit()
                result = self.level + 1
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
            self.image = pygame.image.load("files/lazer.png")
            self.setPos()
        elif direction == 1 or direction == 3:
            self.image = pygame.image.load("files/lazer.png")
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
        if direction == 0:
            self.image = pygame.image.load("files/bullet.png")
            self.setPos()
        elif direction == 2:
            self.image = pygame.image.load("files/bullet.png")
            self.image = pygame.transform.rotate(self.image, 45)
            self.setPos()
        elif direction == 1:
            self.image = pygame.image.load("files/bullet.png")
            self.image = pygame.transform.rotate(self.image, 90)
            self.setPos()
        elif direction == 3:
            self.image = pygame.image.load("files/bullet.png")
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

class Map():
    def __init__(self, objets, level, game, fichier=""):
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
                if game != "" and game.mode == "IA":
                    if i.split(", ")[4] == "Ennemi":
                        self.player = Player(i.split(", ")[4], "files/ia/"+str(level)+".rev", game, level, self, int(i.split(", ")[3]))
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
