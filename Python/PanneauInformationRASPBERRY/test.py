# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:26:54 2017

@author: yvan
"""

from chronotext import ChronologicText
import datetime
import listes
import re
import imapy
from imapy.query_builder import Q
import commands
import re

def test1():
    t1=datetime.time(18)
    t2=datetime.time(18,5)
    t3=datetime.time(17,15)
    t4=datetime.time(17,5)
    lc = [
         ChronologicText('*',t1,t1,'Bonjour'),
         ChronologicText('*',t1,t2,'Hello'),
         ChronologicText('*',t1,t3,'Bonjour'),
         ChronologicText('*',t2,t4,'Bonjour'),
         ChronologicText('*',t4,t4,'Au revoir'),
         ChronologicText('*',t4,t4,'Bonjour')
         ]
   
 
    assert lc[0]==lc[1], 'a <> aa'
    assert lc[0]==lc[3], 'a == b'
    assert lc[0]!=lc[4], 'a == d'
  
    
    print '----------'
    
    
    for i in range(len(lc)):
        for j in range(len(lc)):
            if lc[i] == lc[j]:
                print lc[i], " == ", lc[j]
            else:
                print lc[i], " <> ", lc[j]

    for c in lc:
        print c

        
    lc = list(set(lc))
    print '----------'
    for c in lc:
        print c
 
 
def test2():
    t=18
    t1=datetime.time(t)
    t2=datetime.time(t+1)
    t3=datetime.time(t+2,15)
    t4=datetime.time(t+2,30)
    lc = [
         ChronologicText('*',t1,t1,t1.__str__()+' -> '+t1.__str__()),
         ChronologicText('*',t1,t2,t1.__str__()+' -> '+t2.__str__()),
         ChronologicText('*',t1,t3,t1.__str__()+' -> '+t3.__str__()),
         ChronologicText('*',t2,t4,t2.__str__()+' -> '+t4.__str__()),
         ChronologicText('*',t4,t4,t4.__str__()+' -> '+t4.__str__())
         ]
   
    now = datetime.now()
    h = now.hour-1
    if h < 0:
        h = 23
    nowmoins1 = datetime.time(h, now.minute)
    print now
    print nowmoins1
 
    lc = list(filter(lambda s : s.end()<nowmoins1, lc))
    
    for c in lc:
        print c
    
def test3():
    print listes.get_date('09/03/1965')        
    datetime.date.today()
    
def test4(text):
    m = re.search('([0-9]+)/([0-9]+)/([0-9]+)', text)
    print 'Les groupes trouvés -> ', m.group(3), '#', m.group(2),'#',m.group(1)
    print datetime.date(int(m.group(3)),int(m.group(2)),int(m.group(1)))
    
def test5():
    with open('fp') as fp:
        thename = fp.readline().rstrip()
        thepasswd = fp.readline().rstrip()
    box = imapy.connect(
                host='imap.gmail.com',
                username=thename,
                password=thepasswd,
                # you may also specify custom port:
                # port=993
                ssl=True,
            )
    q = Q()
    emails = box.folder('INBOX').emails(q.unseen())
    for email in emails:
        for attachment in email['attachments']:
            print 'Nom : ',attachment['filename']
            print 'Taille : ',len(attachment['data'])
            print 'Type : ',attachment['content_type']
        
    box.logout()
    
def test6():
    if re.search('python mainframe\.py.*python mainframe\.py', commands.getoutput('ps -ef | grep mainframe')):
        print "L'application est déjà lancée"
    else:
        print "L'application n'est pas lancée"
        
def test7(s):
    print len(commands.getoutput('ps -ef | grep '+s).split('\n')) - 1
    
    
def getDelay(key, default):
    try:
        with open('delays') as fp:
            return eval(fp.read())[key]
    except:
        return default
        
def test8():
    try:
        with open('lperm') as fp:
            x = fp.read()
            for c in fp:
                print c
    except:
        print 'erreur'
    
            
def test9():
    today = datetime.date.today()

    try:
        with open('tmp', 'w') as fout:
            with open('lperm') as fin:
                for c in fin:
                    ct = listes.get_begin_end_day_text(c)
                    if ct.date() == None or ct.date() >= today: 
                        fout.write(ct.__str__() + "\n")

        with open('lperm', 'w') as fout:
            with open('tmp') as fin:
                for c in fin:
                    fout.write(c)
    except Exception as e:
        print 'erreur ', e   
                
    print "done"
#print getDelay('mailing_delay', 100)

def appendToLperm(ct):
    try:
        with open('tmp', 'w') as fout:
            with open('lperm') as fin:
                for c in fin:
                    act = listes.get_begin_end_day_text(c)
                    fout.write(str(act) + "\n")
                fout.write(str(ct) + "\n")

        with open('lperm', 'w') as fout:
            with open('tmp') as fin:
                for c in fin:
                    fout.write(c)
    except Exception as e:
        print 'erreur ', e 
    
def push(message): 
      today = datetime.date.today()
      if message.strip() != '':
          ct = listes.get_begin_end_day_text(message)
          if ct.date() == None or ct.date() == today:
              print "Aujoud'hui -->", ct
          elif ct.date() < today:
              print "avant -->", ct   
          else:
              print "après -->", ct
        
def cat(fileName):
    try:
        list = []
        with open(fileName) as fin:
            for c in fin:
                list.append(c)
        return ''.join(list)
    except Exception as e:
        return 'no file : ' + fileName 

print cat('xxx')
print 'done'


