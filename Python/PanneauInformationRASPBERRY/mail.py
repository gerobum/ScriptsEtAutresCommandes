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
import sys

locale.setlocale(locale.LC_TIME,'')

from threading import Thread

import time

from mailing import Mailing


fmain = Tk();
fmain.config(bg='black')
fmain.title('Bonjour Maman')
fmain.attributes('-fullscreen', True)


tkFont.families()

thefont = tkFont.Font(family='Helvetica',size=30, weight='bold')
theMiddlefont = tkFont.Font(family='Geogia',size=40, weight='bold', slant='italic')
theBigfont = tkFont.Font(family='Geogia',size=50, weight='bold', slant='italic')

def the_date():
    return datetime.date.today().strftime('Aujourd\'hui, nous sommes %A %d %B %Y')

def the_time():
    return datetime.datetime.now().strftime('Il est %H:%M:%S')
    
lintro = Label(fmain, text='Bonjour Maman', bg='#3209FF', fg='white', font=theBigfont)
ldate = Label(fmain, text=the_date(), bg='#3209FF', fg='white', font=thefont, height=2)
lheure = Label(fmain, text=the_time(), bg='#3209FF', fg='white', font=thefont)  
lsep = Label(fmain, text='____________________________________________', bg='black', fg='white', font=thefont)   
lmes = [#Label(fmain, text='', bg='#FF3314', fg='white', font=thefont),
        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FF6810', fg='black', font=thefont),
        Label(fmain, text='', bg='#FFE810', fg='black', font=thefont),
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

ldate.pack(fill='both', pady=1)
lheure.pack(fill='both')
lsep.pack(fill='both')
for lm in lmes:
    lm.pack(fill='both')
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

