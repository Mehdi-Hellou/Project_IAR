import sys 
import random
import tkinter
import dynamic_environment
import numpy as np

class Ennemy(object):
    """docstring for Ennemy"""
    def __init__(self, x, y, environment):
        super(Ennemy, self).__init__()
        self.y = y
        self.x = x

    def move(self, state, direction, ennemyText, pas, canvas):
        """
        direction : direction of the movement (Est,West,North,South)
        state : the environment of dynamic  
        """
        x,y = self.getPosition() 
        # Bouger vers le Nord 
        if direction == 3: 
            if state.lookupObstacles(x, y - 1)==False and state.lookupEnnemies(x, y - 1)==False and state.lookupFood(x, y-1)==False: 
                y = y - 1
                if (canvas != None) and (ennemyText != None) and (pas !=None): 
                    #print("North!!!")
                    canvas.move(ennemyText, 0, -pas)
        # Bouger vers l'Ouest
        elif direction == 2:
            if state.lookupObstacles(x - 1 ,y)==False and state.lookupEnnemies(x -1 , y)==False and state.lookupFood(x-1 , y)==False: 
                x = x - 1
                if (canvas != None) and (ennemyText != None) and (pas !=None):
                    #print("West!!!")
                    canvas.move(ennemyText, -pas, 0)            
        # Bouger vers le Sud
        elif direction == 1:
            if state.lookupObstacles(x,y + 1)==False and state.lookupEnnemies(x, y + 1)==False and state.lookupFood(x, y+1)==False:
                y = y + 1
                if (canvas != None) and (ennemyText != None) and (pas !=None): 
                    #print("South!!!")
                    canvas.move(ennemyText, 0, pas)
        # Bouger vers l'Est
        elif direction == 0:
            if state.lookupObstacles(x + 1,y)==False and state.lookupEnnemies(x+1, y )==False and state.lookupFood(x+1, y)==False:
                x = x + 1
                if (canvas != None) and (ennemyText != None) and (pas !=None): 
                    #print("East!!!")
                    canvas.move(ennemyText, pas, 0)
        
        return x,y

    def getPosition(self): 
        return (self.x, self.y)

    def setPosition(self, x,y): 
        self.x = x
        self.y = y
            
    def strategy(self, state, ennemyText = None, pas = None, canvas = None): 
        """
        The strategy of the ennemy for moving into the environnement 
        """
        x,y = self.getPosition()
        
        P = [0.0 for i in range(4)]

        for p in range(4): 
            xprime,yprime = self.move(state, p, None, None, None) # the potential ennemy position after have execute the move p

            if x==xprime and y==yprime:  # if the movement result in a collision with an obstacle 
                P[p] = 0.0
            else:                      
                P[p] = np.exp(0.33 * self.W_angle(p,state) * self.T_dist(state))  

        Pa = [i/np.sum(P) for i in P]  # the probability for each action possible

        move = np.argmax(Pa)    # we took the one with the best proba
        x,y = self.move(state, move, ennemyText, pas, canvas)
        self.setPosition(x,y)

        

    def W_angle(self, move,state):
        """
        The fonction for calculating the W angle. 
        Refer to the appendix A for more details.
        """
        xAgent, yAgent = state.agent.getPosition()

        x,y = self.getPosition()

        xafter, yafter = self.move(state, move, None, "", 0)

        u = np.array([xAgent-x, yAgent-y])
        v = np.array([xafter-x, yafter-y])

        angle = np.arccos((np.dot(u,v))/(np.linalg.norm(u)*np.linalg.norm(v)))

        angle = angle*180.0/np.pi

        return (180.0-abs(angle))/180.0 


    def T_dist(self,state):
        """
        The fonction for calculating the T dist. 
        Refer to the appendix A for more details. 
        """
        xAgent, yAgent = state.agent.getPosition()

        x,y = self.getPosition()

        dist =np.linalg.norm(np.array([xAgent-x, yAgent-y])) 

        if dist <= 4.0: 
            return 15.0 - dist 
        elif dist <= 15.0: 
            return 9.0 - dist/2
        else: 
            return 1.0