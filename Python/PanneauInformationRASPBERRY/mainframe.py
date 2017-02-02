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
import sys, os, traceback, commands
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import signal


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


        self.thefont = tkFont.Font(family='Purisa',size=20, weight='bold')
        self.theMiddlefont = tkFont.Font(family='Purisa',size=30, weight='bold', slant='italic')
        self.theBigfont = tkFont.Font(family='Purisa',size=40, weight='bold', slant='italic')

    
        self.lintro = Label(self, text='Bonjour Maman', bg='#3209FF', fg='#FFFFDA', font=self.theBigfont, anchor='w')
        self.ldate = Label(self, text='', bg='#3209FF', fg='#FFFFDA', font=self.theMiddlefont, anchor='w')
        self.lheure = Label(self, text='', bg='#3209FF', fg='#FFFFDA', font=self.theBigfont, anchor='w') 
        
        self.bexit = Button(self, text='Quitter', command = self.the_end)         
        self.bminmax = Button(self, text='Minimise', command = self.mini_maxi)        
        self.bjournuit = Button(self, text='Jour', command = self.jour_nuit)
        #self.jour = True

        self.lintro.pack(fill='both')
        self.ldate.pack(fill='both')
        self.lheure.pack(fill='both')        
        
        self.init_labels()
       
#        self.bexit.pack(side='left')  
#        self.bminmax.pack(side='left')
#        self.bjournuit.pack(side='left')                        

        self.dh = DateHeure(self.ldate, self.lheure)
        self.mail = Mailing(self)
        self.copie_ecran = CopieEcran()
        
        self.dh.start()
        self.mail.start()
        self.copie_ecran.start()
        self.mainloop()              
                
    def init_labels(self):  
#        
#        self.bexit.pack_forget()
#        self.bminmax.pack_forget()
#        self.bjournuit.pack_forget()
        
        colors = ['#BAFFA8', '#FFFFD0']
        nbcolors = len(colors) # Nécessaire
        # Chargement des labels permanents  
        # Chaque ligne du fichier lperm a la forme suivante
        #<j>,<message>
        # où j est dans {1,2,3,4,5,6,7} pour 1 = lundi, 2 mardi, etc.
        try:
            for label in self.lperm:
                label.destroy()
        except AttributeError as e:
            pass   
        
            
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
        
            
        try:
            for label in self.lmes:
                label.destroy()
        except AttributeError as e:
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
#
#        self.bexit.pack(side='left')
#        self.bminmax.pack(side='left')
#        self.bjournuit.pack(side='left')

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
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self):
        Thread.__init__(self)       
        with open('fp') as fp:
            self.thename = fp.readline().rstrip()
            self.thepasswd = fp.readline().rstrip()
            self.ok = True
    
    def the_end(self):
        print 'fin de copie écran demandée'
        self.ok = False 
        
    def send(self, subject, body=None, files=None):
        user = self.thename
        password = self.thepasswd
        
        try:
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.ehlo()
            s.starttls()
            s.ehlo
            s.login(user, password)
            msg = MIMEMultipart()
            msg['From'] = user
            msg['To'] = user
            msg['Subject'] = subject
            if body is not None:  
                msg.attach(MIMEText(body, 'plain'))     
            for img in files or []:
                if os.path.isfile(img):
                    with open(img, "rb") as fil:
                        part = MIMEApplication(
                            fil.read(),
                            Name=os.path.basename(img)
                        )
                    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(img)
                    msg.attach(part)
            s.sendmail(user, user, msg.as_string())
            s.quit()
        except Exception:
            sys.stderr.write(traceback.format_exc())    
            pass

    def run(self):
        while self.ok:
            commands.getoutput('scrot screen.png')
            self.send('Copie d\'écran', None, ['screen.png'])
            time.sleep(60*60)
        print 'fin de la mise à jour de la date'


MainFrame()
