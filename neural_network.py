import sys 
import tensorflow as tf
import numpy as np

#@tf.function
def new_sigmoid(x):
    """
    Activate function
    """ 
    return (1/(1+tf.math.exp(-x))) - 0.5

#@tf.function
def customLoss(yp, y): 
    """
    fonction loss 
    """
    return abs(y - yp)

def derivate_sigmoid(x): 
    return (1/(1+tf.math.exp(-x)))*(1-(1/(1+tf.math.exp(-x))))

class NeuralNetwork(object):
    """docstring for NeuralNetwork"""
    def __init__(self,n_hidden = None, path_load = None, lr = 0.3):
        if (n_hidden == None) and (path_load == None ):
            raise ValueError("Un argument est nécessaire")
        super(NeuralNetwork, self).__init__()
        if path_load == None:
            print("New NN")
            self.model = tf.keras.models.Sequential()

            #add the the input layer 
            self.model.add(tf.keras.layers.InputLayer(input_shape=(145,)))
            #inputs = tf.keras.layers.Input(shape=(145,))

            # add the hidden layers 
            init = tf.constant_initializer(0.1*np.random.rand(145,n_hidden))
            self.model.add(tf.keras.layers.Dense( n_hidden, activation = new_sigmoid, kernel_initializer= init))
            #x = tf.keras.layers.Dense( n_hidden, activation = new_sigmoid, kernel_initializer= init)(inputs)
            #self.model.add(tf.keras.layers.Dense( n_hidden, activation = "softmax", kernel_initializer= init))

            #Add the output layers
            init = tf.constant_initializer(0.01*np.random.rand(n_hidden,1))
            self.model.add(tf.keras.layers.Dense(1, activation = new_sigmoid, kernel_initializer= init ) )
            #outputs = tf.keras.layers.Dense(1, activation = new_sigmoid, kernel_initializer= init )(x)
            #self.model.add(tf.keras.layers.Dense(1, activation = "softmax", kernel_initializer= init ) )

            #self.model = tf.keras.Model(inputs=inputs, outputs=outputs)           
            self.model.compile(optimizer = tf.keras.optimizers.SGD(learning_rate=lr, momentum = 0.9 ), # optimizer 
                              loss=customLoss)          # the loss function
        else:
            print("Same NN")
            self.model  = tf.keras.models.load_model(path_load, custom_objects={'new_sigmoid': new_sigmoid, "customLoss" : customLoss})

        self.optimizer = tf.keras.optimizers.SGD(learning_rate=lr, momentum = 0.9 )
        self.loss_fn = tf.keras.losses.MeanAbsoluteError()

    def predict(self,x): 
        return self.model(x)

    def save_on_file(self,path):
        self.model.save(path)

    def grad(self, inputs, target):
        """
        """
        with tf.GradientTape() as tape:
            yp = self.predict(inputs)
            loss_value = customLoss(yp,target)
            #loss_value = self.loss_fn(target,yp)

        print("the prediction is %s" %(yp))
        print("the target is %s" %(target))
        return loss_value, tape.gradient(loss_value, self.model.trainable_variables)

    @tf.function
    def _train_one_step(self, X, Xtarget,parameters, end):
        """
        X : list of inputs of differents action that could be performed 
        """        
        r = parameters[1]
        gamma = parameters[0]
        with tf.GradientTape() as tape:
            yp = self.predict(X)

            if end:
                ytarget = r
            else: 
                ytarget = self.predict(Xtarget) * gamma + r
            
            loss = customLoss(ytarget,yp)
        #print(loss)
        print(tf.executing_eagerly())
        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        tf.print("Step: {},         Loss: {}".format(int(self.optimizer.iterations),loss))
        d = dict(loss=loss)
        #tf.print(yp[0], loss)        

    def train_one_step_other(self, X, target):
        """
        X : input for the prediction
        target : the target label 

        """
        #print("########################Input###############################")
        #print(X)

        loss , gradients = self.grad(X,target)
        #print("########gradient########")
        #tf.print(gradients[0]) 
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        tf.print("Step: {},         Loss: {}".format(self.optimizer.iterations.numpy(),loss))
        #self.print_weight()
    
    def print_weight(self):
        tf.print(self.model.trainable_variables[0])
    
    def train(self,X,target): 
        self.model.fit(X,target)

def try_nn(nb_hidden, input_nn, parameters,path_load = None, path_save = None):
    #les fichiers de sauvegarde sont des .h5
    if path_load != None:
        network = NeuralNetwork( path_load = path_load)
    else:
        network = NeuralNetwork(n_hidden = nb_hidden)
    output = network.predict(input_nn)
    print(input_nn)
    np.random.seed(5)
    input_nn2 = np.random.choice(2, size = 145)
    input_nn2 = input_nn.reshape(1,145)
    target = -0.0000 + 0.9*network.predict(input_nn2) 
    network.train_one_step_other(input_nn,target)
    print(input_nn)
    print(target)
    #network.train(input_nn, target)
    if path_save != None:
        network.save_on_file(path_save)
    return output


if __name__ == '__main__':
    input_nn = np.random.choice(2, size = 145)
    input_nn = input_nn.reshape(1,145)
    #output = try_nn(5, input_nn, [0.4,0.9],path_load = "save.h5", path_save = "save.h5")
    output = try_nn(5, input_nn, [0.4,0.9])
    #model = NeuralNetwork(5)

#     output = model.predict(input_nn) 
#     output = try_nn
#     print(float(output))
#     input_nn = np.random.randint(145, size = 145)
#     input_nn = input_nn.reshape(1,145)
#     model._train_one_step([input_nn],output,[0.4,0.9])







