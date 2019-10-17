import sys 
import random
import tkinter
random.seed()

#dimension de la grille
width = 25
heigth = 25
print("truc")
class State:
    def __init__(self, obstacles):
        self.environment = [[ 0 for j in range(25)] for i in range(25)]
        for (x,y) in obstacles:
            self.environment[x][y] = 1
        self.ennemies = [(6,6), (12,2),(12,6),(18,6)]
        self.agent = (12,12)
        for i in range(15):
            x = random.randint(0,24)
            y = random.randint(0,24)
            while not self.is_empty(x,y):
                x = random.randint(0,24)
                y = random.randint(0,24)
            self.environment[x][y] =2
        self.energy=40
        return
    
    def is_empty(self,x,y):
        return (self.environment[x][y]==0) and ((x,y)!=self.agent) and not((x,y) in self.ennemies)
    
    def remaining_energy(self):
        return self.energy
    
    def print_grid(self):
        to_print=tkinter.Tk()
        for i in range(25):
            for j in range(25):
                case = tkinter.Canvas(to_print, height=25, width=25,  bg="white").grid(row=j, column=i)
                if (i,j) in self.ennemies:
                    l = tkinter.Label(case, text = "E", borderwidth=1, fg='blue', bg="white").grid(row=j, column=i)
                elif (i,j)==self.agent:
                    l = tkinter.Label(case, text = "A", borderwidth=1, fg='red', bg="white").grid(row=j, column=i)
                elif self.environment[i][j]==2:
                    l = tkinter.Label(case, text = "$", borderwidth=1, fg='green', bg="white").grid(row=j, column=i)
                elif self.environment[i][j] == 1:
                    l= tkinter.Label(case, text="O", borderwidth=1, fg='black', bg="white").grid(row=j, column=i)
                else:
                    l= tkinter.Label(case, text="", borderwidth=1, fg='black', bg="white").grid(row=j, column=i)
        to_print.mainloop()

test= State([(5,3)])
test.print_grid()