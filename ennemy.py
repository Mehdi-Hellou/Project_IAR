import sys 
import random
import tkinter
import dynamic_environment
import numpy as np

class Ennemy(object):
    """docstring for Ennemy"""
    def __init__(self, x, y, energy):
        super(Ennemy, self).__init__()
        self.y = y
        self.energy = energy
        return

    def move(self, direction, state):
        x,y = self.getPosition() 
        # Bouger vers le Nord 
        if direction == 0: 
            if !state.lookupObstacles(x,y): 
                y = y - 1
            
        # Bouger vers l'Ouest
        elif direction == 1:
            if !state.lookupObstacles(x,y): 
                x = x - 1 
            
        # Bouger vers le Sud
        elif direction == 2: 
            if !state.lookupObstacles(x,y):
                y = y + 1
        # Bouger vers l'Est
        elif direction == 3: 
            if !state.lookupObstacles(x,y):
                x = x + 1
        return x,y

    def getPosition(self): 
        return (self.x, self.y)

    def setPosition(self, x,y): 
        self.x = x
        self.y = y
            
    def strategy(self, state): 
        """
        The strategy of the ennemy for moving into the environnement 
        """
        
        x,y = self.getPosition()

        P = [0.0 for i in range(4)]

        for p in range(4): 
            xprime,yprime = self.move(p,state)

            if x==xprime and y==yprime: 
                P[p] = 0.0
            else:
                P[p] = np.exp(0.33 * W_angle(state,p) * T_dist())
        

    def W_angle(self,state, move):
        xAgent, yAgent = state.agent.getPosition()

        x,y = self.getPosition()

        xafter, yafter = self.move(move,state)

        u = np.array(xAgent-x, yAgent-y)
        v = np.array(xafter-x, yafter-y)

        angle = np.arccos((np.dot(u,v))/(np.linalg.norm(u)*np.linalg.norm(v)))

        angle = angle*180.0/np.pi

        return (180.0-abs(angle))/180.0 


    def T_dist(self): 
        xAgent, yAgent = state.agent.getPosition()

        x,y = self.getPosition()

        dist =np.linalg.norm(np.array(xAgent-x, yAgent-y)) 

        if dist <= 4.0: 
            return 15.0 - dist 
        elif dist <= 15.0: 
            return 9.0 - dist/2
        else: 
            return 1.0