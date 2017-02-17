# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:26:54 2017

@author: yvan
"""

from chronotext import ChronologicText
from datetime import time, datetime

def test1():
    t1=time(18)
    t2=time(18,5)
    t3=time(17,15)
    t4=time(17,5)
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
    t1=time(t)
    t2=time(t+1)
    t3=time(t+2,15)
    t4=time(t+2,30)
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
    nowmoins1 = time(h, now.minute)
    print now
    print nowmoins1
 
    lc = list(filter(lambda s : s.end()<nowmoins1, lc))
    
    for c in lc:
        print c
    
    
    
def getDelay(key, default):
    try:
        with open('delays') as fp:
            return eval(fp.read())[key]
    except:
        return default
        
#print getDelay('mailing_delay', 100)
        
test2()        

