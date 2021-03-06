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
import sys
import traceback
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import listes
from listes import appendToLperm
import jvcframe
from chronotext import getDelay
from files import cat

nbmailingerror = 0

def send(user, password, subject, body=None, files=None):       
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
        sys.stderr.write('mailing.py send')
        sys.stderr.write(traceback.format_exc())    

class ReceiveMail(Thread):
    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.error_delay = 900
                      
    def run(self):    
        global nbmailingerror
        #if nbmailingerror > 10:
        #    commands.getoutput('shutdown -r now')
                             
        if nbmailingerror > 10:
            self.parent.parent.restart_mail()
        
        try:
            box = imapy.connect(
                host='imap.gmail.com',
                username=self.parent.thename,
                password=self.parent.thepasswd,
                # you may also specify custom port:
                # port=993
                ssl=True,
            )            
        except:
            self.parent.parent.mailing_delay = self.error_delay
            nbmailingerror+=1
            print "Nb erreurs ", nbmailingerror
            print "Unexpected error in ReceiveMail: box = imapy.connect(...)", sys.exc_info()[0]
            try:
                box.logout()             
            except:
                nbmailingerror+=1
                
                if nbmailingerror > 10:
                    self.parent.parent.restart_mail()
                    
                print "Nb erreurs ", nbmailingerror
                print "Unexpected error in ReceiveMail: dans le box.logout() du box = imapy.connect(...)", sys.exc_info()[0]
            return
         
        try:
            emails = box.folder('INBOX').emails(self.parent.q.unseen())            
        except:
            self.parent.parent.mailing_delay = self.error_delay
            nbmailingerror+=1                
            if nbmailingerror > 10:
                self.parent.parent.restart_mail()
                
            print "Nb erreurs ", nbmailingerror
            print "Unexpected error in ReceiveMail: emails = box.folder('INBOX')...", sys.exc_info()[0]
            try:
                box.logout()             
            except:
                nbmailingerror+=1
                print "Nb erreurs ", nbmailingerror
                print "Unexpected error in ReceiveMail: dans le box.logout() du emails = box.folder('INBOX')...", sys.exc_info()[0]
                if nbmailingerror > 10:
                    self.parent.parent.restart_mail()
                    
            return           

        try:
            if len(emails) > 0:    
                for mail in emails:
                    mail.mark(['seen'])
    # ------------------------------------------------                
                    if mail['subject'] == 'ALL FONT':
                        thesize = int(mail['text'][0]['text_normalized'])
                        thefont = tkFont.Font(family='Helvetica',size=thesize, weight='bold')
                        self.parent.parent.theBigfont = thefont
                        self.parent.parent.theMiddlefont = thefont
                        self.parent.parent.thefont = thefont
                        self.parent.parent.lintro.config(font=thefont)             
                        self.parent.parent.ldate.config(font=thefont)             
                        self.parent.parent.lheure.config(font=thefont)
                        for label in self.parent.parent.labels:
                            label.config(font=thefont)
    # ------------------------------------------------  
                    elif mail['subject'] == 'CAT LMES':  
                        txt = cat('lmes')
                        send (self.parent.thename, self.parent.thepasswd, "Contenu de lmes", txt)


    # ------------------------------------------------  
                    elif mail['subject'] == 'CAT LPERM':  
                        txt = cat('lperm')
                        send (self.parent.thename, self.parent.thepasswd, "Contenu de lmes", txt)

    # ------------------------------------------------  
                    elif mail['subject'] == 'COMMANDE':  
                        cmd = mail['text'][0]['text_normalized']
                        txt = commands.getoutput(cmd)
                        send (self.parent.thename, self.parent.thepasswd, cmd, txt)
    # ------------------------------------------------  
                    elif re.match('DELAY ([0-9]+)', mail['subject']):
                        try:
                            m = re.search('DELAY ([0-9]+)', mail['subject'])
                            p = int(m.group(1))
                            if p >= 10:
                                self.parent.mailing_delay = p
                        except ValueError:
                            pass
    # ------------------------------------------------  
                    elif mail['subject'] == 'FONT':
                        thesize = mail['text'][0]['text_normalized']
                        thefont = tkFont.Font(family='Helvetica',size=thesize, weight='bold')
                        self.parent.ldate.config(font=thefont)
    # ------------------------------------------------  
                    elif mail['subject'] == 'GIT PULL REBOOT':
                        commands.getoutput('git-pull-reboot')
    # ------------------------------------------------  
                    elif mail['subject'] == 'HELP':     
                        try:
                            with open('help.txt') as fp:
                                message = []
                                for line in fp:
                                    #line = line.decode('utf-8').encode('utf-8')
                                    message.append(line)
                                send(self.parent.thename, self.parent.thepasswd, 'HELP?', ''.join(message))
                                    
                        except TypeError as e:
                            print "Type error({0})".format(e.message)   
                        except IOError as e:
                            print "I/O error({0}): {1}".format(e.errno, e.strerror)               
                        except:
                            print "Unexpected error:", sys.exc_info()[0]
    # ------------------------------------------------  
                    elif mail['subject'] == 'MINMAX':                        
                        self.parent.parent.mini_maxi()
    # ------------------------------------------------  
                    elif mail['subject'] == 'MSGS':  
                        for line in mail['text'][0]['text_normalized'].replace('\r\n', '').replace('\n', '').replace('\\t', '\n').splitlines():                      
                            self.parent.push(line.replace('\\n', '\n')) 
    # ------------------------------------------------  
                    elif mail['subject'] == 'MSG':  
                        #sys.stderr.write("MAILING.PY -> RECEIVEMAIL -> MSG : " + mail['subject'] + "\n")
                        #sys.stderr.write("MAILING.PY -> RECEIVEMAIL -> MSG : " + mail['text'][0]['text_normalized'] + "\n")                        
                        #sys.stderr.write("MAILING.PY -> RECEIVEMAIL -> MSG : " + str(type(mail['text'][0]['text_normalized'])) + "\n")
                        self.parent.push(mail['text'][0]['text_normalized'].replace('\r\n', '').replace('\n', '').replace('\\n', '\n')) 
    # ------------------------------------------------       
                    elif re.match('REP ([0-9]+)', mail['subject']):
                        try:
                            m = re.search('REP ([0-9]+)', mail['subject'])
                            p = int(m.group(1))                      
                            self.parent.replace(p, mail['text'][0]['text_normalized'])
                        except ValueError as v:  
                            sys.stderr.write('mailing.py ReceiveMail run')
                            sys.stderr.write(str(v))
                            sys.stderr.write(traceback.format_exc())                
    # ------------------------------------------------  
                    elif mail['subject'] == 'FICHIER':  
                        try:                      
                            for attachment in mail['attachments']:
                                file_name = attachment['filename']
                                data = attachment['data']
                                
                                if len(data) < 500000: 
                                    with open(file_name, 'w') as f:
                                        f.write(data)
                        except:                        
                            sys.stderr.write(traceback.format_exc()) 
    # ------------------------------------------------  
                    elif mail['subject'] == 'JVC ON':  
                        try:                      
                            self.jvc = jvcframe.JVCFrame()
                        except:                        
                            sys.stderr.write(traceback.format_exc()) 
    # ------------------------------------------------  
                    elif mail['subject'] == 'JVC OFF':  
                        try:                      
                            self.jvc.the_end()
                        except:                        
                            sys.stderr.write(traceback.format_exc()) 
    # ------------------------------------------------  
                    elif mail['subject'] == 'PHOTO':  
                        try:                      
                            for attachment in mail['attachments']:
                                file_name = attachment['filename']
                                data = attachment['data']
                                content_type = attachment['content_type']
                                
                                if re.match('image[0-9]\.png', file_name) and len(data) < 500000 and content_type == 'image/png': 
                                    m = re.search('image([0-9])\.png', file_name)
                                    n = int(m.group(1))
                                    with open('images/'+file_name, 'w') as f:
                                        f.write(data)
                                    self.parent.parent.maj_photo(n)
                        except:                        
                            sys.stderr.write(traceback.format_exc()) 
    # ------------------------------------------------  
                    elif mail['subject'] == 'SCREEN OFF':
                        commands.getoutput('xset dpms force off')  
    # ------------------------------------------------    
                    elif mail['subject'] == 'SCREEN ON':
                        commands.getoutput('xset dpms force on')  
    # ------------------------------------------------  
                    elif mail['subject'] == 'SCROT':  
                        commands.getoutput('scrot screen.png')
                        send(self.parent.thename, self.parent.thepasswd, 'Copie d\'écran', None, ['screen.png'])  
    # ------------------------------------------------  
                    elif mail['subject'] == 'STOP':
                        self.parent.parent.the_end()
    # ------------------------------------------------  
                    elif re.match('SUP ([0-9]+)$', mail['subject']):
                        try:
                            m = re.search('SUP ([0-9]+$)', mail['subject'])
                            p = int(m.group(1))                      
                            self.parent.sup(p)
                        except ValueError as v:  
                            sys.stderr.write('mailing.py ReceiveMail run')
                            sys.stderr.write(v)
                            sys.stderr.write(traceback.format_exc())   
                            
                        except:  
                            sys.stderr.write('mailing.py ReceiveMail run')
                            sys.stderr.write(traceback.format_exc())   
                            
    # ------------------------------------------------  
                    elif re.match('SUP ([0-9]+)-([0-9]+)', mail['subject']):
                        try:
                            m = re.search('SUP ([0-9]+)-([0-9]+)', mail['subject'])
                            p = int(m.group(1))  
                            q = int(m.group(2))                    
                            self.parent.sup(p, q+1)
                        except ValueError as v:  
                            sys.stderr.write('mailing.py ReceiveMail run')
                            sys.stderr.write(v)
                            sys.stderr.write(traceback.format_exc())   
                            
                        except:  
                            sys.stderr.write('mailing.py ReceiveMail run')
                            sys.stderr.write(traceback.format_exc())   
                            
        except:
            self.parent.parent.mailing_delay = self.error_delay
            nbmailingerror+=1
            print "Nb erreurs ", nbmailingerror
            print "Unexpected error in ReceiveMail: dans la suite de if", sys.exc_info()[0]
                           
            if nbmailingerror > 10:
                self.parent.parent.restart_mail()
                
            try:
                box.logout()             
            except:
                print "Unexpected error in ReceiveMail: dans le box.logout() de la suite de if", sys.exc_info()[0]
           
            return
            
        try:
            box.logout()             
        except:
            self.parent.parent.mailing_delay = self.error_delay
            nbmailingerror+=1 
                    
            if nbmailingerror > 10:
                self.parent.parent.restart_mail()
                
            print "Nb erreurs ", nbmailingerror
            print "Unexpected error in ReceiveMail: dans le box.logout()", sys.exc_info()[0]
            return
            
        self.parent.parent.mailing_delay = getDelay('mailing_delay', 71)
        nbmailingerror = 0


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
            
        
        with open('jn') as jn:
            self.beginhour = jn.readline().rstrip()
            self.endhour = jn.readline().rstrip()
                
        
    def __switchscreen(self):        
        if int(datetime.datetime.now().hour) > int(self.beginhour) and int(datetime.datetime.now().hour) < int(self.endhour):
            if not os.path.exists('lmes'):   
                # La création du fichier indique qu'il fait jour
                with open('lmes', 'w'):
                    pass
                self.parent.fill_labels()
                commands.getoutput('xset dpms force on')
        else:
            if os.path.exists('lmes'):
                os.remove('lmes') 
            self.parent.chronolist = []
            for label in self.parent.labels:
                label['text'] = ''
            commands.getoutput('xset dpms force off')
                
            
    def __writelabels(self):
        try:
            # Si le fichier n'existe pas, c'est la nuit
            if os.path.exists('lmes'):
                with open('lmes', 'w') as fp:
                    for chrono in self.parent.chronolist:
                        if str(chrono).strip() != '':
                            fp.write(''.join([str(chrono).strip().replace('\n', '\\n'),'\n'])) 
