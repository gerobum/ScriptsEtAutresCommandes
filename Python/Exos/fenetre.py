# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 17:28:43 2017

@author: yvan
"""

from Tkinter import Label, Button, Tk
import tkFont
import datetime
import locale
locale.setlocale(locale.LC_TIME,'')

from threading import Thread

import time




fmain = Tk();
fmain.config(bg='black')
fmain.title('Bonjour Maman')

ldate = Label(fmain, text=datetime.date.today().strftime('%A %d %B %Y'), bg='black', fg='white', font=tkFont.Font(family='Helvetica',size=50, weight='bold'))
lheure = Label(fmain, text=datetime.datetime.now().strftime('%H:%M:%S'), bg='black', fg='white', font=tkFont.Font(family='Helvetica',size=50, weight='bold'))  

ldate.pack()
lheure.pack()
bou1 = Button(fmain, text='Quitter', command = fmain.destroy)
bou1.pack()


class Maj(Thread):
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self, ldate, lheure):
        Thread.__init__(self)
        self.ldate = ldate
        self.lheure = lheure

    def run(self):
        while True:
            ldate.config(text=datetime.date.today().strftime('%A %d %B %Y'))
            lheure.config(text=datetime.datetime.now().strftime('%H:%M:%S'))
            time.sleep(1)


maj = Maj(ldate, lheure)

maj.start()
fmain.mainloop()


            