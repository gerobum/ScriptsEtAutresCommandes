# -*- encoding: utf-8 -*-
"""
Lecture mail
"""


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

from mailing import Mailing


fmain = Tk();
fmain.config(bg='black')
fmain.title('Bonjour Maman')
fmain.attributes('-fullscreen', True)

thefont = tkFont.Font(family='Helvetica',size=30, weight='bold')

def the_date():
    return datetime.date.today().strftime('Aujourd\'hui, nous sommes %A %d %B %Y')

def the_time():
    return datetime.datetime.now().strftime('Il est %H:%M:%S')
    
ldate = Label(fmain, text=the_date(), bg='black', fg='white', font=thefont)
lheure = Label(fmain, text=the_time(), bg='black', fg='white', font=thefont)  
lsep = Label(fmain, text='____________________________________________', bg='black', fg='white', font=thefont)   
lmes = [Label(fmain, text='', bg='black', fg='white', font=thefont),
        Label(fmain, text='', bg='black', fg='white', font=thefont),
        Label(fmain, text='', bg='black', fg='white', font=thefont)]

ldate.pack()
lheure.pack()
lsep.pack()
for lm in lmes:
    lm.pack()

def mini_maxi():
    global fmain
    global bminmax
    if bminmax['text'] == 'Minimise':
        bminmax['text']='Maximise'
        fmain.attributes('-fullscreen', False)
    else:
        bminmax['text']='Minimise'
        fmain.attributes('-fullscreen', True)

def the_end():
    print 'fin générale'
    global fmain
    global dh
    global mail
    dh.the_end()
    dh.join()
    mail.the_end()
    mail.join()
    fmain.destroy()
    
bexit = Button(fmain, text='Quitter', command = the_end)
 
bminmax = Button(fmain, text='Minimise', command = mini_maxi)

ldate.pack()
lheure.pack()
lsep.pack()
for lm in lmes:
    lm.pack()
bexit.pack(side='left')  
bminmax.pack(side='left')
    

class DateHeure(Thread):
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self, ldate, lheure):
        Thread.__init__(self)
        self.ldate = ldate
        self.lheure = lheure
        self.ok = True
    
    def the_end(self):
        print 'fin de date demandée'
        self.ok = False    

    def run(self):
        while self.ok:
            ldate.config(text=the_date())
            lheure.config(text=the_time())
            time.sleep(1)
        print 'fin de la mise à jour de la date'




dh = DateHeure(ldate, lheure)
mail = Mailing(ldate, lheure, lmes)

dh.start()
mail.start()
fmain.mainloop()

