# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 21:02:41 2017

@author: yvan
"""

    
def getDelay(key, default):
    try:
        with open('delays') as fp:
            return eval(fp.read())[key]
    except:
        return default
        

class ChronologicText:
    def __init__(self, day, begin, end, text):
        self.__day = day
        self.__begin = begin
        self.__end = end
        self.__text = text
        
    def begin(self):
        return self.__begin
        
    def end(self):
        return self.__end
        
    def text(self):
        return self.__text
        
    def day(self):
        return self.__day
        
    def __str__(self):
        return ''.join([str(self.__begin.hour),':',str(self.__begin.minute),'§',str(self.__end.hour),':',str(self.__end.minute),'§',self.__day,'§',self.__text])
        
    def __eq__(self, other):
            if other == None:
                return False
        #if isinstance(other, self.__class__):
#            return self.__dict__ == other.__dict__
            return self.__begin == other.__begin and \
                   self.__end == other.__end and \
                   self.__text == other.__text
#        else:
#            return False

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __hash__(self):
        return hash(self.__begin) ^ \
               hash(self.__end) ^ \
               hash(self.__text)