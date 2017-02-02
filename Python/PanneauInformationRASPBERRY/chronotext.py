# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 21:02:41 2017

@author: yvan
"""

class ChronologicText:
    def __init__(self, begin, end, text):
        self.begin = begin
        self.end = end
        self.text = text
        
    def begin(self):
        return self.begin
        
    def end(self):
        return self.end
        
    def text(self):
        return self.text