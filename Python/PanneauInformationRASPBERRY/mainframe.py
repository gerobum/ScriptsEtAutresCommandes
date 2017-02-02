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
import re


locale.setlocale(locale.LC_TIME,'')

from threading import Thread

import time

class MainFrame(Tk):
    def __init__(self):
        Tk.__init__(self) 
        
        self.config(bg='black')
        self.title('Bonjour Maman')
        self.attributes('-fullscreen', True)


        self.thefont = tkFont.Font(family='Purisa',size=20, weight='bold')
        self.theMiddlefont = tkFont.Font(family='Purisa',size=30, weight='bold', slant='italic')
        self.theBigfont = tkFont.Font(family='Purisa',size=40, weight='bold', slant='italic')

    
        self.lintro = Label(self, text='Bonjour Maman', bg='#3209FF', fg='#FFFFDA', font=self.theBigfont, anchor='w')
        self.ldate = Label(self, text='', bg='#3209FF', fg='#FFFFDA', font=self.theMiddlefont, anchor='w')
        self.lheure = Label(self, text='', bg='#3209FF', fg='#FFFFDA', font=self.theBigfont, anchor='w') 
        
        self.bexit = Button(self, text='Quitter', command = self.the_end)         
        self.bminmax = Button(self, text='Minimise', command = self.mini_maxi)        
        self.bjournuit = Button(self, text='Jour', command = self.jour_nuit)
        self.delay = 60 # Délai de 1 minute entre chaque collecte de courrier.
        #self.jour = True

        self.lintro.pack(fill='both')
        self.ldate.pack(fill='both')
        self.lheure.pack(fill='both')        
        
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
            label = Label(self, text='', bg=colors[i%nbcolors], fg='black', font=self.thefont)
            label.pack(fill='both', pady=1)
            self.labels.append(label)
            
    def fill_labels(self):
        for label in self.labels:
            label['text'] = ''
            
        i = 0
        for s in get_liste():
            self.labels[i]['text'] = s
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
        print 'fin générale'
        #signal.signal(signal.SIGINT, handler)
        self.dh.the_end()
        self.dh.join()
        self.mail.the_end()
        self.mail.join()
        self.copie_ecran.the_end()
        #self.copie_ecran.join()
        self.nettoyage.the_end()
        #self.nettoyage.join()
        self.destroy()

def handler(signum, frame):
    print "do whatever, like call thread.interrupt_main()"

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
    
    def the_end(self):
        print 'fin de copie écran demandée'
        self.ok = False 

    def run(self):
        while self.ok:
            commands.getoutput('scrot screen.png')
            send(self.thename, self.thepasswd, 'Copie d\'écran', None, ['screen.png'])
            time.sleep(3600)
        print 'fin de la mise à jour de la date'


class Nettoyage(Thread):
    """Thread chargé de supprimer les messages dépassés toutes les heures."""
    def __init__(self, frame):
        Thread.__init__(self)     
        print 'Lancement du thread de nettoyage'
        self.frame = frame
        self.ok = True
    
    def the_end(self):
        print 'fin du thread de nettoyage'
        self.ok = False 

    def run(self):
        while self.ok:
            now = datetime.datetime.now()
            liste = []
            for label in self.frame.labels:
                texte = label['text'].strip()
                if texte != '':
                    if re.match('[^0-9]*([0-9]+)[h:][0-9]*[^0-9]*([0-9]+)[h:][0-9]*[^0-9]*', texte):
                        m = re.search('[^0-9]*([0-9]+)[h:][0-9]*[^0-9]*([0-9]+)[h:][0-9]*[^0-9]*', texte)
                        heure = int(m.group(2))
                    elif re.match('[^0-9]*([0-9]+)[h:][0-9]*.*', texte):
                        m = re.search('[^0-9]*([0-9]+)[h:][0-9]*.*', texte)
                        heure = int(m.group(1))
                    else:
                        heure = 24 # Pour être sur
                    
                    if now.hour - 2 <= heure:
                        liste.append(texte)
                        
            i = 0
            for s in liste:
                self.frame.labels[i]['text']=s
                i += 1
                
            for i in range(i, len(self.frame.labels)):
                self.frame.labels[i]['text']=''
                
            
            time.sleep(900)
        print 'fin de la mise à jour de la date'
        
            

MainFrame()
