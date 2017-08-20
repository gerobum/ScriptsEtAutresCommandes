# -*- coding: utf-8 -*-
"""
Created on Mon Aug  14 21:02:41 2017

@author: yvan
"""
def cat(fileName):
    try:
        list = []
        with open(fileName) as fin:
            for c in fin:
                list.append(c)
        return ''.join(list)
    except Exception as e:
        return 'no file : ' + fileName 