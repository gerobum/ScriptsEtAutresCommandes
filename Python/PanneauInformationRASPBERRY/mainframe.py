# -*- encoding: utf-8 -*-
"""
Lecture mail

Created on Sat Jan 21 17:28:43 2017

@author: yvan
"""

from Tkinter import Label, Button, Tk, PhotoImage
import tkFont
import datetime
import locale
import commands
from mailing import Mailing
from mailing import send
from listes import get_liste
from chronotext import getDelay
from threading import Lock
import sys
import traceback
import re
import os



locale.setlocale(locale.LC_TIME,'')

from threading import Thread

import time

class MainFrame(Tk):
    def __init__(self):
        Tk.__init__(self) 
        
        self.lock = Lock()
        
        self.config(bg='black')
        self.title('Bonjour Maman')
        self.attributes('-fullscreen', True)
        
        #self.width = int(self.winfo_screenwidth()*0.995)
        self.width = int(self.winfo_screenwidth()*0.8)

        self.thefont = tkFont.Font(family='Purisa',size=20, weight='bold')
        self.theMiddlefont = tkFont.Font(family='Purisa',size=30, weight='bold', slant='italic')
        self.theBigfont = tkFont.Font(family='Purisa',size=40, weight='bold', slant='italic')

    
        self.lintro = Label(self, text='Bonjour Maman', wraplength=self.width, bg='#3209FF', fg='#FFFFDA', font=self.theBigfont, anchor='w')
        self.ldate = Label(self, text='', wraplength=self.width, bg='#3209FF', fg='#FFFFDA', font=self.theMiddlefont, anchor='w')
        self.lheure = Label(self, text='', wraplength=self.width, bg='#3209FF', fg='#FFFFDA', font=self.theBigfont, anchor='w') 
        
        
        self.images = []
        for i in range(3):
            photo = PhotoImage(file="images/image"+str(i)+".png")
            self.images.append(Label(self, image=photo))
            self.images[i].photo = photo 

        
        self.bexit = Button(self, text='Quitter', image=photo, command = self.the_end) 
        
        self.bminmax = Button(self, text='Minimise', command = self.mini_maxi)        
        self.bjournuit = Button(self, text='Jour', command = self.jour_nuit)
        
        self.mailing_delay = getDelay('mailing_delay', 71)

        self.lintro.pack(fill='both')
        self.ldate.pack(fill='both')
        self.lheure.pack(fill='both')     
        self.chronolist = []
        
        self.init_labels()
        self.fill_labels()   
        
        for image in self.images:
            image.pack(side='left')  
       
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
        
    def maj_photo(self, i):
        if i >= 0 and i < len(self.images):
            for image in self.images:
                image.pack_forget()
            
            for i in range(len(self.images)):
                photo = PhotoImage(file="images/image"+str(i)+".png")
                self.images[i].pack_forget()
                self.images[i] = Label(self, image=photo)
                self.images[i].photo = photo 
                self.images[i].pack(side='left')  
            

    def init_labels(self):
        colors = ['#BAFFA8', '#FFFFD0']
        nbcolors = len(colors) # Nécessaire
                
        self.labels = []          
        
        for i in range(10):
            label = Label(self, text='', wraplength=self.width, justify='left', bg=colors[i%nbcolors], fg='black', font=self.thefont)
            label.pack(fill='both', pady=1)
            self.labels.append(label)
        
            
    def fill_labels(self, ctext=None):
        self.lock.acquire()
        try:      
            for label in self.labels:
                label.pack_forget()
                
            self.labels = []    
                
            if ctext != None:
                self.chronolist.append(ctext)
            
            self.chronolist = get_liste(self.chronolist)

          
            colors = ['#BAFFA8', '#FFFFD0']
            nbcolors = len(colors) # Nécessaire
                          
            
            i = 0
            for s in self.chronolist:
                label = Label(self, text='', wraplength=self.width, justify='left', bg=colors[i%nbcolors], fg='black', font=self.thefont)
                label.pack(fill='both', pady=1)
                label['text'] = s.text().strip()
                self.labels.append(label)
                i+=1
        except IndexError as ie:            
            sys.stderr.write(ie.__str__()+'\n')  
            pass
            
        finally:
            self.lock.release()
                

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
        os.kill(os.getpid(), 9) # VIOLENT
        
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
        
def nbapp():
    return len(commands.getoutput('ps -ef | grep mainframe.py').split('\n')) - 2

# Au moment du test, l'application est déjà lancée. Il faut donc la chercher deux fois
if nbapp() > 1:
    print "L'application semble déjà lancée"
else:
    try: 
        frame = MainFrame()  
        print 'fin de la fenêtre principale'
    except:
        sys.stderr.write('Problème au lancement\n') 
        sys.stderr.write(traceback.format_exc()) 
  