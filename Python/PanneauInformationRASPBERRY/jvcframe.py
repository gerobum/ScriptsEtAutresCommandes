# -*- encoding: utf-8 -*-
"""
Lecture mail

Created on Sat Jan 21 17:28:43 2017

@author: yvan
"""

from Tkinter import Label, Tk, PhotoImage

class JVCFrame(Tk):
    def __init__(self):
        Tk.__init__(self) 
        
        self.config(bg='black')
        self.title('Bonjour Maman')
        self.attributes('-fullscreen', True)
        
        #photo = PhotoImage(file="JVC.png")
        #self.label = Label(self, image=photo)
        #self.label.pack(fill='both', pady=1)
        #self.label.photo = photo 
  
    
    def the_end(self):
        self.destroy()


  