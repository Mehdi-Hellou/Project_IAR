
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
    
    
    #test fonction rotations 
    def testRotation(self):
        testgrid= env.State([(5,5),(8,5),(5,7)],nn)
        env_90 = env.State([(5,5),(8,5),(5,7)],nn)
        env_180 = env.State([(5,5),(8,5),(5,7)],nn)
        env_270 = env.State([(5,5),(8,5),(5,7)],nn)

        # We delete all the case whit food since it is plot randomly
        for i in range(env.width):
            for j in range(env.heigth):
                if testgrid.environment[i][j] == 2: 
                    testgrid.environment[i][j]=0
                if env_90.environment[i][j] == 2: 
                    env_90.environment[i][j]=0
                if env_180.environment[i][j] == 2: 
                    env_180.environment[i][j]=0
                if env_270.environment[i][j] == 2: 
                    env_270.environment[i][j]=0

        e = np.asarray(testgrid.environment)
        
        e = np.rot90(e)
        env_90.environment = e.tolist() # environment with a rotation of 90
        env_90.ennemies = [Ennemy(18,6,env_90.environment), Ennemy(22,12,env_90.environment), Ennemy(18,12,env_90.environment), Ennemy(18,18,env_90.environment)]

        e = np.rot90(e)
        env_180.environment = e.tolist() # environment with a rotation of 180
        env_180.ennemies = [Ennemy(18,18,env_180.environment), Ennemy(12,22,env_180.environment), Ennemy(12,18,env_180.environment), Ennemy(6,18,env_180.environment)]

        e = np.rot90(e)
        env_270.environment = e.tolist() # environment with a rotation of 270
        env_270.ennemies = [Ennemy(6,18,env_270.environment), Ennemy(2,12,env_270.environment), Ennemy(6,12,env_270.environment), Ennemy(6,6,env_270.environment)]

        sensors_O = testgrid.rotationEnvironment(90) # sensors when the environment is rotated at 90 degrees
        sensors_S = testgrid.rotationEnvironment(180) # sensors when the environment is rotated at 180 degrees
        sensors_E = testgrid.rotationEnvironment(270) # sensors when the environment is rotated at 270 degrees

        sensors_env_90 = testgrid.agent.sensors( testgrid, x = 1, y = 0)
        sensors_env_270 = testgrid.agent.sensors( testgrid, x = -1, y = 0)
        sensors_env_180 = testgrid.agent.sensors( testgrid, x = 0, y = +1)
        
        #print(np.asarray(sensors_env_90).astype(int))
        #print(np.asarray(sensors_E).astype(int))
        #self.assertTrue(sensors_E==sensors_env_90)
        #self.assertTrue(sensors_S==sensors_env_180)
        #self.assertTrue(sensors_O==sensors_env_270)

    #test fonction sensors en simulant le mouvement de l'agent  
    def testRotationSensors(self):
        testgrid= env.State([(5,5),(8,5),(5,7)],nn)
        (x,y) = testgrid.agent.getPosition()
        testgrid.agent.setPosition(10, 7)
        sensors_N_sim = np.asarray(testgrid.agent.sensors_without_rot(testgrid,direction=3)).astype(int)
        sensors_E_sim = np.asarray(testgrid.agent.sensors_without_rot(testgrid,direction=0)).astype(int)
        sensors_S_sim = np.asarray(testgrid.agent.sensors_without_rot(testgrid,direction=1)).astype(int)
        sensors_O_sim = np.asarray(testgrid.agent.sensors_without_rot(testgrid,direction=2)).astype(int)   
        testgrid.print_grid_line()
        testgrid.grille.mainloop()

        (x_n,y_n) = testgrid.agent.move(3,state = testgrid)
        (x_e,y_e) = testgrid.agent.move(0,state = testgrid)
        (x_s,y_s) = testgrid.agent.move(1,state = testgrid)
        (x_o,y_o) = testgrid.agent.move(2,state = testgrid)

        testgrid.agent.setPosition(x_s,y_s)        
        self.assertTrue(np.array_equal(sensors_S_sim, np.asarray(testgrid.agent.sensors(testgrid)).astype(int)))

        testgrid.agent.setPosition(10, 7)
        testgrid.agent.setPosition(x_n,y_n)
        self.assertTrue(np.array_equal(sensors_N_sim, np.asarray(testgrid.agent.sensors(testgrid)).astype(int)))

        testgrid.agent.setPosition(10, 7)
        testgrid.agent.setPosition(x_e,y_e)
        self.assertTrue(np.array_equal(sensors_E_sim, np.asarray(testgrid.agent.sensors(testgrid)).astype(int)))

        testgrid.agent.setPosition(10, 7)
        testgrid.agent.setPosition(x_o,y_o)
        self.assertTrue(np.array_equal(sensors_O_sim, np.asarray(testgrid.agent.sensors(testgrid)).astype(int)))
        
        
        
if __name__ == '__main__':
    unittest.main()
