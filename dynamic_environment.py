import sys 
import os
import random
import tkinter
import agent as agt
import threading 
from ennemy import Ennemy
from neural_network import *

random.seed()

#dimension de la grille
width = 25
heigth = 25

#poisiton des obstacles 
obstacles = [] 
obstacles+= [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24)]
obstacles+=[(1,0), (1,24)]
obstacles+=[(2,0),(2,3),(2,4), (2,8), (2,9), (2,11), (2,12), (2,13), (2,15), (2,16), (2,20), (2,21), (2,24)]
obstacles+=[(3,0), (3,2), (3,3), (3,4), (3,8), (3,9), (3,11), (3,13), (3,15), (3,16), (3,20), (3,21), (3,22), (3,24)]
obstacles+=[(4,0), (4,2), (4,3), (4,4), (4,20), (4,21), (4,22), (4,24)]
obstacles+=[(5,0),(5,24)]
obstacles+=[(8,2),(8,3), (8,8), (8,9), (8,10), (8,11), (8,13), (8,14), (8,15), (8,16), (8,21), (8,22)]
obstacles+=[(9,2),(9,3), (9,8), (9,9), (9,10), (9,14), (9,15), (9,16), (9,21), (9,22)]
obstacles+=[(10,8), (10,9), (10,15), (10,16)]
obstacles+=[(11,2),(11,3), (11,8), (11,16), (11,21), (11,22)]
obstacles+=[(12,3), (12,12), (12,22)]
obstacles+= [(24,0), (24,1), (24,2), (24,3), (24,4), (24,5), (24,19), (24,20), (24,21), (24,22), (24,23), (24,24)]
obstacles+=[(23,0), (23,24)]
obstacles+=[(22,0),(22,3),(22,4), (22,8), (22,9), (22,11), (22,12), (22,13), (22,15), (22,16), (22,20), (22,21), (22,24)]
obstacles+=[(21,0), (21,2), (21,3), (21,4), (21,8), (21,9), (21,11), (21,13), (21,15), (21,16), (21,20), (21,21), (21,22), (21,24)]
obstacles+=[(20,0), (20,2), (20,3), (20,4), (20,20), (20,21), (20,22), (20,24)]
obstacles+=[(19,0),(19,24)]
obstacles+=[(16,2),(16,3), (16,8), (16,9), (16,10), (16,11), (16,13), (16,14), (16,15), (16,16), (16,21), (16,22)]
obstacles+=[(15,2),(15,3), (15,8), (15,9), (15,10), (15,14), (15,15), (15,16), (15,21), (15,22)]
obstacles+=[(14,8), (14,9), (14,15), (14,16)]
obstacles+=[(13,2),(13,3), (13,8), (13,16), (13,21), (13,22)]

