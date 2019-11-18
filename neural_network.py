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

		self.optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)
		self.loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)


	def predict(self,x): 
		x = x.reshape(1,145)
		return self.model.predict(x)

	def loss(self,y, y0):
		
		return self.loss_object(y_true=y, y_pred=y0)
		#return tf.sum((y - y0))

	def grad(self, Uprime, U):
		
		with tf.GradientTape() as tape:
			loss_value = self.loss(Uprime, U)
		print(loss_value)
		return loss_value, tape.gradient(loss_value, self.model.trainable_variables)


	def train(self, Uprime, U):
		loss_value, grads = self.grad(Uprime, U) 
		self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))



if __name__ == '__main__':
	model = NeuralNetwork(5)

	input = np.ones((145))
	output = model.predict(input)  

	print(output)