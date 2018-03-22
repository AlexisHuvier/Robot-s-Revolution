from tkinter import *
from urllib.request import urlopen
from urllib.error import HTTPError
from tkinter.messagebox import showerror
try:
    from files.RR_class import MyHTMLParser
except ImportError:
    from RR_class import MyHTMLParser


class VersusFen(Tk):
    def __init__(self):
        super(VersusFen, self).__init__()
        self.on = True
        try:
            html = urlopen('http://www.robot-s-revolution.fr.nf/scripts.php').read().decode("utf-8")
            parser = MyHTMLParser()
            parser.feed(html)
            self.result=parser.get("ia")
        except HTTPError:
            showerror("ERREUR", "Connection au serveur impossible")
            self.choix = "Quit"
            self.on = False
            self.destroy()
            return;     
        
        self.page = 1
        self.listeButton = []

        self.title("Choix du niveau")
        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.titre = Label(self, text="Choix de l'IA", font=("Comic Sans MS", 20, "bold"))
        self.titre.grid(row = 1, column = 2)
        if len(self.result) >= 7:
            self.nbPage = int(len(result)/9)+1
        else:
            self.nbPage = 1

        self.affichePage(self.page)

        self.buttonLeft = Button(self, text="Page Précédente", width=12, height=2, command=self.pageMoins)
        self.buttonLeft.grid(row=5, column=1, padx=10, pady=10)
        self.buttonLeft.config(state="disabled")
        self.buttonQuit = Button(self, text="Quitter", width=12, height=2, command=self.quit)
        self.buttonQuit.grid(row=5, column=2, padx=10, pady=10)
        self.buttonRight = Button(self, text="Page Suivante", width=12, height=2, command=self.pagePlus)
        self.buttonRight.grid(row=5, column=3, padx=10, pady=10)
        if self.nbPage:
            self.buttonRight.config(state="disabled")

        self.mainloop()
    
    def pageMoins(self):
        self.page -= 1
        self.affichePage(self.page)
        self.buttonRight.config(state="normal")
        if self.page == 1:
            self.buttonLeft.config(state="disabled")
    
    def pagePlus(self):
        self.page += 1
        self.affichePage(self.page)
        self.buttonLeft.config(state="normal")
        if self.page == self.nbPage:
            self.buttonRight.config(state="disabled")
    
    def quit(self):
        self.choix = "Quit"
        self.on = False
        self.destroy()

    def affichePage(self, page = 1):
        self.listeButton = []
        row = 2
        column = 1
        for i in range(9):
            frame = Frame(self, borderwidth = 2, relief = GROOVE)
            nb = i+(9*(page-1))

            try:
                level = self.result[nb]
                if len(level[6]) >= 17:
                    level[6] = level[6][:17]
                texte = "Nom : "+level[1]+"\nDescription : "+level[4]+"\nDifficulté : "+level[6]+"\nAuteur : "+level[5]
                setButton = True
            except IndexError:
                texte = ""
                setButton = False

            infos = Label(frame, text=texte, height = 10, width = 25)
            frame.grid(row=row, column=column, padx=20, pady=20)
            infos.pack()
            self.button = Button(frame, text="Choisir cet IA", command=lambda x=nb: self.choisir(x))
            self.button.pack()
            if setButton == False:
                self.button.config(state="disabled")
            column += 1
            if column == 4:
                row += 1
                column = 1
    
    def choisir(self, nb):
        self.choix = self.result[nb]
        self.on = False
        self.destroy()
        
