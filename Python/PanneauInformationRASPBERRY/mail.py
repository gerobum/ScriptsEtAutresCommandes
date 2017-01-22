# -*- encoding: utf-8 -*-
"""
Lecture mail
"""

import imapy
from Tkinter import *

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

from imapy.query_builder import Q

fp = open('fp')
thepasswd = fp.read()
print "le mot de passe ", thepasswd
fp.close()


fmain = Tk();
fmain.config(bg='black')
fmain.title('Bonjour Maman')
fmain.attributes('-fullscreen', True)

thefont = tkFont.Font(family='Helvetica',size=50, weight='bold')

def the_date():
    return datetime.date.today().strftime('Aujourd\'hui, nous sommes %A %d %B %Y')

def the_time():
    return datetime.datetime.now().strftime('Il est %H:%M:%S')
    
ldate = Label(fmain, text=the_date(), bg='black', fg='white', font=thefont)
lheure = Label(fmain, text=the_time(), bg='black', fg='white', font=thefont)  
lsep = Label(fmain, text='____________________________________________', bg='black', fg='white', font=thefont)   
lmes = Label(fmain, text='', bg='black', fg='white', font=thefont)  

ldate.pack()
lheure.pack()
lsep.pack()
lmes.pack();


def the_end():
    print 'fin générale'
    global fmain
    global dh
    global mail
    dh.the_end()
    mail.the_end()
    fmain.destroy()
    
bexit = Button(fmain, text='Quitter', command = the_end)
bexit.pack()
    

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

class Mailing(Thread):
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self):
        Thread.__init__(self)
        self.q = Q()
        self.ok = True
    
    def the_end(self):
        print 'fin de courrier'
        self.ok = False            

    def run(self):
        while self.ok:            
            box = imapy.connect(
                host='imap.gmail.com',
                username='mamie.rasp@gmail.com',
                password=thepasswd,
                # you may also specify custom port:
                # port=993
                ssl=True,
            )
            
            emails = box.folder('INBOX').emails(self.q.unseen())

            if len(emails) > 0:    
                for mail in emails:
                    print mail
                    mail.mark(['seen'])
                    if mail['subject'] == 'STOP':
                        mail.mark(['seen'])
                        the_end()
                    else:
                        lmes.config(text=mail['text'][0]['text_normalized'])
                        print mail
            else:
                print 'Nothing to do'
            
            box.logout()
            #time.sleep(300)
            time.sleep(10)
        print 'fin de la collecte du courrier'


dh = DateHeure(ldate, lheure)
mail = Mailing()

dh.start()
mail.start()
fmain.mainloop()

