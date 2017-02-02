# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:43:23 2017

@author: yvan
"""

from datetime import datetime
from datetime import time
import sys
import re
from chronotext import ChronologicText

# Retourne une liste de messages sans doublon et ordonnée
# 
#def get_liste_from(labels, message):
#    liste = [message]
#    for label in labels:
#        liste.append(label['text'])
#    liste = list(set(liste))
#    #liste.sort(key=lambda s : critere(s))
#    liste.sort()
#    
#    return liste[-len(labels):]
    
# Une heure s'écrit sous les formes suivantes
#    10
#    10:25
#    5:2
#    10h20
#    23h
#    23:
def get_heure(s, default=time()):
    s = s.strip()
    mn = 0
    hr = 0
    
    if re.match('[0-9]+$', s):
        m = re.search('([0-9]+)$', s)
        hr = int(m.group(1))
    elif re.match('[0-9]+[h:]$', s):
        m = re.search('([0-9]+)[h:]$', s)
        hr = int(m.group(1))
    elif re.match('[0-9]+[h:][0-9]+$', s):
        m = re.search('([0-9]+)[h:]([0-9]+)$', s)
        hr = int(m.group(1))
        mn = int(m.group(2))
    else:
        return default
        
    if mn < 0 or mn > 59:
        mn = 0
    if hr >= 0 and hr < 24:
        return time(hr, mn)
    else:
        return default
        
def get_begin_end(text):
    begin = time(0,0)
    end = time(23,59)
    if re.match('.*[^0-9][0-9]+[h:][0-9]*.*[^0-9][0-9]+[h:][0-9]*.*', text):
        m = re.search('.*[^0-9]([0-9]+[h:][0-9]*).*[^0-9]([0-9]+[h:][0-9]*).*', text)
        begin = get_heure(m.group(1))
        end = get_heure(m.group(2))
    elif re.match('.*[^0-9][0-9]+[h:][0-9]*.*', text):
        m = re.search('.*[^0-9]([0-9]+[h:][0-9]*).*', text)
        begin = get_heure(m.group(1))
            
    return begin, end
  
# Une ligne contient toujours un texte et des informations chronologiques
# en début. Chaque partie est séparée de ses voisines par le caractère §
# Elle peut s'écrit de 4 façons :
# 4. <h>§<h>§<j>§<t>
# 3.     <h>§<j>§<t>
# 2.         <j>§<t>
# 1.             <t>
# où <h> est une heure (par exemple 10, 10h, 10h15, 10:15)
#    <j> est le jour (0 => lundi, 1 => mardi, ...)
#    <t> un texte sans §
#
# Dans le cas 4, l'heure de début est le premier <h>
#                l'heure de fin   est le second  <h>
#                le jour est <j>
#
# Dans le cas 3, l'heure de début est <h> 
#                l'heure de fin est 23:59
#                le jour est <j>
#
# Dans le cas 2, l'heure de début est 00:00
#                l'heure de fin   est 23:59
#                le jour est <j>
#
# Dans le cas 1, l'heure de début est 00:00
#                l'heure de fin   est 23:59
#                le jour est '*' (tous les jours)
def get_begin_end_day_text(line):
    begin = time(0,0)
    end = time(23,59)
    day = '*'
    text = ''
    
    t = line.split('§')
    l = len(t)
    hrf = time(23,59)
    if l == 4:
        begin = get_heure(t[0])
        end = get_heure(t[1], hrf)
        if t[2] >= '0' and t[2] <= '6':
            day = t[2]
        text = t[3]
    elif l == 3:
        begin = get_heure(t[0])
        if t[1] >= '0' and t[1] <= '6':
            day = t[1]
        text = t[2]
    elif l == 2:
        if t[0] >= '0' and t[0] <= '6':
            day = t[0]
        begin, end = get_begin_end(t[1])
        text = t[1]
    elif l == 1:
        begin, end = get_begin_end(t[0])
        text = t[0]
                                
    return ChronologicText(day, begin, end, text)
        
        
# Construit une liste de messages chronologiques à partir des fichiers lperm et lmes
# Les doublons de la liste sont enlevés et elle est triée chronologiquement.
def get_liste(liste = []):
    now = datetime.now()
    try:           
        with open('lperm') as fp:         
            for line in fp:
                # Une ligne comprend l'heure de début, de fin et un texte
                # Par exemple 10:00,12:00,Je passe à 14 heures.
                # séparés par une virgule. L'absence d'heure est remplacé par 23:59        
                line = line.decode('utf-8').strip().encode('utf-8').strip()   
                if not line.startswith('#', 0):
                    chronotext = get_begin_end_day_text(line)                 
                    if chronotext.day() == '*' or int(chronotext.day()) == now.weekday():
                        liste.append(chronotext)
    except TypeError as e:
        print "Type error({0})".format(e.message)   
        pass
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror) 
        pass    
    except ValueError as e:
        print "Erreur lors de la lecture de lperm ", e               
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass
    
    try:
        with open('lmes') as fp:
            for line in fp:
                liste.append(get_begin_end_day_text(line.strip()))
    
    except TypeError as e:
        print "Type error({0})".format(e.message)   
        pass
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror) 
        pass   
    except ValueError as e:
        print "Erreur lors de la lecture de lmes ", e
        pass               
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass
    
    liste = list(set(liste))
    nowplus1 = time(now.hour+1, now.minute)
    
    
    liste = list(filter(lambda s : s.end()>nowplus1, liste))
#    liste.sort(key=lambda s : critere(s.begin()))
    liste.sort(key=lambda s : s.begin())
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
        