import sys 
import tensorflow as tf
import numpy as np

@tf.function
def new_sigmoid(x): 
	return (1/(1+tf.math.exp(-x))) - 0.5

class NeuralNetwork(object):
	"""docstring for NeuralNetwork"""
	def __init__(self, n_hidden):
		super(NeuralNetwork, self).__init__()
		
		self.model = tf.keras.models.Sequential()
		
		self.model.add(tf.keras.layers.InputLayer(input_shape=(145,)))

		for i in range(3):
			self.model.add(tf.keras.layers.Dense( n_hidden, activation = new_sigmoid))

		self.model.add(tf.keras.layers.Dense(1, activation = new_sigmoid))

	def predict(self,x): 
		x = x.reshape(1,145)
		return self.model.predict(x)

if __name__ == '__main__':
	model = NeuralNetwork(5)

	input = np.ones((145))
	output = model.predict(input)  

	print(output)