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

            # add the hidden layers 
            init = tf.constant_initializer(np.random.uniform(-0.1,0.1,[145,n_hidden]))
            self.model.add(tf.keras.layers.Dense( n_hidden, activation = new_sigmoid, kernel_initializer= init))

            #Add the output layers
            init = tf.constant_initializer(np.random.uniform(-0.1,0.1,[n_hidden,1]))
            self.model.add(tf.keras.layers.Dense(1, activation = new_sigmoid, kernel_initializer= init ) )

            self.model.compile(optimizer = tf.keras.optimizers.SGD(learning_rate=lr, momentum = 0.9 ), # optimizer 
                              loss=customLoss)          # the loss function

        else:
            print("Same NN")
            self.model  = tf.keras.models.load_model(path_load, custom_objects={'new_sigmoid': new_sigmoid, "customLoss" : customLoss})

        self.optimizer = tf.keras.optimizers.SGD(learning_rate=lr, momentum = 0.9 )
        # uncomment this line to use the MAE 
        #self.loss_fn = tf.keras.losses.MeanAbsoluteError()   # loss function that uses Mean Absolute differences from keras in order to compute the error 
        self.loss_fn = tf.keras.losses.MeanSquaredError()     # loss function that uses Mean Squared differences from keras in order to compute the error

    def predict(self,x): 
        return self.model(x)

    def save_on_file(self,path):
        self.model.save(path)

    def grad(self, x, target):
        """
        Compute the gradient of the errors between the prediction of x and the target given
        """
        with tf.GradientTape() as tape:
            yp = self.predict(x)
            #loss_value = customLoss(yp,target)     # loss value made by hand 
            loss_value = self.loss_fn(target,yp)   # loss value provide by tensorflow 

        print("the prediction is %s" %(yp))
        print("the target is %s" %(target))
        return loss_value, tape.gradient(loss_value, self.model.trainable_variables)

    def train_one_step_other(self, X, target):
        """
        X : input for the prediction
        target : the target label 

        """
        loss , gradients = self.grad(X,target) 
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        tf.print("Step: {},         Loss: {}".format(self.optimizer.iterations.numpy(),loss))
    
    def print_weight(self):
        tf.print(self.model.trainable_variables[0])
    
    def train(self,X,target): 
        """
        """
        self.model.fit(X,target,verbose=0)

def try_nn(nb_hidden, input_nn, parameters,path_load = None, path_save = None):
    #les fichiers de sauvegarde sont des .h5
    if path_load != None:
        network = NeuralNetwork( path_load = path_load)
    else:
        network = NeuralNetwork(n_hidden = nb_hidden)
    output = network.predict(input_nn)
    np.random.seed(5)
    input_nn2 = np.random.choice(2, size = 145)
    input_nn2 = input_nn.reshape(1,145)
    target = -0.0000 + 0.9*network.predict(input_nn2) 
    network.train_one_step_other(input_nn,target)

    if path_save != None:
        network.save_on_file(path_save)
    return output


if __name__ == '__main__':
    input_nn = np.random.choice(2, size = 145)
    input_nn = input_nn.reshape(1,145)
    output = try_nn(5, input_nn, [0.4,0.9])






