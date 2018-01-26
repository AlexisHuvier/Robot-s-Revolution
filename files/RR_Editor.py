from tkinter import *
from tkinter.messagebox import showerror, showinfo
from PIL import Image, ImageTk
try:
    from files.RR_Game import Game
except ImportError:
    from RR_Game import Game

class Editor(Tk):
    def __init__(self, level):
        super(Editor, self).__init__()
        self.level = level

        self.title("Revolt IDE")

        self.code = Text(self, font=("Comic Sans MS", 14),
                    wrap='none', tabs=('1c', '2c'))
        self.code.insert('1.0', '#Votre code')
        self.s1 = Scrollbar(self)
        self.s2 = Scrollbar(self)
        self.code.config(yscrollcommand=self.s1.set, xscrollcommand=self.s2.set)
        self.s2.config(orient="horizontal")
        self.s2.config(command=self.code.xview)
        self.s1.config(command=self.code.yview)

        self.code.grid(row=0, column=0, sticky="NSEW")
        self.s1.grid(row=0, column=1, stick="NSEW")
        self.s2.grid(row=1, column=0, columnspan=2, stick="NSEW")
        self.code.focus_set()

        self.screen = Toplevel(self)
        self.screen.title("Level"+str(self.level))
        self.screen.geometry("620x650")

        self.ltitre = Label(self.screen, text="Level "+str(self.level),
                    font=("Comic Sans MS", 14, "bold"))

        self.canvas = Canvas(self.screen, width=600, height=600, bg="black")
        image = Image.open("files/l"+str(self.level)+".png")
        photo = ImageTk.PhotoImage(image)
        item = self.canvas.create_image(300, 300, image=photo)

        self.ltitre.place(x=260, y=5)
        self.canvas.place(x=10, y=40)

        self.mainloop()

    def Jouer(self, name):

        if name == "":
            showerror("Your Robot", "Veuillez écrire quelque chose !")
        elif name == "Nom du script":
            showerror("Your Robot", "Veuillez changer le nom !")
        else:
            try:
                with open("scripts/"+name+".rev"):
                    pass
            except IOError:
                showerror("Fichier inconnu", "Le fichier n'a pas pu être ouvert.")
            else:
                game = Game("scripts/"+name+".rev",
                            "Parcours", self.level)
                LEVEL = game.launch()
                try:
                    with open("levels/"+str(self.level)+".rev"):
                        pass
                except IOError:
                    showinfo("Bravo !", "Vous avez fini tous les niveaux de ce mode !")
                    Solo()
                else:
                    showinfo(
                        "Suivant", "C'est parti pour le niveau "+str(self.level))
                    image = Image.open("files/l"+str(self.level)+".png")
                    photo = ImageTk.PhotoImage(image)
                    item = self.canvas.create_image(300, 300, image=photo)

    def Execute(self):
        if self.nom.get() != "Nom Script" or NOM.get() != "":
            if " " in self.nom.get():
                showerror("ERROR","Le nom du script a un espace")
            else:
                with open("scripts/"+self.nom.get()+".rev","w") as fichier:
                    fichier.write(self.code.get("1.0","end"))
                self.Jouer(self.nom.get())
        else:
            showerror("ERROR","Il faut changer le nom du script ou lui en donner un")
