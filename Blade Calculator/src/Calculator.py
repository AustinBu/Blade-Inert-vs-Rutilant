import os
import sys
import time
import tkinter as tk
from tkinter.constants import *

from PIL import ImageTk, Image


class Calculator:
    def __init__(self, master):
        self.master = master
        time.sleep(1)
        self.master.attributes('-fullscreen', True)
        self.master.attributes('-transparent', True)
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master, bg='#40af20')
        self.frame.pack(fill=Y, expand=True)

        img = ImageTk.PhotoImage(
            Image.open(os.path.join(sys.path[0], "bladehsr.webp")))
        lbl = tk.Label(self.frame, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.55, anchor='center')  # Place label in center of parent.

        self.required_talent_stacks = 5
        self.ultMultiplier = 1.9
        self.turns = tk.StringVar()
        self.hits = tk.StringVar()
        self.cone = tk.StringVar()
        self.cone.set("Select Light Cone")
        self.eidolon = tk.StringVar()
        self.eidolon.set("Select Eidolon")

        self.basics = 0
        self.basicsCounter = 0
        self.talents = 0
        self.talentCounter = 0
        self.ults = 0
        self.ultCounter = 0

        self.inert = 0.
        self.rutilant = 0.

        self.frame0 = tk.Frame(self.frame, height=60)
        self.frame0.grid(row=0, column=0, pady=50)
        self.frame1 = tk.Frame(self.frame, height=60, bd=4, relief="groove")
        self.frame1.grid(row=1, column=0, pady=50)
        self.frame2 = tk.Frame(self.frame, height=60)
        self.frame2.grid(row=2, column=0, pady=50)
        self.frame3 = tk.Frame(self.frame, height=60)
        self.frame3.grid(row=3, column=0, pady=200)

        # Frame 0
        self.lblTitle = tk.Label(self.frame0, text='BLADE \nINERT VS RUTILANT', font='Broadway 50', bg='#40af20',
                                 width=30)
        self.lblTitle.grid(row=0, column=0, columnspan=2)

        # Frame 1
        self.lblTurns = tk.Label(self.frame1, text='Turns:\t', font='Broadway 24')
        self.lblTurns.grid(row=0, column=0, sticky='nsew')
        self.txtTurns = tk.Entry(self.frame1, textvariable=self.turns, font='Broadway 24', width=20)
        self.txtTurns.grid(row=0, column=1)

        self.lblHits = tk.Label(self.frame1, text='Hits:\t', font='Broadway 24')
        self.lblHits.grid(row=1, column=0, sticky='nsew')
        self.txtHits = tk.Entry(self.frame1, textvariable=self.hits, font='Broadway 24', width=20)
        self.txtHits.grid(row=1, column=1)

        self.cone_options = [
            "S1 The Unreachable Side",
            "S5 A Secret Vow"
        ]
        self.dropCone = tk.OptionMenu(self.frame1, self.cone, *self.cone_options)
        self.dropCone.grid(row=2, column=0, columnspan=2)

        self.eidolon_options = [
            "E0",
            "E1",
            "E6"
        ]
        self.dropEidolons = tk.OptionMenu(self.frame1, self.eidolon, *self.eidolon_options)
        self.dropEidolons.grid(row=3, column=0, columnspan=2)

    # Frame 2
        self.btnCalculate = tk.Button(self.frame2, bd=6, relief=RAISED, text='Calculate', font='Broadway 24',
                                      width=15, command=self.calculate)
        self.btnCalculate.grid(row=0)

        # Frame 3
        self.txtResults = tk.StringVar()
        self.lblResults = tk.Label(self.frame3, width=40, height=6, textvariable=self.txtResults, font='Broadway 24')
        self.lblResults.grid(row=0)

    def calculate(self):
        self.reset()
        
        if self.eidolon.get() == self.eidolon_options[0]:
            self.required_talent_stacks = 5
            self.ultMultiplier = 1.9
        elif self.eidolon.get() == self.eidolon_options[1]:
            self.required_talent_stacks = 5
            self.ultMultiplier = 3.25
        elif self.eidolon.get() == self.eidolon_options[2]:
            self.required_talent_stacks = 4
            self.ultMultiplier = 3.25
        else:
            self.txtResults.set("Please select an eidolon")
            return
        self.attack_calcs()

        if self.cone.get() == self.cone_options[0]:
            self.damage_calc_bis()
        elif self.cone.get() == self.cone_options[1]:
            self.damage_calc_s5_vow()
        else:
            self.txtResults.set("Please select a light cone")
            return



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
        if self.talentCounter >= self.required_talent_stacks:
            self.talents += 1
            self.talentCounter = 0
            self.ultCounter += 10

    def check_ultimate_counter(self):
        if self.ultCounter >= 130:
            self.ults += 1
            self.ultCounter = 0
            self.talentCounter += 1

    def damage_calc_bis(self):
        self.inert = self.basics * 1.64 + (((1.1 * self.talents) + (self.ultMultiplier * self.ults)) * 1.79)
        self.rutilant = self.basics * 1.84 + (((1.1 * self.talents) + (self.ultMultiplier * self.ults)) * 1.64)

    def damage_calc_s5_vow(self):
        self.inert = self.basics * 2 + (((1.1 * self.talents) + (self.ultMultiplier * self.ults)) * 2.15)
        self.rutilant = self.basics * 2.2 + (((1.1 * self.talents) + (self.ultMultiplier * self.ults)) * 2)

    def reset(self):
        self.basics = 0
        self.basicsCounter = 0
        self.talents = 0
        self.talentCounter = 0
        self.ults = 0
        self.ultCounter = 0

        self.inert = 0.
        self.rutilant = 0.


newWindow = tk.Tk()
myWindow = Calculator(newWindow)

newWindow.mainloop()
