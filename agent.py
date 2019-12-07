import sys 
import random
import tkinter
import dynamic_environment
import math
import numpy as np

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

def oriente(x,y,direction):
    if direction == 3:
        return (x,y)
    elif direction ==2:
        return (y,-x)
    elif direction == 1:
        return (-x,-y)
    elif direction ==0:
        return (-y, x)



class Agent(object):
    """docstring for Agent"""
    def __init__(self, x, y, energy):
        super(Agent, self).__init__()
        self.x = x 
        self.y = y
        self.energy = energy
        self.coarseEnergy = [1 for i in range(16)]   # the coarse coding of the energy for the Neural Network 
        self.previousAction = [0 for i in range(4)] # the 4 previous actions made by the agent 
        self.previous_collision = False # if the agent collide with an obstacle in the previous
        self.reward = 0.0
        return

    def remaining_energy(self):
        return self.energy
    
    def setEnergy(self,value, state=None):
        end = False
        if (self.energy + value) > 40: 
            self.energy = 40
        else :
            self.energy += value
        
        if self.remaining_energy() < 0: 
            self.energy = 0
            self.reward = -1.0
            end = True
        # We set the coarse coding of the agent's energy for the neural network
        len_now = int(self.energy//2.5) 
        self.coarseEnergy = [1 for i in range(len_now)] + [0 for i in range(16-len_now)]

        if end and state != None: # if the agent hasn't remained energy  
            state.dead = True
            state.end = True  # we restart the simulation
        print(self.coarseEnergy)
        return 

    def get_energy_coarsed(self): 
        return self.coarseEnergy

    def get_previousAction(self): 
        return self.previousAction

    def get_previous_collision(self): 
        return self.previous_collision
         
    def updateEnergy(self,canvas, energy_bar, getFood):
        """
        canvas : the canvas where the health bar is located 
        energy_bar : the list of eight rectangles which represented the energy level of the agent
        getFood :  boolean values ot indicate if the agent get the food or not during the current move
        """
        energy = self.remaining_energy()
        #print(energy)
        if (canvas!=None) and (energy_bar != None):
            if getFood:  # if the agent get the food
                length = math.ceil(energy/5)  # we took the lenght corresponding to the upper round of the energy bar divide by 5

                for i in range ( len(energy_bar), length): 
                    x_index = i * 25 + 1
                    energy_bar.append(canvas.create_rectangle(x_index, 0, x_index + 25, 25, fill="red", width = 0.5))

            elif energy%5 == 0: 
                canvas.delete(energy_bar[-1])
                energy_bar.pop()

    def move(self, direction,state=None,canvas=None, agentText=None, pas=None): 
        x,y = self.getPosition()
        # Bouger vers le Nord 
        if direction == 3: 
            if state.lookupObstacles(x, y-1)==False:
                y = y - 1
                if (canvas !=None) and (agentText != None) and (pas != None):
                    canvas.move(agentText, 0, -pas)
                self.previous_collision = False
            else:
                self.previous_collision = True

            #print("Nord !")
        # Bouger vers l'Ouest
        elif direction == 2: 
            if state.lookupObstacles(x - 1 ,y)==False:
                x = x - 1
                if (canvas !=None) and (agentText != None) and (pas != None):
                    canvas.move(agentText, -pas, 0)
                self.previous_collision = False
            else:
                self.previous_collision = True

            #print("Ouest !")
        # Bouger vers le Sud
        elif direction == 1: 
            if state.lookupObstacles(x , y + 1)==False:
                y = y + 1
                if (canvas !=None) and (agentText != None) and (pas != None):
                    canvas.move(agentText, 0, pas)
                self.previous_collision = False
            else:
                self.previous_collision = True

            #print("Sud !") 
        # Bouger vers l'Est
        elif direction == 0: 
            if state.lookupObstacles(x + 1 ,y)==False:
                x = x + 1
                if (canvas !=None) and (agentText != None) and (pas != None):
                    canvas.move(agentText, pas, 0)
                self.previous_collision = False
            else:
                self.previous_collision = True

            #print("Est !")

        return x,y

    def move_simulated(self,state,direction): 
        """
        move for the simulation when we are at the step of learning
        environment : the environment where the agent move which could be 
                      the self environment, or the one after a rotation (90,180,270)   
        direction = the direction of the movement 
        """
        # Toujours l'agent bouge vers le Nord
        # car l'utilité est calculée en fonction du mérite de bouger vers le nord
        # suivant les différentes configurations des ennemies   
        
        x,y = self.getPosition()

        # Bouger vers le Nord 
        if direction == 3: 
            if state.lookupObstacles(x, y-1)==False:
                y = y - 1
        # Bouger vers l'Ouest
        elif direction == 2: 
            if state.lookupObstacles(x - 1 ,y)==False:
                x = x - 1
        elif direction == 1: 
            if state.lookupObstacles(x , y + 1)==False:
                y = y + 1
        # Bouger vers l'Est
        elif direction == 0: 
            if state.lookupObstacles(x + 1 ,y)==False:
                x = x + 1

        return x,y

    def getPosition(self): 
        return (self.x, self.y)

    def setPosition(self, x,y): 
        self.x = x
        self.y = y
            
    def sensors(self, state, x = None, y = None, environment = None, positionEnnemies = None, direction = 3):
        #return the vector of detection
        #pour les directions: 3= nord, 2=ouest, 1=sud, 0 = est
        result=[]
        
        if x == None and y == None: 
            (x,y)=state.agent.getPosition()

        else:
            (x0,y0) = self.getPosition()
            (x,y)=(x0+x,y0+y)

        #food
        for (i0,j0) in Yfood:
            (i,j) = oriente(i0,j0, direction)
            result.append(state.Ypatch(x+i, y+j, environment, positionEnnemies))
            #positionSensorY.append((x+i, y+j))
        for (i0,j0) in Ofood: 
            (i,j) = oriente(i0,j0, direction)
            result.append(state.Opatch(2, x+i, y+j,environment, positionEnnemies))
            #positionSensorO.append((x+i, y+j,environment))
        for (i0,j0) in Xfood:
            (i,j) = oriente(i0,j0, direction)
            result.append(state.Xpatch(2, x+i, y+j,environment, positionEnnemies))
            #positionSensorX.append((x+i, y+j,environment))
        #ennemies
        for (i0,j0) in Oennemies:
            (i,j) = oriente(i0,j0, direction)
            result.append(state.Opatch(1, x+i, y+j,environment, positionEnnemies))
            #positionSensorO.append((x+i,y+j,environment))
        for (i0,j0) in Xennemies:
            (i,j) = oriente(i0,j0, direction)
            result.append(state.Xpatch(1, x+i, y+j,environment, positionEnnemies))
            #positionSensorX.append((x+i,y+j,environment))
        #obstacles
        for (i0,j0) in oobstacles:
            (i,j) = oriente(i0,j0, direction)
            result.append(state.opatch(x+i, y+j,environment, positionEnnemies))

        return result
        #return positionSensorY, positionSensorO, positionSensorX

    def sensors_without_rot(self, state, direction=3):
        #return the vector of detection
        #pour les directions: 3= nord, 2=ouest, 1=sud, 0 = est
        result=[]
        
        (x,y) = self.move_simulated(state,direction)
        #food
        for (i,j) in Yfood:
            result.append(state.Ypatch(x+i, y+j))
            #positionSensorY.append((x+i, y+j))
        for (i,j) in Ofood: 
            result.append(state.Opatch(2, x+i, y+j))
            #positionSensorO.append((x+i, y+j,environment))
        for (i,j) in Xfood:
            result.append(state.Xpatch(2, x+i, y+j))
            #positionSensorX.append((x+i, y+j,environment))
        #ennemies
        for (i,j) in Oennemies:
            result.append(state.Opatch(1, x+i, y+j))
            #positionSensorO.append((x+i,y+j,environment))
        for (i,j) in Xennemies:
            result.append(state.Xpatch(1, x+i, y+j))
            #positionSensorX.append((x+i,y+j,environment))
        #obstacles
        for (i,j) in oobstacles:
            result.append(state.opatch(x+i, y+j))

        return result
    
    
            
    def policy(self, state, agentText, pas, canvas = None):
        """
        The policy of the agentgiven the current neural network, the best utility 
        for the different action it can performed and its current state. 
        """
        l_actions = state.learning_Utility()   # learning step of the agent to get the list of proba values for each action
        #print(l_actions)
        action = np.argmax(l_actions)
        x,y = self.move(action,state, canvas,agentText, pas)  # we make move the agent according the best action possible 
        self.setPosition(x,y)  
      
        self.previousAction.pop(0) # we remove the first element of the list since we only record the 4 previous actions 
        self.previousAction.append(action)  # we add the new direction to the list of previous ones 

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