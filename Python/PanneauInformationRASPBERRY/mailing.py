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

    
    def the_end(self):
        print 'fin de courrier'
        self.ok = False     
        
    def placer(self, message):
        if self.dernierMessage < len(self.lmes):
            self.lmes[self.dernierMessage].config(text = message)
            self.dernierMessage+=1

    def run(self):
        while self.ok:            
            box = imapy.connect(
                host='imap.gmail.com',
                username='mamie.rasp@gmail.com',
                password=self.thepasswd,
                # you may also specify custom port:
                # port=993
                ssl=True,
            )
            
            emails = box.folder('INBOX').emails(self.q.unseen())

            if len(emails) > 0:    
                for mail in emails:
                    mail.mark(['seen'])
                    if mail['subject'] == 'STOP':
                        mail.mark(['seen'])
                        # the_end()
                    elif mail['subject'] == 'FONT':
                        thesize = mail['text'][0]['text_normalized']
                        thefont = tkFont.Font(family='Helvetica',size=thesize, weight='bold')
                        self.ldate.config(font=thefont)
                    else:                        
                        self.placer(mail['text'][0]['text_normalized'])
            
            box.logout()
            #time.sleep(300)
            time.sleep(10)
        print 'fin de la collecte du courrier'