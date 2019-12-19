import threading
import unittest
import agent
import dynamic_environment as env
from ennemy import Ennemy
from neural_network import *

nn = NeuralNetwork(5)  # the neural network used for the learning
class testState(unittest.TestCase):
    
    
    #tests des fonction de lookup et de la fonciton opatch
    
    def testObstacleDetection(self):
        testgrid= env.State([(5,5)],nn)
        for i in range(-1, env.width+1, 1):
            for j in range(-1, env.heigth+1, 1):
                if (i==5 and j==5) or i<0 or i>=env.width or j<0 or j>=env.heigth:
                    self.assertTrue(testgrid.lookupObstacles(i,j))
                    self.assertTrue(testgrid.opatch(i,j))
                else:
                    self.assertFalse(testgrid.lookupObstacles(i,j))
                    self.assertFalse(testgrid.opatch(i,j))
                    
    def testEnnemyLookUp(self):
        testgrid= env.State([],nn)
        testgrid.ennemies=([Ennemy(5,5,testgrid.environment), Ennemy(-1,-1,testgrid.environment)])
        for i in range(-1, env.width+1, 1):
            for j in range(-1, env.heigth+1, 1):
                if i==5 and j==5:
                    self.assertTrue(testgrid.lookupEnnemies(i,j))
                else:
                    self.assertFalse(testgrid.lookupEnnemies(i,j))
        
    def testFoodLookUp(self):
        testgrid= env.State([],nn)
        for i in range(env.width):
            for j in range(env.heigth):
                testgrid.environment[i][j]=0
        testgrid.environment[5][5]=2
        for i in range(-1, env.width+1, 1):
            for j in range(-1, env.heigth+1, 1):
                if i==5 and j==5:
                    self.assertTrue(testgrid.lookupFood(i,j))
                else:
                    self.assertFalse(testgrid.lookupFood(i,j))
    
    
    #tests des fonctions patches
    
    def testXPatch(self):
        testgrid= env.State([],nn)
        for i in range(env.width):
            for j in range(env.heigth):
                testgrid.environment[i][j]=0
        testgrid.environment[10][10]=2
        testgrid.ennemies=([Ennemy(5,5,testgrid.environment), Ennemy(-1,0,testgrid.environment)])
        for i in range(-1, env.width+1, 1):
            for j in range(-1, env.heigth+1, 1):
                if (i==5 and j==5) or (i==4 and j==5) or (i==5 and j==4) or (i==6 and j==5) or (i==5 and j==6):
                    self.assertTrue(testgrid.Xpatch(1,i,j))
                    self.assertFalse(testgrid.Xpatch(2,i,j))
                elif (i==10 and j==10) or (i==9 and j==10) or (i==10 and j==9) or (i==11 and j==10) or (i==10 and j==11):
                    self.assertTrue(testgrid.Xpatch(2,i,j))
                    self.assertFalse(testgrid.Xpatch(1,i,j))
                else:
                    self.assertFalse(testgrid.Xpatch(1,i,j))
                    self.assertFalse(testgrid.Xpatch(2,i,j))
    
    def testOPatch(self):
        testgrid= env.State([],nn)
        for i in range(env.width):
            for j in range(env.heigth):
                testgrid.environment[i][j]=0
        testgrid.environment[10][10]=2
        testgrid.ennemies=([Ennemy(5,5,testgrid.environment), Ennemy(-1,0,testgrid.environment)])
        for i in range(-1, env.width+1, 1):
            for j in range(-1, env.heigth+1, 1):
                if (i==5 and j==5) or (i==4 and j==5) or (i==5 and j==4) or (i==6 and j==5) or (i==5 and j==6) or (i==4 and j==4) or (i==4 and j==6) or (i==6 and j==6) or (i==6 and j==4):
                    self.assertTrue(testgrid.Opatch(1,i,j))
                    self.assertFalse(testgrid.Opatch(2,i,j))
                elif (i==10 and j==10) or (i==9 and j==10) or (i==10 and j==9) or (i==11 and j==10) or (i==10 and j==11) or (i==9 and j==9) or (i==9 and j==11) or (i==11 and j==9) or (i==11 and j==11):
                    self.assertTrue(testgrid.Opatch(2,i,j))
                    self.assertFalse(testgrid.Opatch(1,i,j))
                else:
                    self.assertFalse(testgrid.Opatch(1,i,j))
                    self.assertFalse(testgrid.Opatch(2,i,j))
    

        
if __name__ == '__main__':
    unittest.main()
