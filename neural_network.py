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
    def __init__(self, n_hidden):
        super(NeuralNetwork, self).__init__()
        
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

        self.optimizer = tf.keras.optimizers.SGD(learning_rate=0.3, momentum = 0.9 )
        self.model.compile(loss=customLoss)

    @tf.function
    def predict(self,x): 
        return self.model(x)

    def grad(self, Uprime, U):
        
        with tf.GradientTape() as tape:
            loss_value = self.loss(Uprime, U)
        return loss_value, tape.gradient(loss_value, self.model.trainable_variables)

    @tf.function
    def _train_one_step(self, X, y,parameters):
        """
        X : list of inputs of differents action that could be performed 
        """
        r = parameters[0] 
        gamma = parameters[1]

        with tf.GradientTape() as tape:
            yp = self.predict(X) * gamma + r            
            loss = customLoss(yp,y)
        print(loss)
        gradients = tape.gradient(loss, self.model.trainable_variables)
        l = self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        d = dict(loss=loss)
        tf.print(yp[0], loss)


if __name__ == '__main__':
    model = NeuralNetwork(5)

    input_nn = np.random.randint(145, size = 145)
    input_nn = input_nn.reshape(1,145)
    output = model.predict(input_nn) 
    print(float(output))
    input_nn = np.random.randint(145, size = 145)
    input_nn = input_nn.reshape(1,145)
    model._train_one_step([input_nn],output,[0.4,0.9])
