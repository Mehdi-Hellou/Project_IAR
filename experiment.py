from agent import *
from neural_network import *
from neural_network_self import *
from dynamic_environment import *
import threading
from simple_nn import Network

if __name__ == '__main__': 
    l_lr = [0.001,0.01,0.1,0.15,0.3,1.0]
    l_lr2 = [0.1, 0.125, 0.15, 0.175]
    Temp = [1/20,1/30,1/40,1/50,1/60]
    Temp2 = [1/60, 1/80, 1/100, 1/120, 1/140]
    Temp3 = [1/40, 1/60, 1/70, 1/80, 1/100]
    Temp4 = [1/120, 1/140, 1/160, 1/180, 1/200]
    for T in Temp3[2:3]: 
        for lr in l_lr[3:4]:
            
            # path to save the neural network 
            path_to_nn = "Utility_network/NN_%.3f_%d_mse_var.h5"%(lr,1/T)
            name_File = "Result/result_%.3f_%d_mse_var.txt"%(lr, 1/T)     # path to save the result of experiments

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
            with open(name_File, "a") as f:
                    f.write("Parameter : lr = %.3f Temp_init = %s \n"%(lr,T))

            for i in range(6,7):
                nn = NeuralNetwork(30, lr=lr)    # the neural network use during each experiment
                env = State(obstacles, nn, T,display = False, interval = Temp3)  # we create the state for the trainings
                nb_lessons = 12 
                for epoch in range(0,300):   # for 300 training environments   
                    
                    # in case the temperature isn't fixed
                    """if epoch%60 == 0: 
                        T = Temp[int(epoch/60)]
                        T = Tmp[0]"""
                    
                    # decrease the number of lessons played along the number of training made 
                    if epoch%37 == 36: 
                        if nb_lessons>4: 
                            nb_lessons=-1

                    #phase entrainement 
                    print("########################################### Train-%s ###########################################"%(epoch))
                    count = 0
                    env.reset(False,result,T)
                    while not env.end:
                        count+=0.1
                        env.moveAgent(learning = True)
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
                                count+=0.1                            
                                env.moveAgent(learning = False) 
                                env.moveEnnemy()

                        result.append(sum(mean_food)/50)
                        mean_food = []

                with open(name_File, "a") as f:
                    f.write("experiment {} mean food : {} \n".format(i+1,result))
                    result = []

                env.save_utility_network(path_to_nn)

