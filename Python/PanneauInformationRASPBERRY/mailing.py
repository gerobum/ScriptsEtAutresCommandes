# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 18:37:26 2017

@author: yvan
"""
import imapy
from imapy.query_builder import Q
from threading import Thread
import time
import tkFont
import commands
import re

class SendOneMail(Thread):
    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent

    def run(self):          
        box = imapy.connect(
            host='imap.gmail.com',
            username='mamie.rasp@gmail.com',
            password=self.parent.thepasswd,
            # you may also specify custom port:
            # port=993
            ssl=True,
        )
        
        emails = box.folder('INBOX').emails(self.parent.q.unseen())

        if len(emails) > 0:    
            for mail in emails:
                mail.mark(['seen'])
                if mail['subject'] == 'STOP':
                    mail.mark(['seen'])
                elif re.match('REP ([0-9]+)', mail['subject']):
                    m = re.search('REP ([0-9]+)', mail['subject'])
                    p = int(m.group(1))
                    self.parent.replace(p, mail['text'][0]['text_normalized'])
                elif mail['subject'] == 'GIT PULL REBOOT':
                    commands.getoutput('git-pull-reboot')
                elif mail['subject'] == 'SCREEN ON':
                    commands.getoutput('xset dpms force on')
                elif mail['subject'] == 'SCREEN OFF':
                    commands.getoutput('xset dpms force off')
                elif mail['subject'] == 'FONT':
                    thesize = mail['text'][0]['text_normalized']
                    thefont = tkFont.Font(family='Helvetica',size=thesize, weight='bold')
                    self.parent.ldate.config(font=thefont)
                else:                        
                    self.parent.push(mail['text'][0]['text_normalized'])
        
        box.logout()


class Mailing(Thread):
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self,ldate,lheure,lmes):
        Thread.__init__(self)
        self.q = Q()
        self.ok = True
        self.ldate = ldate
        self.lheure = lheure
        self.lmes = lmes
        self.dernierMessage = 0;
        
        fp = open('fp')
        self.thepasswd = fp.read()
        fp.close()     
               
    def replace(self, i, message):
        print 'Placement de ', message, ' en position ', i
        self.lmes[i].config(text = message)

        
               
    def push(self, message):
        if self.dernierMessage < len(self.lmes):
            self.lmes[self.dernierMessage].config(text = message)
            self.dernierMessage+=1
        else:
            i = 1
            while i < self.dernierMessage:
                self.lmes[i-1].config(text = self.lmes[i]['text'])
                i+=1
            self.lmes[len(self.lmes)-1].config(text = message)

    
    def the_end(self):
        print 'fin de courrier'
        self.ok = False  

    def run(self):
        while self.ok:            
            som = SendOneMail(self)
            som.start()
            #time.sleep(300)
            time.sleep(10)
        print 'fin de la collecte du courrier'