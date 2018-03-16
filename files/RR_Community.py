from tkinter import *
import urllib.request
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.getData = False
        self.result = []

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for i in attrs:
                if i[0]=="class" and i[1]=="level":
                    self.getData = True
                else:
                    self.getData = False
        if tag == "a":
            for i in range(0, len(attrs)):
                if attrs[i][0] == "class" and attrs[i][1] == "lien":
                    self.result.append(attrs[i+1][1])
                    
    
    def handle_endtag(self, tag):
        if tag == "div":
            self.getData = False

    def handle_data(self, data):
        if self.getData == True:
            if data != "- ":
                if " : " in data:
                    self.result.append(data.split(" : ")[1])
                else:
                    self.result.append(data)
    
    def getResult(self):
        nb = int(len(self.result)/8)
        resultF = []
        for i in range(nb):
            resultF.append([])
            for y in range(8):
                resultF[i].append(self.result[y])
            for i in range(8):
                self.result.remove(self.result[0])
        return resultF


class CommunityFen(Tk):
    def __init__(self):
        super(CommunityFen, self).__init__()
        self.on = True
        html = urllib.request.urlopen('http://www.robot-s-revolution.fr.nf/scripts.php').read()
        parser = MyHTMLParser()
        parser.feed(str(html))
        self.listeButton=[]
        self.result=parser.getResult()
        self.page = 1

        self.title("Choix du niveau")

        self.titre = Label(self, text="Choix du niveau", font=("Comic Sans MS", 20, "bold"))
        self.titre.grid(row = 1, column = 2)
        if len(self.result) >= 7:
            self.nbPage = int(len(result)/9)+1
        else:
            self.nbPage = 1

        self.affichePage(self.page)

        self.mainloop()
    
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
            if setButton:
                self.button = Button(frame, text="Choisir "+level[1], command = lambda x=nb:self.choisir(x))
                self.button.pack()
            column += 1
            if column == 4:
                row += 1
                column = 1
    
    def choisir(self, nb):
        self.choix = self.result[nb]
        self.on = False
        self.destroy()
        
