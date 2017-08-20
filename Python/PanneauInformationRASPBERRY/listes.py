# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:43:23 2017

@author: yvan
"""

from datetime import datetime, time, date
import sys
import re
from chronotext import ChronologicText
import os

def appendToLperm(ct):
    sys.stderr.write("> LISTE.PY -> appendToLperm("+str(ct)+")\n")
    try:
        sys.stderr.write("- LISTE.PY -> appendToLperm : ouverture de tmp en w\n")
        with open('tmp', 'w') as fout:
            sys.stderr.write("- LISTE.PY -> appendToLperm : tmp ouvert en w\n")
            sys.stderr.write("- LISTE.PY -> appendToLperm : ouverture de lperm en r\n")
            with open('lperm') as fin:
                sys.stderr.write("- LISTE.PY -> appendToLperm : lperm ouvert en r\n")
                for c in fin:
                    sys.stderr.write("- LISTE.PY -> appendToLperm : lecture de "+c+"\n")
                    act = get_begin_end_day_text(c)                
                    sys.stderr.write("- LISTE.PY -> appendToLperm : écriture de "+str(ct)+"\n")
                    fout.write(str(act) + "\n")
                fout.write(str(ct) + "\n")

        with open('lperm', 'w') as fout:
            with open('tmp') as fin:
                for c in fin:
                    fout.write(c)
    except Exception as e:
        print 'erreur --', e 
    sys.stderr.write("< LISTE.PY -> appendToLperm("+str(ct)+")\n")

def purge_lperm():
    today = date.today()

    try:
        with open('tmp', 'w') as fout:
            with open('lperm') as fin:
                for c in fin:
                    ct = get_begin_end_day_text(c)
                    if ct.date() == None or ct.date() >= today: 
                        fout.write(str(ct) + "\n")

        with open('lperm', 'w') as fout:
            with open('tmp') as fin:
                for c in fin:
                    fout.write(c)
    except Exception as e:
        print 'erreur ', e   

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
        
def get_date(text):
    try:
        m = re.search('([0-9]+)/([0-9]+)/([0-9]+)', text)
        return date(int(m.group(3)),int(m.group(2)),int(m.group(1)))
    except:
        return None
    
        
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
# Elle peut s'écrire de 5 façons :
# 5. <d>§<h>§<h>§<j>§<t>
# 4.     <h>§<h>§<j>§<t>
# 3.         <h>§<j>§<t>
# 2.             <j>§<t>
# 1.                 <t>
# où <d> est une date (par exemple 02/03/2017 ou 2/03/2017 ou 2/3/2017) 
#    <h> est une heure (par exemple 10, 10h, 10h15, 10:15)
#    <j> est le jour (0 => lundi, 1 => mardi, ...)
#    <t> un texte sans §
#
# Dans le cas 5, la date est <d>
#                l'heure de début est le premier <h>
#                l'heure de fin   est le second  <h>
#                le jour est <j>
#
# Dans le cas 4, la date est aujourd'hui
#                l'heure de début est le premier <h>
#                l'heure de fin   est le second  <h>
#                le jour est <j>
#
# Dans le cas 3, la date est aujourd'hui
#                l'heure de début est <h> 
#                l'heure de fin est 23:59
#                le jour est <j>
#
# Dans le cas 2, la date est aujourd'hui
#                l'heure de début est 00:00
#                l'heure de fin   est 23:59
#                le jour est <j>
#
# Dans le cas 1, la date est aujourd'hui
#                l'heure de début est 00:00
#                l'heure de fin   est 23:59
#                le jour est '*' (tous les jours)
def get_begin_end_day_text(line):
    begin = time(0,0)
    end = time(23,59)
    day = '*'
    text = ''
    ddate = None
    
    
    t = line.split('§')
    l = len(t)
    hrf = time(23,59)
    if l == 5:
        ddate = get_date(t[0])
        begin = get_heure(t[1])
        end = get_heure(t[2], hrf)
        if t[3] >= '0' and t[3] <= '6':
            day = t[3]
        text = t[4]
    elif l == 4:
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
                                
    return ChronologicText(ddate, day, begin, end, text)
        
        
# Construit une liste de messages chronologiques à partir des fichiers lperm et lmes
# Les doublons de la liste sont enlevés et elle est triée chronologiquement.
def get_liste(liste = []):
    sys.stderr.write("Entre dans get_liste()\n")
    now = datetime.now()
    today = date.today()
    try:           
        with open('lperm') as fp:      
            for line in fp:
                # Une ligne comprend l'heure de début, de fin et un texte
                # Par exemple 10:00,12:00,Je passe à 14 heures.
                # séparés par une virgule. L'absence d'heure est remplacé par 23:59        
                line = line.decode('utf-8').encode('utf-8').strip() 
                sys.stderr.write("GET_LISTE : LECTURE de " + line + "\n")
                if not line.startswith('#', 0) and line!='': 
                    chronotext = get_begin_end_day_text(line)  
                    if chronotext.date() == None or chronotext.date() == today:
                        if chronotext.day() == '*' or int(chronotext.day()) == now.weekday(): 
                            liste.append(chronotext)
    except TypeError as e:
        print "Type error({0})".format(e.message)   
        pass
    except IOError as e:
        print "Erreur -> ",e.message()
        print "I/O error({0}): {1}".format(e.errno, e.strerror) 
        pass    
    except ValueError as e:
        print "Erreur lors de la lecture de lperm ", e    
        pass
    except AttributeError as e:
        sys.stderr.write("Erreur d'attribut "+ e.__str__() + '\n')    
        pass        
    except:
        sys.stderr.write('Erreur innatendu : ' + sys.exc_info()[0] + '\n')  
        pass
    
    try:
        if os.path.exists('lmes'): 
            with open('lmes') as fp:
                for line in fp:
                    line = line.decode('utf-8').encode('utf-8').strip()
                    if line != '':
                        liste.append(get_begin_end_day_text(line))
    
    except TypeError as e:
        print "Type error({0})".format(e.message)   
        pass
    except IOError as e:
        print "Error à l'ouverture de lmes"
        print "I/O error({0}): {1}".format(e.errno, e.strerror) 
        pass   
    except ValueError as e:
        print "Erreur lors de la lecture de lmes ", e
        pass  
    except AttributeError as e:
        sys.stderr.write("Erreur d'attribut "+ e.__str__() + '\n')    
        pass                
    except:
        sys.stderr.write("Erreur innatendue "+ sys.exc_info()[0] + '\n') 
        pass
    
    liste = list(set(liste))
    
    
    h = now.hour-1
    if h < 0:
        h = 23
    nowmoins1 = time(h, now.minute)
    
    liste = list(filter(lambda s : s.end()>nowmoins1, liste))
    liste.sort(key=lambda s : s.begin())
    
    sys.stderr.write("Sort de get_liste()\n")
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
        