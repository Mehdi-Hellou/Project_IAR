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
            print("Nord !")
        # Bouger vers l'Ouest
        elif direction == 1: 
            self.x = self.x - 1
            print("Ouest !")
        # Bouger vers le Sud
        elif direction == 2: 
            self.y = self.y + 1
            print("Sud !") 
        # Bouger vers l'Est
        elif direction == 3: 
            self.x = self.x + 1
            print("Est !")

    def getPosition(self): 
        return (self.x, self.y)

    def setPosition(self, x,y): 
        self.x = x
        self.y = y

    def sensorObstacle(self,state): 
        positionObstacle = []   # List of position of obstacle in function of position of agent 

        k = 4
        for i in range(5) : 

            for j in reversed(range(k+1)): 
                
                if j==0: # prevent to add twice the same value  
                    if state.opatch(self.x, self.y + i):
                        positionObstacle.append((self.x, self.y + i))

                    if state.opatch(self.x, self.y - i): 
                        positionObstacle.append((self.x, self.y - i))

                else:
                    #The obstacles in bottom left part of the sensor 
                    if state.opatch(self.x-j, self.y + i): 
                        positionObstacle.append((self.x-j, self.y + i))
                    #The obstacles in bottom right part of the sensor 
                    if state.opatch(self.x+j, self.y + i):
                        positionObstacle.append((self.x+j, self.y + i))
                    #The obstacles in up left part of the sensor 
                    if state.opatch(self.x-j,self.y-i): 
                        positionObstacle.append((self.x-j,self.y-i))
                    #The obstacles in up right part of the sensor
                    if state.opatch(self.x+j,self.y-i): 
                        positionObstacle.append((self.x+j,self.y-i))

            k-=1

        return positionObstacle