# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:26:54 2017

@author: yvan
"""

from chronotext import ChronologicText
from datetime import time

def test1():
    t1=time(10)
    t2=time(10,5)
    t3=time(11,15)
    midi=time(12)
    lc = [
         ChronologicText('0',t1,t2,'Bonjour'),
         ChronologicText('0',t1,t2,'Bonjour'),
         ChronologicText('0',t1,t1,'Bonjour'),
         ChronologicText('0',t2,t2,'Bonjour'),
         ChronologicText('0',t1,t2,'Au revoir'),
         ChronologicText('0',t2,t3,'Bonjour')
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
 
    
    
    
def getDelay(key, default):
    try:
        with open('delays') as fp:
            return eval(fp.read())[key]
    except:
        return default
        
#print getDelay('mailing_delay', 100)
        
test1()        

