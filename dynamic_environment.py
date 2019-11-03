import sys 
import random
import tkinter
import agent as agt
from ennemy import Ennemy

random.seed()

#dimension de la grille
width = 25
heigth = 25

class State:
    def __init__(self, obstacles):
        self.environment = [[ 0 for j in range(25)] for i in range(25)]
        #0=empty, 1=obstacle, 2= food (ennemy and agent stored separetely)
        for (x,y) in obstacles:
            self.environment[x][y] = 1
        self.ennemies = [Ennemy(6,6), Ennemy(12,2), Ennemy(12,6), Ennemy(18,6)]
        self.agent = agt.Agent(13,12, 40)
        for i in range(15):
            x = random.randint(12,16)
            y = random.randint(12,16)
            while not self.is_empty(x,y):
                x = random.randint(0,24)
                y = random.randint(0,24)
            self.environment[x][y] =2

        self.energy=40

        self.end = False 
        return
    
    def is_empty(self,x,y):
        return (self.environment[x][y]==0) and ((x,y)!= self.agent.getPosition()) and not((x,y) in [i.getPosition() for i in self.ennemies]) and self.environment[x][y]!=1
    
    def remaining_energy(self):
        return self.agent.remaining_energy()
    
    #------------- fonction pour tester une case
    
    def lookupObstacles(self, x, y):
        if x<0 or x>=width or y<0 or y>=heigth:
            return True
        if self.environment[x][y]==1:
            #print("obstacles !!! ")
            return True
        else:
            return False
    
    def lookupFood(self, x, y):
        if x<0 or x>=width or y<0 or y>=heigth:
            return False
        if self.environment[x][y]==2:
            #print("food !!! ")
            return True
        else:
            return False
    
    def lookupEnnemies(self, x, y):
        positionEnnemies = [i.getPosition() for i in self.ennemies]

        if x<0 or x>=width or y<0 or y>=heigth:
            return False
        if (x,y) in positionEnnemies:
            #print("An ennemiy !!! ")
            return True
        else:
            return False
    
    def lookUpSensor(self, lookup, x, y):
        #  if 2 we use the sensor to detect the food 
        if lookup == 2:   
            return self.lookupFood(x,y)
        #  if 1 we use the sensor to detect the ennemies 
        elif lookup == 1:           
            return self.lookupEnnemies(x,y)
        #  else we use the sensor to detect the obstacles
        else: 
            return self.lookupObstacles(x,y)

    #---------------fonction de patch d'observation-------------
    
    def opatch(self, x, y):
        return self.lookUpSensor(0, x,y)
    
    def Xpatch(self, lookup, x, y):
        # lookup could be 2 to detect the food or 1 to detect the ennemies  
        return self.lookUpSensor(lookup, x,y) or self.lookUpSensor(lookup, x-1,y) or self.lookUpSensor(lookup, x+1,y)\
         or self.lookUpSensor(lookup, x,y-1) or self.lookUpSensor(lookup, x,y+1)
    
    def Opatch(self, lookup, x, y):
        # lookup could be 2 to detect the food or 1 to detect the ennemies
        return self.Xpatch(lookup,x,y) or self.lookUpSensor(lookup, x-1,y-1) or self.lookUpSensor(lookup, x-1,y+1)\
         or self.lookUpSensor(lookup, x+1,y-1) or self.lookUpSensor(lookup, x+1,y+1)
    
    def Ypatch(self, x, y):
        return self.Opatch(2,x,y) or self.lookUpSensor(2, x-2,y) or self.lookUpSensor(2, x+2,y)\
         or self.lookUpSensor(2, x,y-2) or self.lookUpSensor(2, x,y+2)
    
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
        
        self.Opatch(2,self.agent.x, self.agent.y)
        self.ennemyText = []
        for i in range(25): 
            self.can.create_line(0,self.PAS*i,windows_Size,self.PAS*i,fill='black')      # on cree manuellement des lignes horizontales  
            self.can.create_line(self.PAS*i , 0,self.PAS*i,windows_Size,fill='black')    # on cree manuellement des lignes verticales 

            for j in range(25):         
                centre = (X0+i*self.PAS, Y0+j*self.PAS) 

                # Part to write the sensors shape for debug 
                """if (i,j) in sensorsY: 
                    self.can.create_text(centre, text = "Y")
                elif (i,j) in sensorsO: 
                    self.can.create_text(centre, text = "O")
                elif (i,j) in sensorsX: 
                    self.can.create_text(centre, text = "X")"""
                
                if (i,j)==self.agent.getPosition():
                    self.agentText = self.can.create_text(centre, text = "I")
                
                elif (i,j) in [i.getPosition() for i in self.ennemies]:
                    self.ennemyText.append(self.can.create_text(centre, text = "E"))
                
                elif self.environment[i][j]==2:
                    self.can.create_text(centre, text = "$")
                elif self.environment[i][j] == 1:
                    self.can.create_text(centre, text = "O") 
        
        #create the HP bar in the bottom
        self.life = []  # all rectangle for the life 

        self.can_life=tkinter.Canvas(self.grille,bg="light gray",height=25, width=200)
        self.can_life.pack(side = "left") 

        for i in range(1,200,25): 
            self.life.append(self.can_life.create_rectangle( i, 0, i+25, 25, fill="red", width = 0.5))           
                        
    def moveAgent(self):
        getFood = False # boolean to know if the move of agent allowed him to get food or not 
        self.agent.policy(self, self.can, self.agentText, self.PAS)
        self.agent.sensors(self)

        x,y = self.agent.getPosition()

        if self.lookupEnnemies(x,y): 
            self.end = True

        elif self.lookupFood(x,y):
            self.agent.setEnergy(15)
            getFood = True
        else: 
            self.agent.setEnergy(-1)

        self.agent.updateEnergy(self.can_life,self.life, getFood)
        self.grille.after(1000,self.moveAgent)    # Resubscribe to make move again the agent each second

    def moveEnnemy(self):
        """
        Function to make move the ennemies
        """
        for i,ennemy in enumerate(self.ennemies):

            r = random.uniform(0,1)
            if r > 0.2 : 
                ennemy.strategy(self, self.can, self.ennemyText[i], self.PAS)

        """r = random.uniform(0,1)
        if r > 0.2 : 
            self.ennemies[1].strategy(self, self.can, self.ennemyText[1], self.PAS)"""
        self.grille.after(1200, self.moveEnnemy)  # Resubscribe to make move again the agent each second


    def update(self):
        self.print_grid_line()


        self.grille.after(1000,self.moveAgent)  # Subscribe to make move the agent 
        #self.grille.after(1200, self.moveEnnemy) # Subscribe to make move the ennemies 
        self.grille.mainloop()

if __name__ == '__main__':
    
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

    test= State(obstacles)

    test.update()

    