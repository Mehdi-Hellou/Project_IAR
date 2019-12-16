from agent import *
from neural_network import *
from dynamic_environment import *
import threading


if __name__ == '__main__': 
    l_lr = [0.001,0.01,0.1,0.3,1.0]
    l_lr2 = [0.01, 0.03, 0.05, 0.07]
    Temp = [1/20,1/30,1/40,1/50,1/60]
    Temp2 = [1/60, 1/80, 1/100, 1/120, 1/140]
    for lr in l_lr[2:3]: 
        
        path_to_nn = "Utility_network/NN_%.3f_test.h5"%(lr)
        name_File = "Result/result_%.3f_30.txt"%(lr)

        ### Load the neural network if the path exist or not 
        if os.path.isfile(path_to_nn):
            print("The path exist !")
            nn = NeuralNetwork(30,path_load =path_to_nn, lr=lr)
        else: 
            print("The path doesn't exist !")
            nn = NeuralNetwork(30, lr=lr)
        test = False
        result = []
        mean_food = []
        nb_lessons = 12 
        with open(name_File, "a") as f:
                f.write("Parameter : lr = %.3f Temp_init = %.3f \n"%(lr,Temp[0]))
        for i in range(1):
            nn = NeuralNetwork(30, lr=lr)
            env = State(obstacles, nn, Temp[0],display = False)
            for epoch in range(0,300):
                
                if epoch%60 == 0: 
                    #T = Temp[int(epoch/60)]
                    T = Temp[1]
                # decrease the number of lessons played along the number of training made 
                if epoch%37 == 36: 
                    if nb_lessons>4: 
                        nb_lessons=-1

                #phase entrainement 
                print("########################################### Train-%s ###########################################"%(epoch))
                count = 0
                env.reset(False,result,T)
                while not env.end:
                    #count+=0.1
                    env.moveAgent(learning = True)
                    #if count%0.2==0: 
                    env.moveEnnemy()
                # experience replay 
                """if epoch > 12: 
                    env.replay(nb_lessons)"""

                if epoch%20 == 19: 
                    #phase test
                    
                    for j in range(0,50):
                        print("########################################### Test-%s ###########################################"%(j))
                        env.reset(True,mean_food,T)
                        count = 0
                        while not env.end:
                            #count+=0.1                            
                            env.moveAgent(learning = False)
                            #if count%0.2==0: 
                            env.moveEnnemy()

                    result.append(sum(mean_food)/50)
                    mean_food = []

            with open(name_File, "a") as f:
                f.write("experiment {} mean food : {} \n".format(i+1,result))
                result = []

            env.save_utility_network(path_to_nn)
    

