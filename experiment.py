from agent import *
from neural_network import *
from dynamic_environment import *
import threading


if __name__ == '__main__': 
    l_lr = [0.001,0.01,0.1,0.3,1.0,3.0,10.0]
    l_lr2 = [0.01, 0.03, 0.05, 0.07]
    Temp = [1/20,1/30,1/40,1/50,1/60]
    Temp2 = [1/60, 1/80, 1/100, 1/120, 1/140]
    for lr in l_lr2: 
        
        path_to_nn = "Utility_network/NN_%.3f_60-140.h5"%(lr)
        name_File = "Result/result_%.3f_60-140.txt"%(lr)

        ### Load the neural network if the path exist or not 
        if os.path.isfile(path_to_nn):
            print("The path exist !")
            nn = NeuralNetwork(30,path_load =path_to_nn, lr=lr)
        else: 
            print("The path doesn't exist !")
            nn = NeuralNetwork(30, lr=lr)

        env = State(obstacles, nn, Temp[0],display = False)
        test = False
        result = []
        mean_food = []

        for i in range(7):

            for epoch in range(0,300):
                
                if epoch%60 == 0: 
                    T = Temp[int(epoch/60)]

                #phase entrainement 
                print("########################################### Train-%s ###########################################"%(epoch))
                e = threading.Event()
                env.moveAgent(learning=True, event=e)
                env.moveEnnemy()
                e.wait()
                env.reset(False,result,T)

                if epoch%20 == 0: 
                    #phase test
                    
                    for j in range(0,50):
                        print("########################################### Test-%s ###########################################"%(j))
                        e = threading.Event()
                        env.moveAgent(learning=False, event=e)
                        env.moveEnnemy()
                        e.wait()
                        env.reset(True,mean_food,T)

                    result.append(sum(mean_food)/50)
                    mean_food = []

            with open(name_File, "a") as f:
                f.write("experiment {} mean food : {} .\n".format(i+1,result))
                result = []

        env.save_utility_network(path_to_nn)

        """for i in range(50):
            e = threading.Event()
            env.moveAgent(learning=False, event=e)
            env.moveEnnemy()
            e.wait()
            print('Simulation finished !!!!')
            env.reset(True,result,Temp[0])"""
        """for i in range(7):

            for epoch in range(1,301):
                
                if (epoch-1)%60 == 0: 
                    T = Temp[int((epoch-1)/60)]

                #phase entrainement 
                print("########################################### Train-%s ###########################################"%(epoch))
                env.reset(False,result,T)
                while not env.end:
                    env.moveEnnemy()
                    env.moveAgent(learning = True)

                if epoch%20 == 0: 
                    #phase test
                    
                    for j in range(0,50):
                        print("########################################### Test-%s ###########################################"%(j))
                        env.reset(True,mean_food,T)
                        while not env.end:
                            env.moveEnnemy()
                            env.moveAgent(learning = False)

                    result.append(sum(mean_food)/50)
                    mean_food = []

            with open(name_File, "a") as f:
                f.write("experiment {} mean food : {} .\n".format(i+1,result))
                result = []

        env.save_utility_network(path_to_nn)"""
    