#                    for label in self.parent.labels:
#                        if label['text'].strip() != '':
#                            fp.write(''.join([label['text'].strip(),'\n']).encode('utf-8')) 

        except TypeError as e:
            sys.stderr.write("Type error({0})".format(e.message))
            
        except IOError as e:
            sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror)) 
            
        except AttributeError as e:
            sys.stderr.write("Erreur d'attribut "+ e.__str__() + '\n')    
            
        except:
            sys.stderr.write('Erreur innatendu : ' + sys.exc_info()[0] + '\n')  
            
               
    def push(self, message): 
        #sys.stderr.write("> MAILING.PY -> PUSH " + str(message) + "\n")
        today = datetime.date.today()
        if message.strip() != '':
            #sys.stderr.write("- MAILING.PY -> PUSH : avant CT\n")
            ct = listes.get_begin_end_day_text(message)
            #sys.stderr.write("- MAILING.PY -> PUSH : après CT\n")
######################################################            
#            self.parent.fill_labels(ct)
            if ct.date() == None and ct.day != '*':
                appendToLperm(ct)
            elif ct.date() == None or ct.date() == today:
                self.parent.fill_labels(ct)
            elif ct.date() > today:
                appendToLperm(ct)
#######################################################          
        #sys.stderr.write("< MAILING.PY -> PUSH " + str(message) + "\n")
        
    def sup(self, p, q = None):        
        if q == None:
            q = p+1

        commands.getoutput('rm lmes')
        del self.parent.chronolist[p:q]
        self.parent.fill_labels()
           
    def replace(self, p, message):
        if p >= 0 and p < len(self.parent.chronolist):
            self.sup(p)
            self.push(message)
        
    
    def the_end(self):
        print 'fin de courrier'
        self.ok = False  

    def run(self):
        while self.ok: 
            try:
                som = ReceiveMail(self)
                som.start()
                time.sleep(5)
                self.__switchscreen()
                self.__writelabels()
                   
            except:
                sys.stderr.write('Erreur innatendu : ' + str(sys.exc_info()[0]) + '\n')  

            time.sleep(self.parent.mailing_delay)
        print 'fin de la collecte du courrier'