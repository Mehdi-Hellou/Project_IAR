# Self-Improving Reactive Agent Based on Reinforcement Learning, Planning and Teaching 

Project to create a self-learning agent in a complex environment. Based on the paper "Self-improving reactive agents based on reinforcement learning, planning and teaching", Long-ji Lin, 1992. 

# Purpose
survive in a complex environment surrounded by predators, ressources and obstacles. The environment include an agent, 
which can collect ressources and move inside the 2D environment to avoid predators and obstacles.  

# DEPENDANCES 
- tkinter 
- tensorflow2.0

# Files

## dynamic_environment.py 

This is the main file that allows to create the simulation environment, where the agent will be able to move and the enemies will be able to move as well. 
The display grid is realized using the "tkinter" library to display the environment, the enemies(E), the obstacles(O), the agent(I) and the life bar at the bottom left. 

It is also in this part that the agent will learn using its sensors and the neural network, created in another file. 

## agent.py 

This file allows the agent to move according to the policy and his sensors to observe his environment.

## ennemy.py 
This file describe the moving policy of ennemy according the algorithms defined on the paper. 

## neural_network.py 
In this file, the neural network is created to calculate the usefulness of an action given the agent's state.

You can modify the error function and whether use the mean absolute error(mae) which calculates the absolute value of the error between the target and the prediction, or use the mean squared error(mse) which calculates the value of the quadratic error between the target and the prediction.

The libraries used are tensorflow 2.0 to create the neural network and do the backpropagation learning.


## test.py 
Test file to check if the sensors are well coded. 
