import sys 
import random
import tkinter
import dynamic_environment

#list des positions des patch dans le senseurs

#senseur de nourriture
#patches Y
Yfood=[(0,-10), (-2,-8), (2,-8), (-4, -6), (4,-6),(-6, -4), (6, -4), (-8,-2), (8,-2), (-10,0), (10, 0),(0,10), (-2,8), (2,8), (-4, 6), (4,6), (-6, 4), (6, 4), (-8,2), (8,2)]
#patches O
Ofood=[(0,-6), (-2,-4), (0,-4), (2,-4), (-4,-2), (-2,-2), (4,-2), (2,-2), (-6,0), (-4, 0), (4,0), (6,0), (0,6), (-2,4), (0,4), (2,4), (-4,2), (-2,2), (4,2), (2,2)]
#patches X
Xfood=[(0,-2), (-1,-1), (0,-1), (1,-1), (-2,0), (-1,0), (1,0), (2,0), (0,2), (-1,1), (0,1), (1,1)]

#senseur d'ennemies
#patches O
Oennemies=[(0,-6), (-2,-4), (0,-4), (2,-4), (-4,-2), (-2,-2), (4,-2), (2,-2), (-6,0), (-4, 0), (4,0), (6,0), (0,6), (-2,4), (0,4), (2,4), (-4,2), (-2,2), (4,2), (2,2)]
#patches X
Xennemies=[(0,-2), (-1,-1), (0,-1), (1,-1), (-2,0), (-1,0), (1,0), (2,0), (0,2), (-1,1), (0,1), (1,1)]

#senseur d'obstacle (patches o)
oobstacles=[(0,-4), (-1,-3), (0,-3), (1,-3), (-2,-2), (-1,-2), (0,-2), (1,-2), (2,-2), (-3,-1), (-2,-1), (-1,-1), (0,-1), (3,-1), (2,-1), (1,-1), (-4,0), (-3,0),(-2,0), (-1,0), (4,0), (3,0), (2,0), (1,0), (0,4), (-1,3), (0,3), (1,3), (-2,2), (-1,2), (0,2), (1,2), (2,2), (-3,1), (-2,1), (-1,1), (0,1), (3,1), (2,1), (1,1)]





class Agent(object):
    """docstring for Agent"""
    def __init__(self, x, y, energy):
        super(Agent, self).__init__()
        self.x = x 
        self.y = y
        self.energy = energy
        return
    

    def remaining_energy(self):
        return self.energy
    
    def setEnergy(self,value):
        self.energy += value
        
        if self.remaining_energy() < 0: 
            print("Game Over")
        
    def updateEnergy(self,canvas, energy_bar):
        energy = self.remaining_energy()
        print(energy)
        if energy%5 == 0: 
            canvas.delete(energy_bar[-1])
            energy_bar.pop()

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
            
    def sensors(self, state):
        #return the vector of detection
        result=[]
        (x,y)=state.agent.getPosition()

        #List for debug and see if the sensors are well-made 
        """positionSensorY = []
        positionSensorX = []
        positionSensorO = []
        positionSensoro = []"""

        #food
        for (i,j) in Yfood:
            result.append(state.Ypatch(x+i, y+j))
            #positionSensorY.append((x+i, y+j))
        for (i,j) in Ofood:
            result.append(state.Opatch(2, x+i, y+j))
            #positionSensorO.append((x+i, y+j))
        for (i,j) in Xfood:
            result.append(state.Xpatch(2, x+i, y+j))
            #positionSensorX.append((x+i, y+j))
        #ennemies
        for (i,j) in Oennemies:
            result.append(state.Opatch(1, x+i, y+j))
            #positionSensorO.append((x+i,y+j))
        for (i,j) in Xennemies:
            result.append(state.Xpatch(1, x+i, y+j))
            #positionSensorX.append((x+i,y+j))
        #obstacles
        for (i,j) in oobstacles:
            result.append(state.opatch(x+i, y+j))
        return result
        #return positionSensorY, positionSensorO, positionSensorX
            

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

        def debugSensor(self, state, type): 
             result=[]
        (x,y)=state.agent.getPosition()

        #List for debug and see if the sensors are well-made 
        positionSensorY = []
        positionSensorX = []
        positionSensorO = []
        positionSensoro = []

        if type ==2: 
            #food
            for (i,j) in Yfood:
                positionSensorY.append((x+i, y+j))
            for (i,j) in Ofood:
                positionSensorO.append((x+i, y+j))
            for (i,j) in Xfood:
                positionSensorX.append((x+i, y+j))
            return positionSensorY ,positionSensorO, positionSensorX
        #ennemies
        elif type == 1: 
            for (i,j) in Oennemies:
                positionSensorO.append((x+i,y+j))
            for (i,j) in Xennemies:
                positionSensorX.append((x+i,y+j))
            return positionSensorO,positionSensorO
        else :
            #obstacles
            for (i,j) in oobstacles:
                positionSensoro.append((x+i,y+j))
            return positionSensoro