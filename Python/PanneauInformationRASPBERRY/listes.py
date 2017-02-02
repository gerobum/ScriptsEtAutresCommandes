# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:43:23 2017

@author: yvan
"""

import datetime
import sys
import re

# Construit une liste de messages à partir des fichiers lperm et lmes
# Les doublons de la liste sont enlevés et elle est autant que possible
# triée chronologiquement.
def get_liste():
    now = datetime.datetime.now()
    liste = []  
    try:          
        with open('lperm') as fp:
            for line in fp:
                line = line.decode('utf-8').strip().encode('utf-8')
                if not line.startswith('#', 0):
                    t = line.split(',')
                    if int(t[0]) == now.weekday():
                        liste.append(t[1])
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
        with open('lmes') as fp:
            for line in fp:
                liste.append(line.rstrip().decode('utf-8'))
    
    except TypeError as e:
        print "Type error({0})".format(e.message)   
        pass
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror) 
        pass                 
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass
    
    liste = list(set(liste))
    liste.sort(key=lambda s : critere(s))
#    print 'Sort'
    return liste
    
# Critère de tri pour la liste
def critere(s):
    if re.match('.*([0-9][0-9][h:][0-9]*).*', s):
    #if re.match('-(?)-', s):
        m = re.search('[^0-9]*([0-9][0-9][h:][0-9]*).*', s)
        return m.group(1)
    elif re.match('.*([0-9][h:][0-9]*).*', s):
        m = re.search('[^0-9]*([0-9][h:][0-9]*).*', s)
        return '0'+m.group(1)
    else:
        return 'zzzz'
        