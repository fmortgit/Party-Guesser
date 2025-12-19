import requests
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import random


class MPViewer(tk.Tk):
    def __init__(self, mpListData):
        super().__init__()
        self.title("MP Party Guessing Game")
        self.mpListData = mpListData
        self.currentIndex = 0
        self.score = 0

        self.nameLabel = tk.Label(self, text="", font=("Arial", 16))
        self.nameLabel.pack(pady=10)

        self.partyLabel = tk.Label(self, text="", font=("Arial", 12))
        self.partyLabel.pack(pady=5)

        self.imageLabel = tk.Label(self)
        self.imageLabel.pack(pady=20)

        self.buttonsFrame = tk.Frame(self)
        self.buttonsFrame.pack(pady=10)

        self.conservativeButton = tk.Button(self.buttonsFrame, text="Conservative", width=15, command=lambda: self.checkGuess("Conservative"))
        self.conservativeButton.grid(row=0, column=0, padx=5)

        self.labourButton = tk.Button(self.buttonsFrame, text="Labour", width=15, command=lambda: self.checkGuess("Labour"))
        self.labourButton.grid(row=0, column=1, padx=5)

        self.libDemButton = tk.Button(self.buttonsFrame, text="Lib Dem", width=15, command=lambda: self.checkGuess("Liberal Democrat"))
        self.libDemButton.grid(row=1, column=0, padx=5)

        self.greenButton = tk.Button(self.buttonsFrame, text="Green", width=15, command=lambda: self.checkGuess("Green"))
        self.greenButton.grid(row=1, column=1, padx=5)

        self.reformButton = tk.Button(self.buttonsFrame, text="Reform", width=15, command=lambda: self.checkGuess("Reform UK"))
        self.reformButton.grid(row=2, column=0, padx=5)

        self.independantButton = tk.Button(self.buttonsFrame, text="Independent", width=15, command=lambda: self.checkGuess("Independent"))
        self.independantButton.grid(row=2, column=1, padx=5)

        self.showNextMP()

    def showNextMP(self):
        if self.currentIndex < len(self.mpListData):
            name, party, imageUrl = self.mpListData[self.currentIndex]
            self.nameLabel.config(text=name)
            self.partyLabel.config(text="Guess the party:")

            response = requests.get(imageUrl)
            img = Image.open(BytesIO(response.content))

            img = img.resize((250, 250))
            imgTk = ImageTk.PhotoImage(img)

            self.imageLabel.config(image=imgTk)
            self.imageLabel.image = imgTk

            self.removeTickX()
            self.enableButtons()

        else:
            self.endMessage()

    def endMessage(self):
        self.nameLabel.config(text="Game Over!")
        self.partyLabel.config(text=f"Your Score: {self.score} / {len(self.mpListData)}")
        self.removeTickX()

        for button in self.buttonsFrame.winfo_children():
            button.config(state="disabled")

    def checkGuess(self, guessedParty):
        name, correctParty, _ = self.mpListData[self.currentIndex]
        self.disableButtons()

        if guessedParty == correctParty:
            self.displayTick()
            self.score += 1
        else:
            self.displayX()
            self.showCorrectParty(correctParty)  # Display the correct party when wrong guess

        self.currentIndex += 1
        self.after(1000, self.showNextMP)

    def displayTick(self):
        self.tickLabel = tk.Label(self, text="✓", font=("Arial", 50), fg="green", bg="white")
        self.tickLabel.place(x=100, y=200)

    def displayX(self):
        self.xLabel = tk.Label(self, text="X", font=("Arial", 50), fg="red", bg="white")
        self.xLabel.place(x=100, y=200)

    def showCorrectParty(self, correctParty):
        self.partyLabel.config(text=correctParty)  # Show the correct party

    def removeTickX(self):
        if hasattr(self, "tickLabel"):
            self.tickLabel.destroy()
        if hasattr(self, "xLabel"):
            self.xLabel.destroy()

    def disableButtons(self):
        for button in self.buttonsFrame.winfo_children():
            button.config(state="disabled")

    def enableButtons(self):
        for button in self.buttonsFrame.winfo_children():
            button.config(state="normal")



url = "https://www.theyworkforyou.com/mps/"
response = requests.get(url)

if response.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

mpList = soup.find_all("a", class_="people-list__person")

mpListData = []
validParties = ["Conservative", "Labour", "Liberal Democrat", "Green", "Reform UK", "Independent"]

for mp in mpList:
    name = mp.find("h2", class_="people-list__person__name").text.strip()
    imageTag = mp.find("img", class_="people-list__person__image")
    imageUrl = imageTag["src"]
    imageUrl = f"https://www.theyworkforyou.com{imageUrl}"

    partyTag = mp.find("span", class_="people-list__person__party")
    party = partyTag.text.strip() if partyTag else "No party listed"

    if party in validParties:
        mpListData.append((name, party, imageUrl))
    elif party == "Labour/Co-operative":
        mpListData.append((name, "Labour", imageUrl))

random.shuffle(mpListData)

mpListData = mpListData[:10]



app = MPViewer(mpListData)
app.mainloop()