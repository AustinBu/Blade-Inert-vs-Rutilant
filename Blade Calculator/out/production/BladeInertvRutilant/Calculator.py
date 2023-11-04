import os
import sys
import tkinter as tk
from tkinter.constants import *

from PIL import ImageTk, Image


class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-fullscreen', True)
        self.master.wm_attributes('-transparentcolor', True)
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=Y, expand=True)

        img = ImageTk.PhotoImage(
            Image.open(os.path.join(sys.path[0], "bladehsr.webp")))
        lbl = tk.Label(self.frame, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.

        self.turns = tk.StringVar()
        self.hits = tk.StringVar()

        self.basics = 0
        self.basicsCounter = 0
        self.talents = 0
        self.talentCounter = 0
        self.ults = 0
        self.ultCounter = 0

        self.inert = 0.
        self.rutilant = 0.

        self.frame0 = tk.Frame(self.frame, width=800, height=60, bg='')
        self.frame0.grid(row=0, column=0, pady=50)
        self.frame1 = tk.Frame(self.frame, width=800, height=60, bd=4, relief="groove")
        self.frame1.grid(row=1, column=0, pady=50)
        self.frame2 = tk.Frame(self.frame, width=800, height=60)
        self.frame2.grid(row=2, column=0, pady=50)

        # Frame 0
        self.lblTitle = tk.Label(self.frame0, text='BLADE \nINERT VS RUTILANT', font='Broadway 50', bg='')
        self.lblTitle.grid(row=0, column=0, columnspan=2)

        # Frame 1
        self.lblTurns = tk.Label(self.frame1, text='Turns:\t', font='Broadway 24')
        self.lblTurns.grid(row=0, column=0)
        self.txtTurns = tk.Entry(self.frame1, textvariable=self.turns, font='Broadway 24', width=20)
        self.txtTurns.grid(row=0, column=1)

        self.lblHits = tk.Label(self.frame1, text='Hits\t', font='Broadway 24',)
        self.lblHits.grid(row=1, column=0)
        self.txtHits = tk.Entry(self.frame1, textvariable=self.hits, font='Broadway 24', width=20)
        self.txtHits.grid(row=1, column=1)

        # Frame 2
        self.btnCalculate = tk.Button(self.frame2, bd=6, relief=RAISED, text='Calculate', font='Broadway 24',
                                      width=15, command=self.calculate)
        self.btnCalculate.grid(row=0)
        self.txtResults = tk.StringVar()
        self.lblResults = tk.Label(self.frame2, width=40, height=10, textvariable=self.txtResults, font='Broadway 24')
        self.lblResults.grid(row=1, pady=50)

    def calculate(self):
        self.attack_calcs()
        self.damage_calc_bis()

        recommended = "Rutilant is " + str(round(((self.rutilant / self.inert * 100) - 100), 2)) \
                      + "% better than Inert" if self.rutilant > self.inert \
            else "Inert is " + str(round(((self.inert / self.rutilant * 100) - 100), 2)) + "% better than Rutilant"
        self.txtResults.set(
            "After " + self.turns.get() + " turns and getting hit " + self.hits.get() + " times per turn:"
            + "\nBasics: " + str(self.basics)
            + "\nTalents: " + str(self.talents)
            + "\nUlts: " + str(self.ults)
            + "\n" + recommended)
        print(self.rutilant)
        print(self.inert)

    def attack_calcs(self):
        for i in range(int(self.turns.get())):
            if self.basicsCounter == 0:
                self.basicsCounter = 3
                self.talentCounter += 1
            self.check_talent_counter()
            self.check_ultimate_counter()
            self.basics += 1
            self.basicsCounter -= 1
            self.talentCounter += 1
            self.ultCounter += 30
            self.check_talent_counter()
            self.check_ultimate_counter()
            for j in range(int(self.hits.get())):
                self.talentCounter += 1
                self.ultCounter += 10
                self.check_talent_counter()
                self.check_ultimate_counter()

    def check_talent_counter(self):
        if self.talentCounter >= 5:
            self.talents += 1
            self.talentCounter = 0
            self.ultCounter += 10

    def check_ultimate_counter(self):
        if self.ultCounter >= 130:
            self.ults += 1
            self.ultCounter = 0
            self.talentCounter += 1

    def damage_calc_bis(self):
        self.inert = self.basics * 1.64 + (((1.1 * self.talents) + (1.9 * self.ults)) * (1.79))
        self.rutilant = self.basics * 1.84 + (((1.1 * self.talents) + (1.9 * self.ults)) * (1.64))


newWindow = tk.Tk()
myWindow = Calculator(newWindow)

newWindow.mainloop()
