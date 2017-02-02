# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:26:54 2017

@author: yvan
"""

from chronotext import ChronologicText
from datetime import time

t1=time(10)
t2=time(10,5)
t3=time(11,15)
midi=time(12)

a=ChronologicText('0',t1,t2,'Bonjour')
aa=ChronologicText('0',t1,t2,'Bonjour')
b=ChronologicText('0',t1,t1,'Bonjour')
c=ChronologicText('0',t2,t2,'Bonjour')
d=ChronologicText('0',t1,t2,'Au revoir')
e=ChronologicText('0',t2,t3,'Bonjour')
f=ChronologicText('0',t3,midi,'Bonjour')

print a
print aa
print b
print c
print d
print e
print f

assert a==aa, 'a <> aa'
assert a!=b, 'a == b'
assert a!=d, 'a == d'

