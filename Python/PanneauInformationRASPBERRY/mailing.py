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
import datetime
import sys

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
                elif mail['subject'] == 'MSG':                        
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
        
        with open('fp') as fp:
            self.thepasswd = fp.read() 
               
    def replace(self, i, message):
        self.lmes[i].config(text = message)
        
    def __switchscreen(self):
        if datetime.datetime.now().hour > 8 and datetime.datetime.now().hour < 20:
            commands.getoutput('xset dpms force on')
        else:
            commands.getoutput('xset dpms force off')
            
    def __writelabels(self):
        try:
            with open('lmes', 'w') as fp:
                for label in self.lmes:
                    fp.write(''.join([label['text'],'\n']).encode('utf-8')) 
            #with open('lmes', 'w', 'utf-8') as fp:
                #for label in self.lmes:
                    #print label
                    #print label['text']
                    #fp.write(label['text']) 
        except TypeError as e:
            print "Type error({0})".format(e.message)   
            pass
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror) 
            pass                 
        except:
            print "Unexpected error:", sys.exc_info()[0]
            pass
               
    def push(self, message):
        i = 0
        while i < len(self.lmes):
            if self.lmes[i]['text'].strip() == '':
                self.lmes[i].config(text = message)
                return
            i+=1
        
        i = 1
        while i < len(self.lmes):
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
            #self.__switchscreen()
            self.__writelabels()
            time.sleep(10)
        print 'fin de la collecte du courrier'