step_training = 0
###################################################################### Class State ######################################################################
"""
The main class to train and test the agent into the simulator 
"""
class State:
    def __init__(self, obstacles, nn, display = False):
        self.environment = [[ 0 for j in range(25)] for i in range(25)]
        #0=empty, 1=obstacle, 2= food (ennemy and agent stored separetely)
        for (x,y) in obstacles:
            self.environment[x][y] = 1
        self.ennemies = [Ennemy(6,6,self), Ennemy(12,2,self), Ennemy(12,6,self), Ennemy(18,6,self)]        
        self.agent = agt.Agent(13,18, 40)
        
        for i in range(15):
            x = random.randint(0,24)
            y = random.randint(0,24)
            while not self.is_empty(x,y):
                x = random.randint(0,24)
                y = random.randint(0,24)
            self.environment[x][y] =2

        self.energy=40

        self.end = False 
        self.nn = nn  # the neural network used for the learning 
        self.gamma = 0.95  # the parameters for the learning
        self.Temp = 1/40 # The temperature for the stochastic action selector 
        self.Ulist = []  # list of Utility for all the actions at each state use for the learning  
        self.totalFood = 0 #food eaten during the simulation
        self.grille = None
        self.can = None
        self.agentText = None
        self.PAS=None
        self.can_life = None
        self.life = None
        self.ennemyText=None
        self.display = display
        if self.display:
            self.initiate_simulation()
        
    
    def is_empty(self,x,y,agentInit=True):

        if agentInit: 
            return (self.environment[x][y]==0) and ((x,y)!= self.agent.getPosition()) and not((x,y) in [i.getPosition() for i in self.ennemies]) and self.environment[x][y]!=1
        else: 
            return (self.environment[x][y]==0) and not((x,y) in [i.getPosition() for i in self.ennemies]) and self.environment[x][y]!=1

    def remaining_energy(self):
        return self.agent.remaining_energy()
    
    #------------- fonction pour tester une case
    
    def lookupObstacles(self, x, y,environment=None):
        if x<0 or x>=width or y<0 or y>=heigth:
            return True
        
        if environment != None and environment[x][y]==1:
            return True
        elif self.environment[x][y]==1:
            #print("obstacles !!! ")
            return True
        else:
            return False
    
    def lookupFood(self, x, y,environment=None):
        if x<0 or x>=width or y<0 or y>=heigth:
            return False

        if environment != None and environment[x][y]==2:
            return True
        elif self.environment[x][y]==2:
            #print("food !!! ")
            return True
        else:
            return False
    
    def lookupEnnemies(self, x, y,environment=None, positionEnnemies =  None):
        """
        positionEnnemies : position of ennemy of the environment has just been rotated
        """
        if positionEnnemies == None: 
            positionEnnemies = [i.getPosition() for i in self.ennemies]

        if x<0 or x>=width or y<0 or y>=heigth:
            return False
        if (x,y) in positionEnnemies:
            #print("An ennemiy !!! ")
            return True
        else:
            return False
    
    def lookUpSensor(self, lookup, x, y, environment=None, positionEnnemies=None):
        #  if 2 we use the sensor to detect the food 
        if lookup == 2:   
            return self.lookupFood(x,y, environment)
        #  if 1 we use the sensor to detect the ennemies 
        elif lookup == 1:           
            return self.lookupEnnemies(x,y, environment, positionEnnemies)
        #  else we use the sensor to detect the obstacles
        else: 
            return self.lookupObstacles(x,y, environment)

    #---------------fonction de patch d'observation-------------
    
    def opatch(self, x, y,environment=None, positionEnnemies=None):
        return self.lookUpSensor(0, x,y,environment, positionEnnemies)
    
    def Xpatch(self, lookup, x, y,environment=None,positionEnnemies=None):
        # lookup could be 2 to detect the food or 1 to detect the ennemies  
        return self.lookUpSensor(lookup, x,y,environment,positionEnnemies) or self.lookUpSensor(lookup, x-1,y,environment,positionEnnemies)\
        or self.lookUpSensor(lookup, x+1,y,environment,positionEnnemies) or self.lookUpSensor(lookup, x,y-1,environment,positionEnnemies)\
        or self.lookUpSensor(lookup, x,y+1,environment,positionEnnemies)
    
    def Opatch(self, lookup, x, y,environment=None,positionEnnemies=None):
        # lookup could be 2 to detect the food or 1 to detect the ennemies
        return self.Xpatch(lookup,x,y,environment) or self.lookUpSensor(lookup, x-1,y-1,environment,positionEnnemies)\
        or self.lookUpSensor(lookup, x-1,y+1,environment,positionEnnemies) or self.lookUpSensor(lookup, x+1,y-1,environment,positionEnnemies)\
        or self.lookUpSensor(lookup, x+1,y+1,environment,positionEnnemies)
    
    def Ypatch(self, x, y,environment=None,positionEnnemies=None):
        return self.Opatch(2,x,y,environment) or self.lookUpSensor(2, x-2,y,environment,positionEnnemies) or self.lookUpSensor(2, x+2,y,environment,positionEnnemies)\
         or self.lookUpSensor(2, x,y-2,environment,positionEnnemies) or self.lookUpSensor(2, x,y+2,environment,positionEnnemies)
    
    #-------------- fonctions d'affichage (a garder en bas)------------------
    
    def print_grid(self):
        #to_print=tkinter.Tk()
        
        for i in range(25):
            for j in range(25):         
                case = tkinter.Canvas(to_print, height=25, width=25,  bg="white").grid(row=i, column=j)       
                if (i,j) in [i.getPosition() for i in self.ennemies]:
                    l = tkinter.Label(case, text = "E", borderwidth=1, fg='blue', bg="white").grid(row=i, column=j)
                elif (i,j)==self.agent.getPosition():
                    l = tkinter.Label(case, text = "I", borderwidth=1, fg='red', bg="white").grid(row=i, column=j)
                elif self.environment[i][j]==2:
                    l = tkinter.Label(case, text = "$", borderwidth=1, fg='green', bg="white").grid(row=i, column=j)
                elif self.environment[i][j] == 1:
                    l= tkinter.Label(case, text="O", borderwidth=1, fg='black', bg="white").grid(row=i, column=j)
                else:
                    l= tkinter.Label(case, text="", borderwidth=1, fg='black', bg="white").grid(row=i, column=j)

        #to_print.mainloop()

    def print_grid_line(self):
        windows_Size=800
        self.grille = tkinter.Tk()
        self.can=tkinter.Canvas(self.grille,bg="light gray", height=windows_Size, width=windows_Size)
        self.can.pack()

        self.PAS = int(windows_Size/width)   # Pas en fonction de la taille de la fenetre ainsi que la taille de notre grillage dans la simulation 

        X0 = Y0 = int(self.PAS/2)           # coordonner pour centrer le texte au milieu de chaque case 
        
        self.ennemyText = []
        self.foodText = {}
        for i in range(25): 
            self.can.create_line(0,self.PAS*i,windows_Size,self.PAS*i,fill='black')      # on cree manuellement des lignes horizontales  
            self.can.create_line(self.PAS*i , 0,self.PAS*i,windows_Size,fill='black')    # on cree manuellement des lignes verticales 

            for j in range(25):         
                centre = (X0+i*self.PAS, Y0+j*self.PAS) 

                if (i,j)==self.agent.getPosition():
                    self.agentText = self.can.create_text(centre, text = "I")
                
                elif (i,j) in [i.getPosition() for i in self.ennemies]:
                    self.ennemyText.append(self.can.create_text(centre, text = "E"))
                
                elif self.environment[i][j]==2:
                    self.foodText[(i,j)] = self.can.create_text(centre, text = "$")

                elif self.environment[i][j] == 1:
                    self.can.create_text(centre, text = "O") 
        
        #create the HP bar in the bottom
        self.life = []  # all rectangle for the life 

        self.can_life=tkinter.Canvas(self.grille,bg="light gray",height=25, width=200)
        self.can_life.pack(side = "left") 

        for i in range(1,200,25): 
            self.life.append(self.can_life.create_rectangle( i, 0, i+25, 25, fill="red", width = 0.5))      
            
    def print_sensors(self, target): #fonction affichant la position (et les activations) des patch
        #target: 0=obstacles, 1= ennemies, 2 =food
        windows_Size=800
        self.grille = tkinter.Tk()
        self.can=tkinter.Canvas(self.grille,bg="light gray", height=windows_Size, width=windows_Size)
        self.can.pack()

        self.PAS = int(windows_Size/width)   # Pas en fonction de la taille de la fenetre ainsi que la taille de notre grillage dans la simulation 

        X0 = Y0 = int(self.PAS/2)           # coordonner pour centrer le texte au milieu de chaque case 
        
        self.ennemyText = []
        self.foodText = {}
        (a,b) = self.agent.getPosition()
        if target ==2:
            YFoodPatch = [(a+x,b+y) for (x,y) in agt.Yfood]
            OFoodPatch = [(a+x,b+y) for (x,y) in agt.Ofood]
            XFoodPatch = [(a+x,b+y) for (x,y) in agt.Xfood]
            allFoodPatch = YFoodPatch + OFoodPatch + XFoodPatch
        if target ==1:
            OEnnemyPatch = [(a+x,b+y) for (x,y) in agt.Oennemies]
            XEnnemyPatch = [(a+x,b+y) for (x,y) in agt.Xennemies]
            allEnnemyPatch = OEnnemyPatch + XEnnemyPatch
        if target==0:
            ObstaclesPatch = [(a+x,b+y) for (x,y) in agt.oobstacles]
        for i in range(25): 
            self.can.create_line(0,self.PAS*i,windows_Size,self.PAS*i,fill='black')      # on cree manuellement des lignes horizontales  
            self.can.create_line(self.PAS*i , 0,self.PAS*i,windows_Size,fill='black')    # on cree manuellement des lignes verticales 

            for j in range(25):         
                centre = (X0+i*self.PAS, Y0+j*self.PAS)
                if target ==2:
                    if (i,j)==self.agent.getPosition():
                        self.agentText = self.can.create_text(centre, text = "I")
                    elif (i,j) in YFoodPatch:
                        b = self.Ypatch(i,j)
                        if self.environment[i][j]==2 and b:
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "$", fill='red')
                        elif self.environment[i][j]==2 and not(b):
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "Y", fill='blue')
                        elif self.environment[i][j]!=2 and b:
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "Y", fill='red')
                        elif self.environment[i][j]!=2 and not(b):
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "Y", fill='black')
                    elif (i,j) in OFoodPatch:
                        b = self.Opatch(2,i,j)
                        if self.environment[i][j]==2 and b:
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "$", fill='red')
                        elif self.environment[i][j]==2 and not(b):
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "O", fill='blue')
                        elif self.environment[i][j]!=2 and b:
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "O", fill='red')
                        elif self.environment[i][j]!=2 and not(b):
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "O", fill='black')
                    elif (i,j) in XFoodPatch:
                        b = self.Xpatch(2,i,j)
                        if self.environment[i][j]==2 and b:
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "$", fill='red')
                        elif self.environment[i][j]==2 and not(b):
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "X", fill='blue')
                        elif self.environment[i][j]!=2 and b:
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "X", fill='red')
                        elif self.environment[i][j]!=2 and not(b):
                            self.foodText[(i,j)] = self.can.create_text(centre, text = "X", fill='black')
                    elif self.environment[i][j]==2 and not ((i,j) in allFoodPatch) :
                        self.foodText[(i,j)] = self.can.create_text(centre, text = "$")
                        
                if target == 1:
                    if (i,j)==self.agent.getPosition():
                        self.agentText = self.can.create_text(centre, text = "I")
                    elif (i,j) in OEnnemyPatch:
                        b = self.Opatch(1,i,j)
                        if (i,j) in [i.getPosition() for i in self.ennemies] and b:
                            self.ennemyText.append(self.can.create_text(centre, text = "E", fill = 'red'))
                        elif (i,j) in [i.getPosition() for i in self.ennemies] and not(b):
                            self.ennemyText.append(self.can.create_text(centre, text = "O", fill = 'blue'))
                        elif not((i,j) in [i.getPosition() for i in self.ennemies]) and b:
                            self.ennemyText.append(self.can.create_text(centre, text = "O", fill = 'red'))
                        elif not((i,j) in [i.getPosition() for i in self.ennemies]) and not(b):
                            self.ennemyText.append(self.can.create_text(centre, text = "O", fill = 'black'))
                    elif (i,j) in XEnnemyPatch:
                        b = self.Xpatch(1,i,j)
                        if (i,j) in [i.getPosition() for i in self.ennemies] and b:
                            self.ennemyText.append(self.can.create_text(centre, text = "E", fill = 'red'))
                        elif (i,j) in [i.getPosition() for i in self.ennemies] and not(b):
                            self.ennemyText.append(self.can.create_text(centre, text = "X", fill = 'blue'))
                        elif not((i,j) in [i.getPosition() for i in self.ennemies]) and b:
                            self.ennemyText.append(self.can.create_text(centre, text = "X", fill = 'red'))
                        elif not((i,j) in [i.getPosition() for i in self.ennemies]) and not(b):
                            self.ennemyText.append(self.can.create_text(centre, text = "X", fill = 'black'))
                    elif ((i,j) in [i.getPosition() for i in self.ennemies]) and not ((i,j) in allEnnemyPatch) :
                        self.ennemyText.append(self.can.create_text(centre, text = "E"))
                if target ==0:
                    if (i,j)==self.agent.getPosition():
                        self.agentText = self.can.create_text(centre, text = "I")
                    elif (i,j) in ObstaclesPatch:
                        b = self.opatch(i,j)
                        if self.environment[i][j]==1 and b:
                            self.can.create_text(centre, text = "O", fill='red')
                        elif self.environment[i][j]==1 and not(b):
                            self.can.create_text(centre, text = "o", fill = 'blue')
                        elif self.environment[i][j]!=1 and b:
                            self.can.create_text(centre, text = "o", fill = 'red')
                        elif self.environment[i][j]!=1 and not(b):
                            self.can.create_text(centre, text = "o", fill = 'black')
                    elif self.environment[i][j] == 1:
                        self.can.create_text(centre, text = "O") 

        
        #create the HP bar in the bottom
        self.life = []  # all rectangle for the life 

        self.can_life=tkinter.Canvas(self.grille,bg="light gray",height=25, width=200)
        self.can_life.pack(side = "left") 

        for i in range(1,200,25): 
            self.life.append(self.can_life.create_rectangle( i, 0, i+25, 25, fill="red", width = 0.5))  

    def deleteFood(self,x,y): 
        """
        Delete the food from the simulator
        """     
        self.environment[x][y] = 0      # the value of the case change 
        if self.display:
            self.can.delete(self.foodText[(x,y)])  # delete the food text from the simulators 
                        
    def moveAgent(self, learning = False):
          
        getFood = False # boolean to know if the move of agent allowed him to get food or not 

        if not(self.end): ## if the move an ennemy has collided with the agent in the previous loop, he can't move
            self.agent.policy(self, self.agentText, self.PAS, self.can)  # perform the policy of the agent 
        
        x,y = self.agent.getPosition()
            
        if self.lookupEnnemies(x,y): # if the movement of the agent is on an ennemie's position it is the end of the simulation
            print("Catch by the ennemies !!!")
            self.agent.reward = -1.0
            self.end = True

        elif self.lookupFood(x,y):
            self.agent.reward = 0.4            
            self.agent.setEnergy(15)
            self.deleteFood(x,y)  # delete the food from the environment
            self.totalFood+=1
            if self.totalFood==15:
                self.end=True
            getFood = True
            self.agent.updateEnergy(self.can_life,self.life, getFood)  # Update the canvas that displays the level of the health of the agent
        
        else: 
            self.agent.reward = 0.0
            self.agent.setEnergy(-1, self)
            if self.agent.remaining_energy()>0:
                self.agent.updateEnergy(self.can_life,self.life, getFood)   
        
        if learning:
            self.backpropagating()        

        if self.display:
            if self.end:
                self.restart_simulation()
            self.grille.after(3000, lambda: self.moveAgent(learning))    # Resubscribe to make move again the agent each second

            

    def moveEnnemy(self):
        """
        Function to make move the ennemies
        """
        for i,ennemy in enumerate(self.ennemies):

            r = random.uniform(0,1)
            if r > 0.2 : 
                if (self.ennemyText != None) and (self.PAS !=None) and (self.can!=None):
                    ennemy.strategy(self.ennemyText[i], self.PAS, self.can)
                else:
                    ennemy.strategy()
                
                if self.agent.getPosition() == ennemy.getPosition(): # if the movement of the ennemy is in the agent's position it is the end of the simulation
                    self.end = True

        if self.display and not(self.end):# if it's not the end we make move again the ennemies 
            self.grille.after(3000, self.moveEnnemy)  # Resubscribe to make move again the ennemy each 1.2 seconds

    def initiate_simulation(self): 
        self.print_grid_line() 
        self.moveEnnemy()
        self.moveAgent(learning=True)
        self.grille.mainloop() 

    def restart_simulation(self):
        self.grille.destroy() 

    def learning_Utility(self): 
        """
        Return the action that maximize the utility and the utiliy given by performing this action
        """
        # Shape the input that we give to the neural network with the value of sensors, the previous actions the life of the agent 
        input_nn = np.asarray(self.agent.get_energy_coarsed() + self.agent.get_previousAction() + [int(self.agent.get_previous_collision())]) 

        # Get the results from the sensors according the different movement executed by the agent 
        sensors_result_N = np.asarray(self.agent.sensors(self, x = 0, y = -1, direction=3)).astype(int)
        sensors_result_O = np.asarray(self.agent.sensors(self, x = 0, y = -1, direction=2)).astype(int)
        #np.asarray(self.rotationEnvironment(270)).astype(int)
        sensors_result_S = np.asarray(self.agent.sensors(self, x = 0, y = -1, direction=1)).astype(int)
        #np.asarray(self.rotationEnvironment(180)).astype(int)
        sensors_result_E = np.asarray(self.agent.sensors(self, x = 0, y = -1, direction=0)).astype(int)
        #np.asarray(self.rotationEnvironment(90)).astype(int)

        input_nn_N = np.concatenate((sensors_result_N,input_nn))    # input when the Nord action is performed 
        input_nn_O = np.concatenate((sensors_result_O,input_nn))    # input when the West action is performed
        input_nn_S = np.concatenate((sensors_result_S,input_nn))    # input when the South action is performed
        input_nn_E = np.concatenate((sensors_result_E,input_nn))    # input when the West action is performed

        U_list = [self.nn.predict(input_nn_E.reshape(1,145))*self.gamma + self.getRewardAgent(direction = 0),\
                  self.nn.predict(input_nn_S.reshape(1,145))*self.gamma + self.getRewardAgent(direction = 1),\
                  self.nn.predict(input_nn_O.reshape(1,145))*self.gamma + self.getRewardAgent(direction = 2),\
                  self.nn.predict(input_nn_N.reshape(1,145))*self.gamma + self.getRewardAgent(direction = 3)]
                  
        print("The reward is %f" %(self.agent.reward))
        self.U_list = [U_list[i]*self.gamma + self.agent.reward for i in range(4) ] #The utility according the different acts performed    
        return self.actionSelector()    #Select the action acording a propbabilitics distribution given in the paper

    def backpropagating(self): 
        """
        Backpropagate the errors delta U given the previous utility Umax computed during the first step
        and the Utility max given the current state and the different action performed   
        """ 

        ######################### Configure the sensor inputs given the movement of the agent ######################### 
        input_nn = np.asarray(self.agent.get_energy_coarsed() + self.agent.get_previousAction() + [int(self.agent.get_previous_collision())]) 
        #print(self.agent.get_previousAction())
        sensors_result_N = np.asarray(self.agent.sensors(self, x = 0, y = -1, direction=3)).astype(int)
        sensors_result_O =np.asarray(self.agent.sensors(self, x = 0, y = -1, direction=2)).astype(int) 
        #np.asarray(self.rotationEnvironment(270)).astype(int)
        sensors_result_S = np.asarray(self.agent.sensors(self, x = 0, y = -1, direction=1)).astype(int) 
        #np.asarray(self.rotationEnvironment(180)).astype(int)
        sensors_result_E = np.asarray(self.agent.sensors(self, x = 0, y = -1, direction=0)).astype(int) 
        #np.asarray(self.rotationEnvironment(90)).astype(int)

        input_nn_N = np.concatenate((sensors_result_N,input_nn))    # input when the Nord action is performed 
        input_nn_O = np.concatenate((sensors_result_O,input_nn))    # input when the West action is performed
        input_nn_S = np.concatenate((sensors_result_S,input_nn))    # input when the South action is performed
        input_nn_E = np.concatenate((sensors_result_E,input_nn))    # input when the West action is performed

        l_input = [input_nn_E.reshape(1,145),input_nn_S.reshape(1,145),input_nn_O.reshape(1,145),input_nn_N.reshape(1,145)]
        ######################### Configure the sensor inputs given the movement of the agent #########################

        print("The reward in baskpropagating is %f" %(self.agent.reward) ) 
        parameters = [self.gamma, self.agent.reward]

        U_list_y = [self.nn.predict(input_nn_E.reshape(1,145))*self.gamma + self.getRewardAgent(direction = 0),\
                  self.nn.predict(input_nn_S.reshape(1,145))*self.gamma + self.getRewardAgent(direction = 1),\
                  self.nn.predict(input_nn_O.reshape(1,145))*self.gamma + self.getRewardAgent(direction = 2),\
                  self.nn.predict(input_nn_N.reshape(1,145))*self.gamma + self.getRewardAgent(direction = 3)]

        index_input_maxU = np.argmax(U_list_y)   # the input given for the backprogating is the one with the maximum utility

        Ui = self.U_list[self.agent.get_previousAction()[-1]]

        parameters.append(self.getRewardAgent(direction = index_input_maxU))   # reward related to the state with the best utility
        input_nn = l_input[index_input_maxU].reshape(1,145)    # input of the utility with the best value
        self.nn._train_one_step(input_nn,Ui,parameters)

    def getRewardAgent(self,direction = None): 
        """
        get the reward from the currnet position of the agent 
        or from the simulated position of the agent after a movement
        """
        if direction == None:
            x,y = self.agent.getPosition()
        else: 
            x,y = self.agent.move_simulated(self,direction)
        
        if self.lookupEnnemies(x,y): # if the movement of the agent is on an ennemie's position it is the end of the simulation
            reward = -1.0        
        elif self.lookupFood(x,y):            
            reward = 0.4        
        else: 
            reward = 0.0

        return reward
    
    def rotationEnvironment(self, angle): 
        """
        Rotate the environment to establich the values of sensors according the rotation of the environment
        angle : 90, 180 and 270 degrees rotation
        """
        x_agent, y_agent = self.agent.getPosition()
        positionEnnemies = [i.getPosition() for i in self.ennemies]

        env_move_E = np.rot90(np.asarray(self.environment)).tolist()   # when we make a rotation of 90 degrees of the map
        env_move_S = np.rot90(np.asarray(env_move_E)).tolist()          # when we make a rotation of 180 degrees of the map
        env_move_O = np.rot90(np.asarray(env_move_S)).tolist()          # when we make a rotation of 270 degrees of the map

        x_agent, y_agent = (24 - y_agent, x_agent)  # the position of agent changes after a rotation of the map
        positionEnnemies = [(24-j,i) for (i,j) in positionEnnemies] # the ennemie position changes after a rotation of the map

        if angle == 180 or angle == 270: 
            x_agent, y_agent = (24 - y_agent, x_agent)
            positionEnnemies = [(24-j,i) for (i,j) in positionEnnemies]
            if angle == 270: 
                x_agent, y_agent = (24 - y_agent, x_agent)
                positionEnnemies = [(24-j,i) for (i,j) in positionEnnemies]
                return self.agent.sensors(self, x = 0, y = -1, environment = env_move_O, positionEnnemies = positionEnnemies)
            else:
                return self.agent.sensors(self, x = 0, y = -1, environment = env_move_S, positionEnnemies = positionEnnemies)
       
        return self.agent.sensors(self, x = 0, y = -1, environment = env_move_E, positionEnnemies = positionEnnemies)

    def actionSelector(self): 
        s = np.sum([np.exp(float(k)/self.Temp) for k in self.U_list])

        action_proba =[np.exp(float(m)/self.Temp)/s for m in self.U_list]
        print(self.U_list)
        print(action_proba)
        return action_proba

    def save_utility_network(self,path_save): 
        """
        Save the utility network into a file 
        """
        self.nn.save_on_file(path_save)

