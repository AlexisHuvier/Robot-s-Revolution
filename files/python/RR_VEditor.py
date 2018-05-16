from tkinter import *
from tkinter.messagebox import showerror, showinfo, askquestion, showwarning
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import pygame, glob, random
try:
    from files.python.RR_Game import Game
    from files.python.RR_Utils import PreviewThread, Map
except ImportError:
    from RR_Utils import PreviewThread, Map
    from RR_Game import Game

class VEditor(Tk):
    """Editeur de script"""
    def __init__(self, level, mode, ia = None):
        super(VEditor, self).__init__()
        self.visuel = True
        self.dOn = False
        self.preview = None
        self.mode = mode
        self.difficultScreen = ""
        self.difficult = "MP"
        self.aide = ""
        self.blockInit = [["walk", ImageTk.PhotoImage(Image.open("files/images/bloc.png"))],
                        ["left", ImageTk.PhotoImage(Image.open("files/images/bloc.png"))],
                        ["right", ImageTk.PhotoImage(Image.open("files/images/bloc.png"))],
                        ["jump", ImageTk.PhotoImage(Image.open("files/images/bloc.png"))]
        ]
        self.blockList = [["blockD", ImageTk.PhotoImage(Image.open("files/images/blocD.png"))]]
        self.on = True
        self.levels = []
        self.xInit = 75
        self.yInit = 45
        try:
            with open("files/saves.txt", "r") as fichier:
                temp = fichier.read().split("\n")
                for i in temp:
                    self.levels.append(i.split(" - "))
        except IOError:
            showwarning("ATTENTION", "Le fichier des sauvegardes n'a pas été trouvé et va être recréer")
            with open("files/saves.txt", "w") as fichier:
                fichier.write("Mode - Nom - Difficulté - NombreLigne")
        if self.mode == "IA" or self.mode == "Versus":
            nb = len(glob.glob("levels/mp_*.rev"))
            if nb == 1 or nb == 0:
                self.level = "mp_1"
            else:
                self.level = "mp_"+str(random.randint(1, nb))
            if ia == None:
                self.ia = "ia_1"
            else:
                self.ia = ia
            while True:
                find = False
                for i in self.levels:
                    if i[0] == self.mode:
                        if str(self.ia) == i[1]:
                            find = True
                            if askquestion("Jouer", "Vous avez déjà battu "+i[1]+ " avec "+i[3]+" lignes de codes.\nVoulez vous rejouer ?") == "yes":
                                find = False
                                break
                            else:
                                if "ia_" in self.ia:
                                    self.ia = "ia_"+str(int(self.ia[3:])+1)
                                    try:
                                        with open("files/ia/"+self.ia+".rev"):
                                            pass
                                    except:
                                        showerror("ERREUR", "Il n'y a plus d'IA à battre")
                                        showinfo("Fermeture", "Fermeture du jeu")
                                        self.on = False
                                        self.destroy()
                                        if self.preview != None:
                                            self.preview.stopThread()
                                            self.preview.join()
                                            self.preview = None
                                else:
                                    showinfo("Fermeture", "Fermeture du jeu")
                                    self.on = False
                                    self.destroy()
                                    if self.preview != None:
                                        self.preview.stopThread()
                                        self.preview.join()
                                        self.preview = None
                if find == False:
                    break

        else:
            self.level = level
            while True:
                find = False
                for i in self.levels:
                    if i[0] == self.mode:
                        if str(self.level) == i[1]:
                            find = True
                            if askquestion("Jouer", "Vous avez fini le level "+i[1]+ " avec "+i[3]+" lignes de codes.\nVoulez vous rejouer ?") == "yes":
                                find = False
                                break
                            else:
                                if self.mode == "Parcours":
                                    self.level = self.level+1
                                    try:
                                        with open("levels/"+str(self.level)+".rev"):
                                            pass
                                    except:
                                        showerror("ERREUR", "Il n'y a plus de niveau")
                                        self.quitter()
                if find == False:
                    break
        self.title("Revolt IDE - Untitled")

        self.show = Canvas(self, width=926, height=624, bg='black')
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Nouveau", command=self.creer)
        self.menu1.add_command(label="Ouvrir", command=self.ouvrir)
        self.menu1.add_command(label="Sauvegarder", command=self.sauvegarde)
        self.menu1.add_command(label="Exécuter", command=self.execute)
        self.menu1.add_command(label="Mode Textuel", command=self.textMode)
        self.menubar.add_cascade(label="Fichier", menu=self.menu1)
        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="A propos", command=self.apropos)
        self.menubar.add_cascade(label="Info", menu=self.menu2)
        
        self.show.grid(row=0, column=0, sticky="NSEW")

        self.bind_all("<Control-KeyPress-o>", self.ouvrir)
        self.bind_all("<Control-KeyPress-n>", self.creer)
        self.bind_all("<Control-KeyPress-i>", self.apropos)
        self.bind_all("<Control-KeyPress-s>", self.sauvegarde)
        self.bind_all("<Control-KeyPress-m>", self.textMode)
        self.bind_all("<KeyPress-F5>", self.execute)
        self.show.bind("<Button-1>", lambda x: self.selectBlock(x))
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.config(menu=self.menubar)

        self.showBlocks()

        self.previewLevel(self.level)

        self.mainloop()
    
    def selectBlock(self, evt):
        bloc = ""
        if evt.x >= 509 and evt.x <= 642:
            if evt.y >= 28 and evt.y <= 62:
                bloc = "walk"
            elif evt.y >= 74 and evt.y <= 108:
                bloc = "left"
            elif evt.y >= 118 and evt.y <= 154:
                bloc = "right"
            elif evt.y >= 166 and evt.y <= 196:
                bloc = "jump"
        elif evt.x >= 811 and evt.x <= 890 and evt.y >= 504 and evt.y <= 595:
            if len(self.blockList) > 1:
                if self.title()[0] != "*":
                    self.title("*"+self.title())
                if len(self.blockList) > 2:
                    self.blockList[len(self.blockList)-2] = [self.blockList[len(self.blockList)-2][0],ImageTk.PhotoImage(Image.open("files/images/blocF.png"))]
                del self.blockList[len(self.blockList)-1]
                self.showBlocks()
        if bloc != "":
            if self.title()[0] != "*":
                self.title("*"+self.title())
            if len(self.blockList) == 1:
                self.blockList.append([bloc, ImageTk.PhotoImage(Image.open("files/images/blocF.png"))])
            else:
                self.blockList[len(self.blockList)-1] = [self.blockList[len(self.blockList)-1][0],ImageTk.PhotoImage(Image.open("files/images/blocM.png"))]
                self.blockList.append([bloc, ImageTk.PhotoImage(Image.open("files/images/blocF.png"))])
            self.showBlocks()
    

    def textMode(self, evt = None):
        """ Passage en mode Visuel"""
        if askquestion("Revolt IDE", "Voulez-vous enregistrer ?\nNe pas enregistrer vous fera perdre ce script")=="yes":
            self.sauvegarde() 
        self.on = False
        self.visuel = False
        self.destroy()
        if self.preview != None:
            self.preview.stopThread()
            self.preview.join()
            self.preview = None
    
    def CloseDifficult(self):
        """ Fermeture du screen de la difficulté"""
        if self.difficultScreen != "":
            self.dOn = False
            self.difficultScreen.destroy()
    
    def previewLevel(self, level):
        """ Preview du level <level>"""
        self.preview = PreviewThread(level, self, "Visuel")
        self.preview.start()
    
    def showBlocks(self):
        self.bgVisuel=ImageTk.PhotoImage(Image.open("files/images/visuel.png"))
        self.show.create_image(463, 312, image = self.bgVisuel)
        self.poub=ImageTk.PhotoImage(Image.open("files/images/poubelle.png"))
        self.show.create_image(850, 550, image = self.poub)
        for i in range(0, len(self.blockInit)):
            self.show.create_image(self.xInit+500, self.yInit*(i+1), image = self.blockInit[i][1])
            self.show.create_text(self.xInit+500, self.yInit*(i+1), text=self.blockInit[i][0], font=("Times New Roman", 25, "bold"), fill = '#000000')
        for i in range(0,len(self.blockList)):
            if i>= 45:
                showerror("ERREUR", "Le nombre de bloc dépasse 45. A partir de maintenant, les blocs ne seront plus affiché.")
            elif i>=30:
                self.show.create_image(self.xInit+300, self.yInit*(i+1-30)-5*(i+1-30), image = self.blockList[i][1])
                if self.blockList[i][0] != "blockD":
                    self.show.create_text(self.xInit+300, self.yInit*(i+1-30)-5*(i+1-30), text=self.blockList[i][0], font=("Times New Roman", 25, "bold"), fill = '#000000')
            elif i>=15:
                self.show.create_image(self.xInit+150, self.yInit*(i+1-15)-5*(i+1-15), image = self.blockList[i][1])
                if self.blockList[i][0] != "blockD":
                    self.show.create_text(self.xInit+150, self.yInit*(i+1-15)-5*(i+1-15), text=self.blockList[i][0], font=("Times New Roman", 25, "bold"), fill = '#000000')
            else:
                self.show.create_image(self.xInit, self.yInit*(i+1)-5*(i+1), image = self.blockList[i][1])
                if self.blockList[i][0] != "blockD":
                    self.show.create_text(self.xInit, self.yInit*(i+1)-5*(i+1), text=self.blockList[i][0], font=("Times New Roman", 25, "bold"), fill = '#000000')
    
    def convertToText(self, liste):
        text = ''
        for i in liste:
            if i[0] != "blockD":
                text += i[0]+"()\n"
        return text[:-1]
    
    def convertToVisuel(self, content):
        self.blockList = [["blockD", ImageTk.PhotoImage(Image.open("files/images/blocD.png"))]]
        listContent = content.split("\n")
        for i in range(len(listContent)):
            if i == len(listContent)-1:
                self.blockList.append([listContent[i].split("(")[0], ImageTk.PhotoImage(Image.open("files/images/blocF.png"))])
            else:
                self.blockList.append([listContent[i].split("(")[0], ImageTk.PhotoImage(Image.open("files/images/blocM.png"))])

    def Jouer(self, name):
        """ Lancer le jeu"""
        try:
            with open(name):
                pass
        except IOError:
            showerror("Fichier inconnu", "Le fichier n'a pas pu être ouvert.")
        else:
            if self.preview != None:
                self.preview.stopThread()
                self.preview.join()
                self.preview = None
            if self.mode == "Parcours" or self.mode == "Community":
                self.difficultScreen = Toplevel()
                self.difficultScreen.title("Difficulty")
                self.difficultScreen.geometry("180x180")

                self.dOn = True
                v = IntVar()
                v.set(0)

                LTitre = Label(self.difficultScreen, text="Robot's Revolution",
                            font=("Comic Sans MS", 13, "bold"))
                REasy = Radiobutton(self.difficultScreen, text="Easy", variable=v,
                            value=1)
                RMedium = Radiobutton(self.difficultScreen, text="Medium", variable=v,
                            value=2)
                RDifficult = Radiobutton(self.difficultScreen, text="Hard", variable=v,
                            value=3)

                button = Button(self.difficultScreen, text="Validate",
                                command=self.CloseDifficult)
                LTitre.pack()
                REasy.pack()
                RMedium.pack()
                RDifficult.pack()
                button.pack()
                while self.dOn:
                    self.update()
                self.difficult = v.get()
            
            if self.mode == "IA" or self.mode == "Versus":
                game = Game(name.split("\"")[-1], self.mode, self.difficult, self.level, self.ia)
            else:
                game = Game(name.split("\"")[-1], self.mode, self.difficult, self.level)
            temp = game.launch()
            if temp == -12 and (self.mode == "IA" or self.mode == "Versus"):
                showinfo("Bravo !", "Vous avez battu l'IA "+str(self.ia))
                if self.mode == "IA":
                    self.ia = self.ia.split("_")[0]+"_"+str(int(self.ia.split("_")[1])+1)
                    try:
                        with open("files/ia/"+str(self.level)+".rev"):
                            pass
                    except IOError:
                        showinfo("Bravo !", "Vous avez fini tous les IA de ce mode !")
                        if askquestion("Robot's Revolution", "Voulez-vous relancer l'ia 1 ?") == "yes":
                            self.ia = "mp_1"
                            self.previewLevel(self.level)
                        else:
                            self.on = False
                            self.destroy()
                    else:
                        showinfo("Suivant", "C'est parti pour l'IA "+str(self.ia))
                        self.previewLevel(self.level)
                else:
                    if askquestion("Robot's Revolution", "Voulez-vous relancer cet ia ?") == "yes":
                        self.previewLevel(self.level)
                    else:
                        self.on = False
                        self.destroy()
            elif temp == -25 and self.mode == "Community":
                showinfo("Bravo !", "Vous avez réussi le niveau !")
                if askquestion("Robot's Revolution", "Voulez-vous refaire ce niveau ?") == "yes":
                    showinfo("Robot's Revolution", "C'est reparti !")
                    self.previewLevel(self.level)
                else:
                    self.on = False
                    self.destroy()
            elif temp == self.level:
                showinfo("Retente", "Réessaie de finir le niveau "+str(self.level)+" !")
                self.previewLevel(self.level)
            else:
                self.level = temp
                try:
                    with open("levels/"+str(self.level)+".rev"):
                        pass
                except IOError:
                    showinfo("Bravo !", "Vous avez fini tous les niveaux de ce mode !")
                    if askquestion("Robot's Revolution", "Voulez-vous relancer le niveau 1 ?\nVous pourrez refaire les niveaux avec plus de difficulté") == "yes":
                        self.level = 1
                        showinfo("Robot's Revolution", "C'est reparti !")
                        self.previewLevel(self.level)
                    else:
                        self.on = False
                        self.destroy()
                else:
                    showinfo("Suivant", "C'est parti pour le niveau "+str(self.level))
                    self.previewLevel(self.level)
                 
    def quitter(self):
        """ Quitter l'éditeur (avec confirmation)"""
        if askquestion("Revolt IDE", "Voulez-vous quitter ?") == "yes":
            if self.title().split(" - ")[1] == 'Untitled' or self.title()[0] == "*":
                if askquestion("Revolt IDE", "Voulez-vous enregistrer ?")=="yes":
                    self.sauvegarde()
            self.on = False
            self.destroy()
            if self.preview != None:
                self.preview.stopThread()
                self.preview.join()
                self.preview = None

    def execute(self, evt = None):
        """ Exécuter le script"""
        file = self.sauvegarde()
        if file != "":
            self.Jouer(file)

    def sauvegarde(self, evt= None):
        """ Sauvegarder un script"""
        if self.title().split(" - ")[1] == 'Untitled':
            filename = asksaveasfilename(title="Sauvegarder votre script",defaultextension = '.rev',filetypes=[('Revolt Files','.rev')])
            if filename != "":
                file=open(filename,"w")
                file.write(self.convertToText(self.blockList))
                self.title("Revolt IDLE - "+filename)
                file.close()
                return filename
            return ""
        else:
            if self.title()[0] == "*":
                liste = self.title().split(" - ")[1].split("/")
                filename = asksaveasfilename(title="Sauvegarder votre script",defaultextension = '.rev',filetypes=[('Revolt Files','.rev')], initialfile = liste[len(liste)-1])
                if filename != "":
                    file = open(filename, "w")
                    file.write(self.convertToText(self.blockList))
                    self.title("Revolt IDLE - "+filename)
                    file.close()
                    return filename
            else:
                return self.title().split(" - ")[1]
            return ""

    def creer(self, evt=None):
        """ Créer un nouveau fichier"""
        if self.title().split(" - ")[1] == 'Untitled':
            showerror("Revolt IDE","Vous êtes déjà sur un nouveau fichier !")
        else:
            if askquestion("Revolt IDE", "Voulez-vous enregistrer ?")=="no":
                self.title("Revolt IDE - Untitled")
                self.blockList = [["blockD", ImageTk.PhotoImage(Image.open("files/blocD.png"))]]
            else:
                self.sauvegarde()

    def ouvrir(self, evt=None):
        """ Ouvrir un fichier"""
        filename = askopenfilename(title="Ouvrir votre script", defaultextension='.rev', filetypes=[('Revolt Files', '.rev')])
        fichier = open(filename, "r", encoding="utf-8")
        content = fichier.read()
        fichier.close()
        self.convertToVisuel(content)
        self.showBlocks()
        self.title("Revolt IDE - "+filename)

    def apropos(self, evt=None):
        """ Informations RP de l'éditeur de script"""
        showinfo("Revolt IDE", "Créé par LN12\nCopyright 2112 - 2113")