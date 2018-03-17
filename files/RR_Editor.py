from tkinter import *
from tkinter.messagebox import showerror, showinfo, askquestion
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import pygame, glob, random
try:
    from files.RR_Game import Game
    from files.RR_class import Map
except ImportError:
    from RR_class import Map
    from RR_Game import Game

class Editor(Tk):
    def __init__(self, level, mode):
        super(Editor, self).__init__()
        self.dOn = False
        self.mode = mode
        self.difficultScreen = ""
        self.difficult = "MP"
        self.aide = ""
        self.on = True
        if self.mode == "IA":
            self.level = "mp_1"
        else:
            self.level = level

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
        self.screen = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Preview - Level "+str(level))
        try:
            with open("levels/"+str(level)+".rev", 'r') as fichier:
                lignes = fichier.read().split("\n")
                if self.mode == "Parcours" or self.mode == "Community": 
                    while lignes[0] == "" or lignes[0] == "\n":
                        lignes = lignes[1:]
                    self.aide = "#"+lignes[0]
                    self.code.delete('1.0', 'end')
                    self.code.insert("1.0", self.aide)
                    self.coloration()
                    lignes = lignes[2:]
                self.map = Map(lignes, level, "")
        except IOError:
            showerror("ERREUR", "Le fichier du level "+str(self.level)+" est inaccessible")
            pygame.quit()
        self.screen.fill((0, 0, 0))
        self.clock.tick(60)
        self.screen.blit(pygame.image.load("files/background.png"), [0, 0])
        self.map.player_list.draw(self.screen)
        self.map.rock_list.draw(self.screen)
        self.map.finish_list.draw(self.screen)
        self.map.lava_list.draw(self.screen)
        self.map.wall_list.draw(self.screen)
        pygame.display.update()
    
    def CloseDifficult(self):
        if self.difficultScreen != "":
            self.dOn = False
            self.difficultScreen.destroy()

    def Jouer(self, name):
        try:
            with open(name):
                pass
        except IOError:
            showerror("Fichier inconnu", "Le fichier n'a pas pu être ouvert.")
        else:
            pygame.quit()
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
            
            game = Game(name.split("\"")[-1], self.mode, self.difficult, self.level)
            temp = game.launch()
            if temp == -12 and self.mode == "IA":
                showinfo("Bravo !", "Vous avez battu l'IA "+str(self.level))
                self.level = self.level.split("_")[0]+"_"+str(int(self.level.split("_")[1])+1)
                try:
                    with open("levels/"+str(self.level)+".rev"):
                        pass
                except IOError:
                    showinfo("Bravo !", "Vous avez fini tous les niveaux de ce mode !")
                    if askquestion("Robot's Revolution", "Voulez-vous relancer le niveau 1 ?\nVous pourrez réaffronter la première IA") == "yes":
                        self.level = "mp_1"
                        showinfo("Robot's Revolution", "C'est reparti !")
                        self.previewLevel(self.level)
                    else:
                        self.on = False
                        self.destroy()
                else:
                    showinfo("Suivant", "C'est parti pour le niveau "+str(self.level))
                    self.previewLevel(self.level)
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
        if askquestion("Revolt IDE", "Voulez-vous quitter ?") == "yes":
            if self.title().split(" - ")[1] == 'Untitled' or self.title()[0] == "*":
                if askquestion("Revolt IDE", "Voulez-vous enregistrer ?")=="yes":
                    self.sauvegarde()
            self.on = False
            self.destroy()
            pygame.quit()

    def execute(self, evt = None):
        file = self.sauvegarde()
        if file != "":
            self.Jouer(file)

    def sauvegarde(self, evt= None):
        if self.title().split(" - ")[1] == 'Untitled':
            filename = asksaveasfilename(title="Sauvegarder votre script",defaultextension = '.rev',filetypes=[('Revolt Files','.rev')])
            if filename != "":
                file=open(filename,"w")
                file.write(self.code.get("1.0","end")[:-1])
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
        nmbChar = IntVar()
        for mot in ["walk", "left", "right", "jump", "getDirection", "setFunc", "callFunc",
                    "getAttack", "setAttack", "setSprite", "getSprite", "setVar", "getVar",
                    "loopif", "loop", "sayConsole", "if_", "getPosX", "getPosY"]:
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
        showinfo("Revolt IDE", "Créé par LN12\nCopyright 2111 - 2112")
