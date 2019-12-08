from agent import *
from neural_network import *
from dynamic_environment import *
import time


if __name__ == '__main__': 
    nn = NeuralNetwork(30,lr=0.1)
    env = State(obstacles, nn, display = False)

    test = False
    result = []
    mean_food = []
    for i in range(7):
        for epoch in range(0,300):
            #phase entrainement 
            print("########################################### Train-%s ###########################################"%(epoch))
            env.reset(False,result)
            while not env.end:
                env.moveEnnemy()
                env.moveAgent(learning = True)

            if epoch%20 == 0: 
                #phase test
                
                for j in range(0,50):
                    print("########################################### Test-%s ###########################################"%(j))
                    env.reset(True,mean_food)
                    while not env.end:
                        env.moveEnnemy()
                        env.moveAgent(learning = False)

                result.append(sum(mean_food)/50)
                mean_food = []

        with open("Result/result2.txt", "a") as f:
            f.write("experiment {} mean food : {} .\n".format(i+1,result))
            result = []

    env.save_utility_network("Utility_network/NN_version2.h5")
    
    """env.display = True
    env.reset(True,mean_food)
    env.print_grid_line()
    env.moveAgent(learning=False) 
    env.moveEnnemy()
    env.grille.mainloop()""" 
