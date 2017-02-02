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
import sys, traceback
import os
import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

class ReceiveMail(Thread):
    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        
#    def send(self, subject, body):
#        user = self.parent.thename
#        password = self.parent.thepasswd
#        try:
#            s = smtplib.SMTP("smtp.gmail.com", 587)
#            s.ehlo()
#            s.starttls()
#            s.ehlo
#            s.login(user, password)
#            msg = MIMEText(body,'plain')
#            msg['Subject'] = subject
#            msg['From'] = user
#            msg['To'] = user
#            s.sendmail(user, user, msg.as_string())
#            s.quit()
#        except Exception:
#            sys.stderr.write(traceback.format_exc())    
#            pass
        
    def send(self, subject, body=None, files=None):
        user = self.parent.thename
        password = self.parent.thepasswd
        
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
        
    
#    def sendMail(self, subject, body=None, files=None):
#        user = self.parent.thename
#        password = 'ton_mot_de_passe'
#        try:
#            s = smtplib.SMTP("smtp.gmail.com", 587)
#            s.ehlo()
#            s.starttls()
#            s.ehlo
#            s.login(user, password)
#            msg = MIMEMultipart()
#            msg['From'] = 'domesange@gmail.com'
#            msg['To'] = 'domesange@gmail.com'
#            msg['Subject'] = subject
#            if body is not None:
#                msg.attach(MIMEText(body.encode('utf-8'), 'plain', 'utf-8'))
#            for img in files or []:
#                if os.path.isfile(img):
#                    with open(img, "rb") as fil:
#                        part = MIMEApplication(
#                            fil.read(),
#                            Name=basename(img)
#                        )
#                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(img)
#                    msg.attach(part)
#            s.sendmail('domesange@gmail.com', 'domesange@gmail.com', msg.as_string())
#            s.quit()
#        except Exception:
#            sys.stderr.write(traceback.format_exc())    
            

    def run(self):     
        box = imapy.connect(
            host='imap.gmail.com',
            username=self.parent.thename,
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
                    self.parent.parent.the_end()
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
                elif mail['subject'] == 'COMMANDE':  
                    cmd = mail['text'][0]['text_normalized']
                    txt = commands.getoutput(cmd)
                    print cmd, '\n', txt
                    self.send (cmd, txt)
                elif mail['subject'] == 'MINMAX':                        
                    self.parent.parent.mini_maxi()

        box.logout()


class Mailing(Thread):
    """Thread chargé simplement d'afficher une lettre dans la console."""
    def __init__(self,parent):
        Thread.__init__(self)
        self.q = Q()
        self.ok = True
        self.parent = parent
        
        with open('fp') as fp:
            self.thename = fp.readline().rstrip()
            self.thepasswd = fp.readline().rstrip()
               
    def replace(self, i, message):
        if i < len(self.parent.lperm):
            self.parent.lperm[i].config(text = message)
        else:
            self.parent.lmes[i-len(self.parent.lperm)].config(text = message)
                
        
    def __switchscreen(self):        
        if datetime.datetime.now().hour > 8 and datetime.datetime.now().hour < 20:
            if not os.path.exists('lmes'):   
                # La création du fichier indique qu'il fait jour
                with open('lmes', 'w'):
                    pass
                self.parent.init_labels()
                commands.getoutput('xset dpms force on')
        else:
            if os.path.exists('lmes'):
                for label in self.parent.lmes:
                    label['text'] = ''
                for label in self.parent.lperm:
                    label['text'] = ''
                os.remove('lmes') 
                commands.getoutput('xset dpms force off')
                
#        if datetime.datetime.now().hour > 8 and datetime.datetime.now().hour < 20:
#            if not os.path.exists('lmes'):   
#                # La création du fichier indique qu'il fait jour
#                with open('lmes', 'w'):
#                    print 'Jour'
#                self.parent.init_labels()
#                commands.getoutput('xset dpms force on')
#        else:
#            if os.path.exists('lmes'):
#                print 'Nuit'
#                for label in self.parent.lmes:
#                    label['text'] = ''
#                for label in self.parent.lperm:
#                    label['text'] = ''
#                os.remove('lmes') 
#                commands.getoutput('xset dpms force off')
            
    def __writelabels(self):
        try:
            # Si le fichier n'existe pas, c'est la nuit
            if os.path.exists('lmes'):
                with open('lmes', 'w') as fp:
                    for label in self.parent.lmes:
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
        while i < len(self.parent.lmes):
            if self.parent.lmes[i]['text'].strip() == '':
                self.parent.lmes[i].config(text = message)
                return
            i+=1
        
        i = 1
        while i < len(self.parent.lmes):
            self.parent.lmes[i-1].config(text = self.parent.lmes[i]['text'])
            i+=1
        self.parent.lmes[len(self.parent.lmes)-1].config(text = message)

    
    def the_end(self):
        print 'fin de courrier'
        self.ok = False  

    def run(self):
        while self.ok:            
            som = ReceiveMail(self)
            som.start()
            #time.sleep(300)
            self.__switchscreen()
            self.__writelabels()
            time.sleep(15)
        print 'fin de la collecte du courrier'