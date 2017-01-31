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


fmain = Tk();
fmain.config(bg='black')
fmain.title('Bonjour Maman')
fmain.attributes('-fullscreen', True)


#tkFont.families()

#thefont = tkFont.Font(family='Caladea',size=35, weight='bold')
#theMiddlefont = tkFont.Font(family='Caladea',size=45, weight='bold', slant='italic')
#theBigfont = tkFont.Font(family='Caladea',size=55, weight='bold', slant='italic')
# La police ci-dessous est rigolote (genre Scrabble) mais pas très lisible
#thefont = tkFont.Font(family='Linux Biolinum Keyboard O',size=35, weight='bold')
#theMiddlefont = tkFont.Font(family='Linux Biolinum Keyboard O',size=45, weight='bold', slant='italic')
#theBigfont = tkFont.Font(family='Linux Biolinum Keyboard O',size=55, weight='bold', slant='italic')

#thefont = tkFont.Font(family='Purisa',size=25, weight='bold')
#theMiddlefont = tkFont.Font(family='Purisa',size=35, weight='bold', slant='italic')
#theBigfont = tkFont.Font(family='Purisa',size=45, weight='bold', slant='italic')

#thefont = tkFont.Font(family='URW Chancery L',size=25, weight='bold')
#theMiddlefont = tkFont.Font(family='URW Chancery L',size=35, weight='bold', slant='italic')
#theBigfont = tkFont.Font(family='URW Chancery L',size=45, weight='bold', slant='italic')

#thefont = tkFont.Font(family='URW Palladio L',size=25, weight='bold')
#theMiddlefont = tkFont.Font(family='URW Palladio L',size=35, weight='bold', slant='italic')
#theBigfont = tkFont.Font(family='URW Palladio L',size=45, weight='bold', slant='italic')

thefont = tkFont.Font(family='Purisa',size=25, weight='bold')
theMiddlefont = tkFont.Font(family='Purisa',size=35, weight='bold', slant='italic')
theBigfont = tkFont.Font(family='Purisa',size=45, weight='bold', slant='italic')



def the_date():
    return datetime.date.today().strftime('Aujourd\'hui, nous sommes %A %d %B %Y')

def the_time():
    return datetime.datetime.now().strftime('Il est %H:%M:%S')
    
lintro = Label(fmain, text='Bonjour Maman', bg='#3209FF', fg='#FFFFDA', font=theBigfont)
ldate = Label(fmain, text=the_date(), bg='#3209FF', fg='#FFFFDA', font=theMiddlefont)
lheure = Label(fmain, text=the_time(), bg='#3209FF', fg='#FFFFDA', font=theBigfont)  

lperm = [#Label(fmain, text='', bg='#FF3314', fg='white', font=thefont),
        Label(fmain, text='', bg='#BAFFA8', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFFFD0', fg='black', font=thefont),
        Label(fmain, text='', bg='#BAFFA8', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFFFD0', fg='black', font=thefont),
        ]

#lsep = Label(fmain, text='____________________________________________', bg='black', fg='white', font=thefont)   
lmes = [#Label(fmain, text='', bg='#FF3314', fg='white', font=thefont),
        Label(fmain, text='', bg='#BAFFA8', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFFFD0', fg='black', font=thefont),
        Label(fmain, text='', bg='#BAFFA8', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFFFD0', fg='black', font=thefont),
        Label(fmain, text='', bg='#BAFFA8', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFFFD0', fg='black', font=thefont),
        Label(fmain, text='', bg='#BAFFA8', fg='black', font=thefont),



#        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),

        #Label(fmain, text='', bg='#D1FF03', fg='black', font=thefont),
        #Label(fmain, text='', bg='#6CFF11', fg='#FF116C', font=thefont),
        #Label(fmain, text='', bg='#07FF5A', fg='#FF5A07', font=thefont),
#        Label(fmain, text='', bg='#09FFFF', fg='#FFFF09', font=thefont),
#        Label(fmain, text='', bg='#B60AFF', fg='#0AFFB6', font=thefont),
#        Label(fmain, text='', bg='#09FFFF', fg='#FFFF09', font=thefont),
#        Label(fmain, text='', bg='#6CFF11', fg='#FF116C', font=thefont),
#        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
#        Label(fmain, text='', bg='#FF3314', fg='white', font=thefont),
        #Label(fmain, text='', bg='#B60AFF', fg='#0AFFB6', font=thefont),
        #Label(fmain, text='', bg='#FF0BB6', fg='#0BB6FF', font=thefont)
        ]
   
# Chargement des labels enregistrés
i = 0
try:
    with open('lmes') as fp:
        for line in fp:
            lmes[i].config(text=line.rstrip().decode('utf-8'))
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

lintro.pack(fill='both');
ldate.pack(fill='both')
lheure.pack(fill='both')
#lsep.pack()

   
# Chargement des labels permanents  
# Chaque ligne du fichier lperm a la forme suivante
#<j>,<message>
# où j est dans {1,2,3,4,5,6,7} pour 1 = lundi, 2 mardi, etc.
now=datetime.datetime.now()   
i = 0
try:
    with open('lperm') as fp:
        for line in fp:
            line = line.decode('utf-8').strip().encode('utf-8')
            if not line.startswith('#',0):
                t = line.split(',')
                if int(t[0]) == now.weekday():
                    lperm[i].config(text=t[1])
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

lintro.pack(fill='both');
ldate.pack(fill='both')
lheure.pack(fill='both')
#lsep.pack()


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

ldate.pack(fill='both')
lheure.pack(fill='both')
#lsep.pack(fill='both')
for lm in lperm:
    lm.pack(fill='both', pady=1)
for lm in lmes:
    lm.pack(fill='both', pady=1)
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

