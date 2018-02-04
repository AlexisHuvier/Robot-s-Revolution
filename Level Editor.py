import pygame, sys
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import askquestion
try:
    from files.pathfinding.verifFunc import verif
except ImportError:
    sys.path.append("files/pathfinding")
    from verifFunc import verif
pygame.mixer.init()

def mouseEvent(button, pos):
    if button == 1:
        posX = pos[0] // 70 + 1
        posY = pos[1] // 70 + 1
        if posY == 11:
            selectPos[0] = posX
        else:
            if len(posAndObjects) == 0:
                posAndObjects.append(
                    [objects[selectPos[0]-1], offset[selectPos[0]-1],  [posX, posY]])
            else:
                find = False
                for items in posAndObjects:
                    if items[0] == "files/finish.png" and objects[selectPos[0]-1] == "files/finish.png":
                        find = True
                        pygame.mixer.music.load("files/negative.wav")
                        pygame.mixer.music.play()
                        break
                    elif (items[0] == "files/robotB.png" or items[0] == "files/robotD.png" or items[0] == "files/robotG.png" or items[0] == "files/robotH.png") and (objects[selectPos[0]-1] == "files/robotB.png" or objects[selectPos[0]-1] == "files/robotD.png" or objects[selectPos[0]-1] == "files/robotG.png" or objects[selectPos[0]-1] == "files/robotH.png"):
                        find = True
                        pygame.mixer.music.load("files/negative.wav")
                        pygame.mixer.music.play()
                        break
                    elif items[2][0] == posX and items[2][1] == posY:
                        posAndObjects.remove(items)
                        posAndObjects.append(
                            [objects[selectPos[0]-1], offset[selectPos[0]-1],  [posX, posY]])
                        find = True
                        break
                if not find:
                    posAndObjects.append(
                        [objects[selectPos[0]-1], offset[selectPos[0]-1],  [posX, posY]])
    elif button == 3:
        posX = pos[0] // 70 + 1
        posY = pos[1] // 70 + 1
        if posY < 11:
            for items in posAndObjects:
                if items[2][0] == posX and items[2][1] == posY:
                    posAndObjects.remove(items)
                    break

def save():
    filename = asksaveasfilename(title="Sauvegarder votre level",defaultextension = '.rev',filetypes=[('Revolt Files','.rev')])
    if filename != "":
        file = open(filename, "w")
        file.write(convertV())
        file.close()
        
def convertV():
    fichier = ""
    for items in posAndObjects:
        if items[0] == "files/finish.png":
            fichier += "finish, "+str(items[2][0])+", "+str(items[2][1])
        elif items[0] == "files/lave.png":
            fichier += "lava, "+str(items[2][0])+", "+str(items[2][1])
        elif items[0] == "files/Mur.png" or items[0] == "files/Mur+.png" or items[0] == "files/MurH.png":
            fichier += "wall, "+str(items[2][0])+", "+str(items[2][1])
            if items[0] == "files/Mur.png":
                fichier += ", V"
            elif items[0] == "files/Mur+.png":
                fichier += ", +"
            elif items[0] == "files/MurH.png":
                fichier += ", H"
        elif items[0] == "files/robotB.png" or items[0] == "files/robotD.png" or items[0] == "files/robotG.png" or items[0] == "files/robotH.png":
            fichier += "player, "+str(items[2][0])+", "+str(items[2][1])
            if items[0] == "files/robotB.png":
                fichier += ", 1"
            elif items[0] == "files/robotD.png":
                fichier += ", 0"
            elif items[0] == "files/robotG.png":
                fichier += ", 2"
            elif items[0] == "files/robotH.png":
                fichier += ", 3"
        elif items[0] == "files/rocher.png":
            fichier += "rock, "+str(items[2][0])+", "+str(items[2][1])
        if items != posAndObjects[-1]:
            fichier += "\n"
    return fichier

offset = [[18,0], [20,3], [20,3],[20,3],[20,3],[10,15],[3,3],[0,35],[32,0],[0,0]]
objects = ["files/finish.png", "files/robotD.png", "files/robotB.png", "files/robotG.png", "files/robotH.png",
           "files/rocher.png", "files/lave.png", "files/Mur.png", "files/MurH.png", "files/Mur+.png"]
pos = [[0, 700], [70,700], [140,700], [210, 700], [280, 700], [350,700], [420,700], [490, 700], [560, 700], [630, 700]]
selectPos = [1, 11]
posAndObjects = []

editor = pygame.display.set_mode((700, 770))
pygame.display.set_caption("Level Editor")
clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_F5:
                if verif(posAndObjects) != 0:
                    save()
                    done = True
                else:
                    if askquestion("Attention", "Votre niveau n'est apparemment pas possible\nVoulez-vous quand même l'enregistrer ?") == "yes":
                        save()
                        done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseEvent(event.button, event.pos)
        if event.type == pygame.QUIT:
            done = True
    editor.fill((0, 0, 0))
    editor.blit(pygame.image.load("files/background.png"), [0, 0])

    for items in posAndObjects:
        editor.blit(pygame.image.load(items[0]), [
                    items[1][0]+(items[2][0] - 1) * 70, items[1][1]+(items[2][1] - 1) * 70])
    editor.blit(pygame.image.load("files/select.png"),
                [(selectPos[0] - 1) * 70, (selectPos[1] - 1) * 70])
    for i in range(0, 10):
        editor.blit(pygame.image.load(objects[i]), [offset[i][0]+pos[i][0], offset[i][1]+pos[i][1]])
    clock.tick(60)
    pygame.display.update()
pygame.quit()
