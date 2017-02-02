# -*- encoding: utf-8 -*-
"""
Lecture mail

Created on Sat Jan 21 17:28:43 2017

@author: yvan
"""

from Tkinter import Label, Button, Tk
import tkFont
import datetime
import locale
import commands
from mailing import Mailing
from mailing import send
from listes import get_liste
from chronotext import getDelay
import os


locale.setlocale(locale.LC_TIME,'')

from threading import Thread

import time

class MainFrame(Tk):
    def __init__(self):
        Tk.__init__(self) 
        
        self.config(bg='black')
        self.title('Bonjour Maman')
        self.attributes('-fullscreen', True)
        
        self.width = int(self.winfo_screenwidth()*0.995)

        self.thefont = tkFont.Font(family='Purisa',size=20, weight='bold')
        self.theMiddlefont = tkFont.Font(family='Purisa',size=30, weight='bold', slant='italic')
        self.theBigfont = tkFont.Font(family='Purisa',size=40, weight='bold', slant='italic')

    
        self.lintro = Label(self, text='Bonjour Maman', wraplength=self.width, bg='#3209FF', fg='#FFFFDA', font=self.theBigfont, anchor='w')
        self.ldate = Label(self, text='', wraplength=self.width, bg='#3209FF', fg='#FFFFDA', font=self.theMiddlefont, anchor='w')
        self.lheure = Label(self, text='', wraplength=self.width, bg='#3209FF', fg='#FFFFDA', font=self.theBigfont, anchor='w') 
        
        self.bexit = Button(self, text='Quitter', command = self.the_end)         
        self.bminmax = Button(self, text='Minimise', command = self.mini_maxi)        
        self.bjournuit = Button(self, text='Jour', command = self.jour_nuit)
        
        self.mailing_delay = getDelay('mailing_delay', 900)

        self.lintro.pack(fill='both')
        self.ldate.pack(fill='both')
        self.lheure.pack(fill='both')     
        self.chronolist = []
        
        self.init_labels()
        self.fill_labels()        
       
#        self.bexit.pack(side='left')  
#        self.bminmax.pack(side='left')
#        self.bjournuit.pack(side='left')                        

        self.dh = DateHeure(self.ldate, self.lheure)
        self.mail = Mailing(self)
        self.copie_ecran = CopieEcran()
        self.nettoyage = Nettoyage(self)
        
        self.dh.start()
        self.mail.start()
        self.copie_ecran.start()
        self.nettoyage.start()
        self.mainloop()  

    def init_labels(self):
        colors = ['#BAFFA8', '#FFFFD0']
        nbcolors = len(colors) # Nécessaire
                
        self.labels = []  
        
        
        for i in range(10):
            label = Label(self, text='', wraplength=self.width, justify='left', bg=colors[i%nbcolors], fg='black', font=self.thefont)
            label.pack(fill='both', pady=1)
            self.labels.append(label)
            
    def fill_labels(self, ctext=None):
        for label in self.labels:
            label['text'] = ''
            
        i = 0
        if ctext != None:
            self.chronolist.append(ctext)
        
        self.chronolist = get_liste(self.chronolist)
#        #list(filter(lambda a: a != 2, x))
        for s in self.chronolist:
            if s.text().strip() != '':
                self.labels[i]['text'] = s.text().strip()
                i+=1
                

    def mini_maxi(self):
        if self.bminmax['text'] == 'Minimise':
            self.bminmax['text']='Maximise'
            self.attributes('-fullscreen', False)
        else:
            self.bminmax['text']='Minimise'
            self.attributes('-fullscreen', True)

    def jour_nuit(self):
        if self.bjournuit['text'] == 'Nuit':
            self.bjournuit['text']='Matin'
            #self.jour = False
        elif self.bjournuit['text'] == 'Jour':
            self.bjournuit['text']='Soir'
            #self.jour = True
    
    def the_end(self):
        print 'TERMINAISON demandée'
        #signal.signal(signal.SIGINT, handler)
        print "Attention fermeture dans "
        print "3"
        time.sleep(1)
        print "2"
        time.sleep(1)
        print "1"
        time.sleep(1)
        commands.getoutput('rm lmes')
        commands.getoutput('rm .lock-panel')
        #os.kill(os.getpid(), 9)
        
        self.dh.the_end()
#        self.dh.join()
        print "FIN de l'horloge"
        self.mail.the_end()
#        self.mail.join()
        print 'FIN de la relève du courrier'

        self.copie_ecran.the_end()
#        self.copie_ecran.join()
        print "FIN de mise à jour de l'écran"

        self.nettoyage.the_end()
#        self.nettoyage.join()
        print 'FIN du thread horaire'
        self.destroy()
        print "C'est totalement fini"


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
            self.ldate.config(text=self.the_date())
            self.lheure.config(text=self.the_time())
            time.sleep(1)
        print 'fin de la mise à jour de la date'

    def the_date(self):
        return datetime.date.today().strftime('Aujourd\'hui, nous sommes %A %d %B %Y')

    def the_time(self):
        return datetime.datetime.now().strftime('Il est %H:%M:%S')
        #return datetime.datetime.now().strftime('                  Il est %H:%M:%S')
        
class CopieEcran(Thread):
    """Thread chargé d'envoyer une image écran toutes les heures."""
    def __init__(self):
        Thread.__init__(self)       
        with open('fp') as fp:
            self.thename = fp.readline().rstrip()
            self.thepasswd = fp.readline().rstrip()
            self.ok = True
            self.screencopy_delay = getDelay('screencopy_delay', 3600)
    
    def the_end(self):
        print 'fin de copie écran demandée'
        self.ok = False 

    def run(self):
        while self.ok:
            commands.getoutput('scrot screen.png')
            send(self.thename, self.thepasswd, 'Copie d\'écran', None, ['screen.png'])
            time.sleep(self.screencopy_delay)
        print 'fin de la mise à jour de la date'


class Nettoyage(Thread):
    """Thread chargé de supprimer les messages dépassés toutes les heures."""
    def __init__(self, frame):
        Thread.__init__(self)     
        self.frame = frame
        self.ok = True
        self.cleaning_delay = getDelay('cleaning_delay', 1200)
    
    def the_end(self):
        print 'fin du thread de nettoyage'
        self.ok = False 

    def run(self):
        while self.ok:
            self.frame.fill_labels()
            time.sleep(self.cleaning_delay)
            #time.sleep(10)
        print 'fin de la mise à jour de la date'

if not os.path.exists('.lock-panel'):  
    with open('.lock-panel', 'w'):
        pass
    try:
        frame = MainFrame()
    except:
        print "Problème au lancement"
        commands.getoutput('rm .lock-panel')
else:
    print "L'application semble déjà lancée"
    

#frame = MainFrame()