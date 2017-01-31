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
import sys


locale.setlocale(locale.LC_TIME,'')

from threading import Thread

import time

from mailing import Mailing

class MainFrame(Tk):
    def __init__(self):
        Tk.__init__(self) 
        self.config(bg='black')
        self.title('Bonjour Maman')
        self.attributes('-fullscreen', True)


        self.thefont = tkFont.Font(family='Purisa',size=25, weight='bold')
        self.theMiddlefont = tkFont.Font(family='Purisa',size=35, weight='bold', slant='italic')
        self.theBigfont = tkFont.Font(family='Purisa',size=45, weight='bold', slant='italic')

    
        self.lintro = Label(self, text='Bonjour Maman', bg='#3209FF', fg='#FFFFDA', font=self.theBigfont)
        self.ldate = Label(self, text='', bg='#3209FF', fg='#FFFFDA', font=self.theMiddlefont)
        self.lheure = Label(self, text='', bg='#3209FF', fg='#FFFFDA', font=self.theBigfont) 
        
        self.bexit = Button(self, text='Quitter', command = self.the_end)         
        self.bminmax = Button(self, text='Minimise', command = self.mini_maxi)

        self.lintro.pack(fill='both')
        self.ldate.pack(fill='both')
        self.lheure.pack(fill='both')
        
        
        self.__init_labels()

       
        self.bexit.pack(side='left')  
        self.bminmax.pack(side='left')
                
        

        self.dh = DateHeure(self.ldate, self.lheure)
        self.mail = Mailing(self.ldate, self.lheure, self.lmes)
        
        self.dh.start()
        self.mail.start()
        self.mainloop()
                

                
    def __init_labels(self):     
        colors = ['#BAFFA8', '#FFFFD0']
        nbcolors = len(colors) # Nécessaire
        # Chargement des labels permanents  
        # Chaque ligne du fichier lperm a la forme suivante
        #<j>,<message>
        # où j est dans {1,2,3,4,5,6,7} pour 1 = lundi, 2 mardi, etc.
        self.lperm = []
        now=datetime.datetime.now()   
        i = 0
        try:
            with open('lperm') as fp:
                for line in fp:
                    line = line.decode('utf-8').strip().encode('utf-8')
                    if not line.startswith('#',0):
                        t = line.split(',')
                        if int(t[0]) == now.weekday():
                            label = Label(self, text=t[1], bg=colors[i%nbcolors], fg='black', font=self.thefont)
                            label.pack(fill='both', pady=1)
                            self.lperm.append(label)
                            i+=1
        except TypeError as e:
            print "Type error({0})".format(e.message)   
            pass
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror) 
            pass                 
        except:
            print "Unexpected error:", sys.exc_info()[0]
            pass
        
        self.lmes = []
        try:
            with open('lmes') as fp:
                for line in fp:
                    label = Label(self, text=line.rstrip().decode('utf-8'), bg=colors[i%nbcolors], fg='black', font=self.thefont)
                    label.pack(fill='both', pady=1)
                    self.lmes.append(label)
                    i+=1
        
        except TypeError as e:
            print "Type error({0})".format(e.message)   
            pass
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror) 
            pass                 
        except:
            print "Unexpected error:", sys.exc_info()[0]
            pass
        
        while i < 10:
            label = Label(self, text='', bg=colors[i%nbcolors], fg='black', font=self.thefont)
            label.pack(fill='both', pady=1)
            self.lmes.append(label)
            i+=1


    def mini_maxi(self):
        if self.bminmax['text'] == 'Minimise':
            self.bminmax['text']='Maximise'
            self.attributes('-fullscreen', False)
        else:
            self.bminmax['text']='Minimise'
            self.attributes('-fullscreen', True)
    
    def the_end(self):
        print 'fin générale'
        self.dh.the_end()
        self.dh.join()
        self.mail.the_end()
        self.mail.join()
        self.destroy()
    

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

MainFrame()
