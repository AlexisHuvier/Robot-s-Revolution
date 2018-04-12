import pygame, sys
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import askquestion, showerror
from tkinter import *
try:
    from files.pathfinding.verifFunc import verif
except ImportError:
    sys.path.append("files/pathfinding")
    from verifFunc import verif
pygame.mixer.init()
temp_text = ""
mode = 0 #Mode parcours par défaut

def mouseEvent(button, pos):
    global mode
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
                        if mode == 0:
                            nb_temp = 0
                            for items in posAndObjects:
                                if items[0] == "files/finish.png":
                                    nb_temp += 1
                            if nb_temp == 1:
                                showerror(
                                    "ERREUR", "Vous êtes en mode Parcours et vous avez un drapeau sur le terrain")
                                find = True
                                pygame.mixer.music.load("files/negative.wav")
                                pygame.mixer.music.play()
                                break
                            else:
                                if askquestion("Attention", "Voulez-vous faire un niveau pour le mode Versus ?") == "yes":
                                    mode = 1
                                else:
                                    find = True
                                    pygame.mixer.music.load("files/negative.wav")
                                    pygame.mixer.music.play()
                                    break
                        else:
                            nb_temp = 0
                            for items in posAndObjects:
                                if items[0] == "files/robotB.png" or items[0] == "files/robotD.png" or items[0] == "files/robotG.png" or items[0] == "files/robotH.png":
                                    nb_temp += 1
                            if nb_temp == 2:
                                find = True
                                pygame.mixer.music.load("files/negative.wav")
                                pygame.mixer.music.play()
                                break
                    elif items[2][0] == posX and items[2][1] == posY:
                        posAndObjects.remove(items)
                        break
                if not find:
                    if objects[selectPos[0]-1] == "files/finish.png":
                        if mode == 1:
                            nb_temp = 0
                            for items in posAndObjects:
                                if items[0] == "files/robotB.png" or items[0] == "files/robotD.png" or items[0] == "files/robotG.png" or items[0] == "files/robotH.png":
                                    nb_temp += 1
                            if nb_temp == 2:
                                showerror("ERREUR", "Vous êtes en mode Versus et vous avez deux robots sur le terrain")
                                find = True
                                pygame.mixer.music.load("files/negative.wav")
                                pygame.mixer.music.play()
                            else:
                                if askquestion("Attention", "Voulez-vous faire un niveau pour le mode Parcours ?") == "yes":
                                    mode = 0
                                    posAndObjects.append([objects[selectPos[0]-1], offset[selectPos[0]-1],  [posX, posY]])
                                else:
                                    find = True
                                    pygame.mixer.music.load("files/negative.wav")
                                    pygame.mixer.music.play()
                        else:
                            posAndObjects.append([objects[selectPos[0]-1], offset[selectPos[0]-1], [posX, posY]])
                    else:
                        posAndObjects.append([objects[selectPos[0]-1], offset[selectPos[0]-1],  [posX, posY]])
    elif button == 3:
        posX = pos[0] // 70 + 1
        posY = pos[1] // 70 + 1
        if posY < 11:
            for items in posAndObjects:
                if items[2][0] == posX and items[2][1] == posY:
                    if items[0] == "files/robotB.png" or items[0] == "files/robotD.png" or items[0] == "files/robotG.png" or items[0] == "files/robotH.png":
                        nb_temp = 0
                        for items2 in posAndObjects:
                            if items2[0] == "files/robotB.png" or items2[0] == "files/robotD.png" or items2[0] == "files/robotG.png" or items2[0] == "files/robotH.png":
                                nb_temp += 1
                        if nb_temp == 2:
                            if mode == 1:
                                if askquestion("Attention", "Voulez-vous faire un niveau pour le mode Parcours ?") == "yes":
                                    mode = 0
                    posAndObjects.remove(items)
                    break

def validate():
    global EEasy, EMedium, EHard, temp_text, EHelp
    temp_text += EHelp.get() + "\n"
    for i in [EEasy, EMedium, EHard]:
        if i != EHard:
            temp_text += i.get() + ", "
        else:
            temp_text += i.get()+"\n"
    save()
        
def difficult():
    global EEasy, EMedium, EHard, difficultScreen, EHelp
    difficultScreen = Tk()
    difficultScreen.title("Difficulty")
    difficultScreen.geometry("180x230")

    LTitre = Label(difficultScreen, text="Robot's Revolution",
                    font=("Comic Sans MS", 13, "bold"))
    LHelp = Label(difficultScreen, text="Phrase d'aide :")
    EHelp = Entry(difficultScreen)
    LEasy = Label(difficultScreen, text="Nombre de ligne en Easy :")
    EEasy = Entry(difficultScreen)
    LMedium = Label(difficultScreen, text="Nombre de ligne en Medium :")
    EMedium = Entry(difficultScreen)
    LHard = Label(difficultScreen, text="Nombre de ligne en Hard :")
    EHard = Entry(difficultScreen)
    button = Button(difficultScreen, text="Validate",
                    command=validate)
    LTitre.pack()
    LHelp.pack()
    EHelp.pack()
    LEasy.pack()
    EEasy.pack()
    LMedium.pack()
    EMedium.pack()
    LHard.pack()
    EHard.pack()
    button.pack()
    difficultScreen.mainloop()

def save():
    global temp_text, difficultScreen

    filename = asksaveasfilename(title="Sauvegarder votre level",defaultextension = '.rev',filetypes=[('Revolt Files','.rev')])
    if filename != "":
        file = open(filename, "w")
        file.write(convertV(temp_text))
        file.close()
    try:
        difficultScreen.destroy()
    except NameError:
        pass

def convertV(texttemp):
    global fichier, mode
    nb_ennemi = 0
    nb_joueur = 0
    fichier = texttemp
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
            if mode == 1:
                print(nb_ennemi, nb_joueur)
                if nb_ennemi == 0 and nb_joueur == 0:
                    if askquestion("Type", "Voulez vous que le robot aux coordonnées ("+str(items[2][0])+";"+str(items[2][1])+") soit un ennemi ?") == "yes":
                        fichier += ", Ennemi"
                        nb_ennemi += 1
                    else:
                        fichier += ", Joueur"
                        nb_joueur += 1
                elif nb_ennemi == 0:
                    fichier += ", Ennemi"
                else:
                    fichier += ", Joueur"
            else:
                fichier += ", Joueur"
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
                if mode == 0:
                    if verif(posAndObjects) > 0:
                        difficult()
                        done = True
                    elif verif(posAndObjects) == -1:
                        showerror("ERREUR", "Il manque un robot et un drapeau de fin")
                    elif verif(posAndObjects) == -2:
                        showerror("ERREUR", "Il manque un robot de début")
                    elif verif(posAndObjects) == -3:
                        showerror("ERREUR", "Il manque un drapeau de fin")
                    else:
                        if askquestion("Attention", "Votre niveau n'est apparemment pas possible\nVoulez-vous quand même l'enregistrer ?") == "yes":
                            difficult()
                            done = True
                else:
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
