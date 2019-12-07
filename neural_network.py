import sys 
import tensorflow as tf
import numpy as np

@tf.function
def new_sigmoid(x):
    """
    Activate function
    """ 
    return (1/(1+tf.math.exp(-x))) - 0.5

@tf.function
def customLoss(y, y0): 
    """
    fonction loss 
    """
    return (y - y0)

class NeuralNetwork(object):
    """docstring for NeuralNetwork"""
    def __init__(self, n_hidden = None, path_load = None):
        if (n_hidden == None) and (path_load == None ):
            raise ValueError("Un argument est nécessaire")
        super(NeuralNetwork, self).__init__()
        if path_load == None:
            self.model = tf.keras.models.Sequential()

            #add the the input layer 
            self.model.add(tf.keras.layers.InputLayer(input_shape=(145,)))

            # add the hidden layers 
            init = tf.constant_initializer(0.1*np.random.rand(145,n_hidden))
            self.model.add(tf.keras.layers.Dense( n_hidden, activation = new_sigmoid, kernel_initializer= init))

            init = tf.constant_initializer(0.1*np.random.rand(n_hidden,n_hidden))
            self.model.add(tf.keras.layers.Dense( n_hidden, activation = new_sigmoid, kernel_initializer= init))

            init = tf.constant_initializer(0.1*np.random.rand(n_hidden,n_hidden))
            self.model.add(tf.keras.layers.Dense( n_hidden, activation = new_sigmoid, kernel_initializer= init))

            init = tf.constant_initializer(0.1*np.random.rand(n_hidden,1))
            self.model.add(tf.keras.layers.Dense(1, activation = new_sigmoid, kernel_initializer= init ) )
            self.model.compile(loss=customLoss)           
        else:
            self.model  = tf.keras.models.load_model(path_load, custom_objects={'new_sigmoid': new_sigmoid, "customLoss" : customLoss})
        
        self.optimizer = tf.keras.optimizers.SGD(learning_rate=0.3, momentum = 0.9 )
        

    @tf.function
    def predict(self,x): 
        return self.model(x)

    def save_on_file(self,path):
        self.model.save(path)

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
        gradients = tape.gradient(loss, self.model.trainable_variables)
        l = self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        d = dict(loss=loss)
        #tf.print(yp[0], loss)
#

def try_nn(nb_hidden, input_nn, parameters,path_load = None, path_save = None):
    #les fichiers de sauvegarde sont des .h5
    if path_load != None:
        network = NeuralNetwork( path_load = path_load)
    else:
        network = NeuralNetwork(n_hidden = nb_hidden)
    output = network.predict(input_nn)
    network._train_one_step([input_nn],output,parameters,False)
    if path_save != None:
        network.save_on_file(path_save)
    return output


if __name__ == '__main__':
    input_nn = np.random.randint(145, size = 145)
    input_nn = input_nn.reshape(1,145)
    output = try_nn(5, input_nn, [0.4,0.9,0.5],path_load = "save.h5", path_save = "save.h5")
    print(float(output))
    #model = NeuralNetwork(5)

#     output = model.predict(input_nn) 
#     output = try_nn
#     print(float(output))
#     input_nn = np.random.randint(145, size = 145)
#     input_nn = input_nn.reshape(1,145)
#     model._train_one_step([input_nn],output,[0.4,0.9])