###################################################################### End Class State ######################################################################

def execute_simulation_learning(path_to_nn, display=False): 
    if not(os.path.isfile(path_to_nn)):
        nn = NeuralNetwork(30)
        print("the file %s doesn't exist!"%(path_to_nn))
    else: 
        print("the file %s exist!"%(path_to_nn))
        nn = NeuralNetwork(path_load = path_to_nn)

    experiment = State(obstacles, nn, display)

    if not(display):## if tkinter is desactivated, we need to create the loop with a while condition
        while not(experiment.end):
            experiment.moveEnnemy()
            experiment.moveAgent(True)

    experiment.save_utility_network(path_to_nn)

def train_network(path_save_nn): 
    for i in range(20):
        print("----------------------------------------%d---------------------------------------------" % i)
        execute_simulation_learning(path_save_nn)
        

def execute_simulation_no_learning_no_display(path_to_nn = None):
    if path_to_nn ==None:
        nn = NeuralNetwork(30)
    else:
        nn = NeuralNetwork(path_load = path_to_nn)
    experiment = State(obstacles, nn)
    while not(experiment.end):
        experiment.moveEnnemy()
        experiment.moveAgent()
    return experiment.totalFood

def test_network(path_to_nn):
    results = [0 for i  in range(50)]
    for i in range(50):
        print("----------------------------------------%d---------------------------------------------" % i)
        results[i] = execute_simulation_no_learning_no_display(path_to_nn)
    mean = sum(results)/50
    return (mean,results)

if __name__ == '__main__':
    # start the experiment 
    """for i in range(15):
        train_network("save.h5")

        food = execute_simulation_no_learning_no_display()
        print("food = ", food)
        (m,l) = test_network("save.h5")
        print("nourriture obtenue:", l)
        print("moyenne:", m)"""
    for i in range(5):
        execute_simulation_learning("save.h5",display=True)
    """nn = NeuralNetwork(5)
    test = State(obstacles, nn, display=False)
    test.agent.setPosition(x=12, y=5)
    test.print_sensors(1)
    test.grille.mainloop()"""

    