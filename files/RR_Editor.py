from tkinter import *
from tkinter.messagebox import showerror, showinfo, askquestion
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import pygame, glob, random
try:
    from files.RR_Game import Game
    from files.RR_class import Map, PreviewThread
except ImportError:
    from RR_class import Map, PreviewThread
    from RR_Game import Game

class Editor(Tk):
    """Editeur de script"""
    def __init__(self, level, mode, ia = None):
        """Initiation de la classe"""
        super(Editor, self).__init__()
        self.dOn = False
        self.preview = None
        self.mode = mode
        self.difficultScreen = ""
        self.difficult = "MP"
        self.aide = ""
        self.on = True
        self.levels = []
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

        self.code = Text(self, font=("Comic Sans MS", 14),
                    wrap='none', tabs=('1c', '2c'))
        self.coloration()
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Nouveau", command=self.creer)
        self.menu1.add_command(label="Ouvrir", command=self.ouvrir)
        self.menu1.add_command(label="Sauvegarder", command=self.sauvegarde)
        self.menu1.add_command(label="Exécuter", command=self.execute)
        self.menubar.add_cascade(label="Fichier", menu=self.menu1)
        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="A propos", command=self.apropos)
        self.menubar.add_cascade(label="Info", menu=self.menu2)
        self.s1 = Scrollbar(self)
        self.s2 = Scrollbar(self)
        self.code.config(yscrollcommand=self.s1.set,
                         xscrollcommand=self.s2.set)
        self.code.tag_config("Mots", foreground="#800000")
        self.code.tag_config("Nombre", foreground="#0000FF")
        self.code.tag_config("Texte", foreground="#156f11")
        self.code.tag_config("Commentaire", foreground="#808080")
        self.s2.config(orient="horizontal")
        self.s2.config(command=self.code.xview)
        self.s1.config(command=self.code.yview)

        self.code.grid(row=0, column=0, sticky="NSEW")
        self.s1.grid(row=0, column=1, stick="NSEW")
        self.s2.grid(row=1, column=0, columnspan=2, stick="NSEW")

        self.bind_all('<Key>', self.writeEvent)
        self.bind_all("<Control-KeyPress-o>", self.ouvrir)
        self.bind_all("<Control-KeyPress-n>", self.creer)
        self.bind_all("<Control-KeyPress-i>", self.apropos)
        self.bind_all("<Control-KeyPress-s>", self.sauvegarde)
        self.bind_all("<KeyPress-F5>", self.execute)
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.config(menu=self.menubar)

        self.code.focus_set()

        self.previewLevel(self.level)

        self.mainloop()

    def previewLevel(self, level):
        """ Preview du level <level>"""
        self.preview = PreviewThread(level, self)
        self.preview.start()
    
    def CloseDifficult(self):
        """ Fermeture du screen de la difficulté"""
        if self.difficultScreen != "":
            self.dOn = False
            self.difficultScreen.destroy()

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
                file.write(self.code.get("1.0", "end")[:-1])
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
                    file.write(self.code.get("1.0", "end")[:-1])
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
            fichier = open(self.title().split(" - ")[1], "r")
            content = fichier.read()
            fichier.close()
            if self.code.get("1.0","end") == content:
                self.title("Revolt IDE - Untitled")
                self.code.delete('1.0','end')
                self.code.insert("1.0",self.aide)
            else:
                if askquestion("Revolt IDE", "Voulez-vous enregistrer ?")=="no":
                    self.title("Revolt IDE - Untitled")
                    self.code.delete('1.0','end')
                    self.code.insert("1.0", self.aide)
                else:
                    self.sauvegarde()

    def ouvrir(self, evt=None):
        """ Ouvrir un fichier"""
        global txt, fenetre
        filename = askopenfilename(title="Ouvrir votre script", defaultextension='.rev', filetypes=[('Revolt Files', '.rev')])
        fichier = open(filename, "r", encoding="utf-8")
        content = fichier.read()
        fichier.close()
        self.code.delete('1.0', 'end')
        self.code.insert('1.0',content)
        self.title("Revolt IDE - "+filename)
        self.coloration()

    def writeEvent(self, evt):
        """Event lors de l'écriture du joueur"""
        if evt.char == '"':
            self.code.mark_gravity(INSERT, LEFT)
            self.code.insert(INSERT, '"')
            self.code.mark_gravity(INSERT, RIGHT)
        elif evt.char == '{':
            self.code.mark_gravity(INSERT, LEFT)
            self.code.insert(INSERT,'}')
            self.code.mark_gravity(INSERT, RIGHT)
        elif evt.char == '(':
            self.code.mark_gravity(INSERT, LEFT)
            self.code.insert(INSERT, ')')
            self.code.mark_gravity(INSERT, RIGHT)
        elif evt.char == '[':
            self.code.mark_gravity(INSERT, LEFT)
            self.code.insert(INSERT, ']')
            self.code.mark_gravity(INSERT, RIGHT)
        elif evt.char == "'":
            self.code.mark_gravity(INSERT, LEFT)
            self.code.insert(INSERT, "'")
            self.code.mark_gravity(INSERT, RIGHT)
        elif evt.char == "}" or evt.char == ")" or evt.char == "]":
            self.code.delete(INSERT)
        if self.title()[0] != "*":
            self.title("*"+self.title())
        self.coloration()

    def coloration(self):
        """ Coloration syntaxique"""
        nmbChar = IntVar()
        for mot in ["walk", "left", "right", "jump", "getDirection", "setFunc", "callFunc",
                "getAttack", "setAttack", "setSprite", "getSprite", "setVar", "getVar",
                "loopif", "loop", "sayConsole", "if_", "getPosX", "getPosY", "shoot",
                "getEnnemyPosX", "getEnnemyPosY"]:
            lastPos = "1.0"
            while 1 :
                lastPos = self.code.search( mot, index = lastPos, stopindex = 'end', regexp = 0, count = nmbChar )
                if lastPos == "" :
                    break
                self.code.tag_add('Mots', lastPos, "%s + %d chars" %
                                  (lastPos, nmbChar.get()))
                lastPos = "%s + 1 chars" % lastPos
        for mot in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            lastPos = "1.0"
            while 1:
                lastPos = self.code.search(
                    mot, index=lastPos, stopindex='end', regexp=0, count=nmbChar)
                if lastPos == "":
                    break
                self.code.tag_add('Nombre', lastPos,
                                  "%s + %d chars" % (lastPos, nmbChar.get()))
                lastPos = "%s + 1 chars" % lastPos
        lastPos = "1.0"
        while 1:
            lastPos = self.code.search(
                r'".*"', index=lastPos, stopindex='end', regexp=True, count=nmbChar)
            if lastPos == "":
                break
            self.code.tag_add('Texte', lastPos, "%s + %d chars" %
                              (lastPos, nmbChar.get()))
            lastPos = "%s + 1 chars" % lastPos
        lastPos = "1.0"
        while 1:
            lastPos = self.code.search(
                r"'.*'", index=lastPos, stopindex='end', regexp=True, count=nmbChar)
            if lastPos == "":
                break
            self.code.tag_add('Texte', lastPos, "%s + %d chars" %
                              (lastPos, nmbChar.get()))
            lastPos = "%s + 1 chars" % lastPos
        lastPos = "1.0"
        while 1:
            lastPos = self.code.search(
                r'#.*', index=lastPos, stopindex='end', regexp=True, count=nmbChar)
            if lastPos == "":
                break
            self.code.tag_add('Commentaire', lastPos,
                              "%s + %d chars" % (lastPos, nmbChar.get()))
            lastPos = "%s + 1 chars" % lastPos

    def apropos(self, evt=None):
        """ Informations RP de l'éditeur de script"""
        showinfo("Revolt IDE", "Créé par LN12\nCopyright 2111 - 2112")
