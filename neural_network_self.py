# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 13:46:08 2018

@author: usman
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

def sigmoid(x):
    return 1/(1+np.exp(-x)) - 0.5

def sigmoid_der(x):
    return sigmoid(x) *(1-sigmoid (x))

def customLoss(yp, y): 
    """
    fonction loss 
    """
    return abs(y - yp)

class Neural_Network():
    """docstring for Neural_Network"""
    def __init__(self):
        
        self.wh = np.random.uniform(-0.1,0.1,[145,30]) 
        self.wo = np.random.uniform(-0.1,0.1,[30, 1])
        self.lr = 0.1

    def predict(self, X): 
        # feedforward
        zh = np.dot(X, self.wh)
        ah = sigmoid(zh)

        zo = np.dot(ah, self.wo)
        ao = sigmoid(zo)
        return ao 

    def gradientDescent(self,X,target): 
    # Phase1 =======================
                
        zh = np.dot(X, self.wh)

        ah = sigmoid(zh)
        zo = np.dot(ah, self.wo)
        
        ao = self.predict(X)
        print("the target is %s"%(target))
        print("the prediction is %s"%(ao))
        error_out = customLoss(ao,target) 
        print(error_out.sum())

        dcost_dao = 1 if target>ao else -1 if target<ao else 0
        dao_dzo = sigmoid_der(zo) 
        dzo_dwo = ah

        dcost_wo = np.outer(dzo_dwo, dcost_dao * dao_dzo)
        #dcost_wo = np.dot(dzo_dwo.T, dcost_dao * dao_dzo)

        # Phase 2 =======================

        # dcost_w1 = dcost_dah * dah_dzh * dzh_dw1
        # dcost_dah = dcost_dzo * dzo_dah
        dcost_dzo = dcost_dao * dao_dzo
        dzo_dah = self.wo
        dcost_dah = np.dot(dcost_dzo , dzo_dah.T)
        dah_dzh = sigmoid_der(zh) 
        dzh_dwh = X
        dcost_wh = np.outer(dzh_dwh.T, dah_dzh * dcost_dah)
        #np.dot(dzh_dwh.T, dah_dzh * dcost_dah)
        # Update Weights ================

        self.wh -= self.lr * dcost_wh
        self.wo -= self.lr * dcost_wo

if __name__ == '__main__':
    input_nn = np.random.choice(2, size = 145)
    np.random.seed(5)
    input_nn2 = np.random.choice(2, size = 145)
    nn = Neural_Network()
    output = nn.predict(input_nn2)
    nn.gradientDescent(input_nn,output)

