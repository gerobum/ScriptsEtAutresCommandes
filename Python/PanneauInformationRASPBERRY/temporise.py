# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 10:25:57 2017

@author: yvan
"""

from datetime import datetime
import time
from dateutil.relativedelta import *
from threading import Thread

        
class Tempo:
    def __init__(self, date, go):
        self.go = go     
        self.duree = date - datetime.now()
        if self.duree.total_seconds() > 0:
            Thread(target=self.__waitandgo).start()

    def __waitandgo(self):
        time.sleep(self.duree.total_seconds())
        self.go()
            
            
    