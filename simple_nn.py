import torch
import torch.nn as nn
import numpy as np
import sys 

## sigmoid activation function using pytorch
def sigmoid_activation(z):
    return 1 / (1 + torch.exp(-z)) - 0.5


def customLoss(yp, y): 
    """
    fonction loss 
    """
    return abs(y - yp)
## function to calculate the derivative of activation
def sigmoid_delta(x):
    return x * (1 - x)

###################################################################Neural Network #######################################################################

class Network(nn.Module):
    def __init__(self, n_hidden, lr=0.3):       
        ## initialize tensor variables for weights 
        self.w1 = (-0.1 - 0.1) * torch.rand(145, n_hidden) + 0.1 # weight for hidden layer
        self.w2 = (-0.1 - 0.1) * torch.randn(n_hidden, 1) + 0.1  # weight for output layer

        ## initialize tensor variables for bias terms 
        self.b1 = torch.randn((1, 30)) # bias for hidden layer
        self.b2 = torch.randn((1, 1)) # bias for output layer

        self.learning_rate = lr
    
    def forward_propagation(self, x):
        #convert the input to tensor 
        x = torch.from_numpy(x)
        x = x.reshape(1,145).float()   #2D matrix

        ## activation of hidden layer 
        z1 = torch.mm(x, self.w1) + self.b1
        a1 = sigmoid_activation(z1)
        
        ## activation (output) of final layer 
        z2 = torch.mm(a1, self.w2) + self.b2
        output = sigmoid_activation(z2)
        return a1,output

    def backpropagation(self,x, y): 

        a1,output = self.forward_propagation(x)
        print("target : %s"%(y))
        print("prediction : %s"%(output))

        loss = customLoss(output,y)
        print("the error is %s"%(loss))
        ## compute derivative of error terms
        delta_output = sigmoid_delta(output)
        delta_hidden = sigmoid_delta(a1)

        ## backpass the changes to previous layers 
        d_outp = loss * delta_output
        loss_h = torch.mm(d_outp, self.w2.t())
        d_hidn = loss_h * delta_hidden

        #convert the input to tensor 
        x = torch.from_numpy(x)
        x = x.reshape(1,145).float()   #2D matrix

        # Update the vectors of weights        
        self.w2 += torch.mm(a1.t(), d_outp) * self.learning_rate
        self.w1 += torch.mm(x.t(), d_hidn) * self.learning_rate

        self.b2 += d_outp.sum() * self.learning_rate
        self.b1 += d_hidn.sum() * self.learning_rate 

    def saveParameters(self, model):
        # we will use the PyTorch internal storage functions
        torch.save(model, "NN")

    def loadParameters(self,namefile): 
        torch.load(namefile)

if __name__ == '__main__':
    NN = Network(30)

    x = np.random.choice(2, size = 145)
    np.random.seed(5)
    x2 = np.random.choice(2, size = 145)

    target = NN.forward_propagation(x2)[1]

    print("the vector weight 1 %s" %(NN.w1))
    print("the vector weight 2 %s" %(NN.w2))
    NN.backpropagation(x,target)
    print("the vector weight 2 %s" %(NN.w2))    
    print("the vector weight 1 %s" %(NN.w1))

    NN.saveParameters("NN")

    nn = NN.loadParameters("NN")
    print("the vector weight 2 %s" %(nn.w2))    
    print("the vector weight 1 %s" %(nn.w1))