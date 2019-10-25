import sys 
import random
import tkinter

class Agent(object):
    """docstring for Agent"""
    def __init__(self, x, y, energy):
        super(Agent, self).__init__()
        self.x = x 
        self.y = y
        self.energy = energy

    def remaining_energy(self):
        return self.energy
    
    
    def move(self, direction): 
        # Bouger vers le Nord 
        if direction == 0: 
            self.y = self.y - 1
        # Bouger vers l'Ouest
        elif direction == 1: 
            self.x = self.x - 1
        # Bouger vers le Sud
        elif direction == 2: 
            self.y = self.y + 1 
        # Bouger vers l'Est
        elif direction == 3: 
            self.x = self.x + 1

    def getPosition(self): 
        return (self.x, self.y)

    def setPosition(self, x,y): 
        self.x = x
        self.y = y