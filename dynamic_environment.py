import sys 
import random
import tkinter
random.seed()

#dimension de la grille
width = 25
heigth = 25

class State:
    def __init__(self, obstacles):
        self.environment = [[ 0 for j in range(25)] for i in range(25)]
        for (x,y) in obstacles:
            self.environment[x][y] = 1
        self.ennemies = [(6,6), (12,2),(12,6),(18,6)]
        self.agent = (18,12)
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
        return (self.environment[x][y]==0) and ((x,y)!=self.agent) and not((x,y) in self.ennemies) and self.environment[x][y]!=1
    
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

    def print_grid_terminal(self):
        for i in range(25):
            l = ""
            for j in range(25):
                if (i,j) in self.ennemies:
                    l += "E"
                elif (i,j)==self.agent:
                    l+= "I"
                elif self.environment[i][j]==2:
                    l+="$"
                elif self.environment[i][j] == 1:
                    l+="O"
                else:
                    l+=" "
            print(l)


if __name__ == '__main__':
    
    obstacles = [] 
    obstacles+= [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,19), (0,20), (0,21), (0,22), (0,23), (0,24)]
    obstacles+=[(1,0), (1,24)]
    obstacles+=[(2,0),(2,3),(2,4), (2,8), (2,9), (2,11), (2,12), (2,13), (2,15), (2,16), (2,20), (2,21), (2,24)]
    obstacles+=[(3,0), (3,2), (3,3), (3,4), (3,8), (3,9), (3,11), (3,13), (3,15), (3,16), (3,20), (3,21), (3,22), (3,24)]
    obstacles+=[(4,0), (4,2), (4,3), (4,4), (4,20), (4,21), (4,22), (4,24)]
    obstacles+=[(5,0),(5,24)]
    obstacles+=[(8,2),(8,3), (8,8), (8,9), (8,10), (8,11), (8,13), (8,14), (8,15), (8,16), (8,21), (8,22)]
    obstacles+=[(9,2),(9,3), (9,8), (9,9), (9,10), (9,14), (9,15), (9,16), (9,21), (9,22)]
    obstacles+=[(10,8), (10,9), (10,15), (10,16)]
    obstacles+=[(11,2),(11,3), (11,8), (11,16), (11,21), (11,22)]
    obstacles+=[(12,3), (12,12), (12,22)]
    obstacles+= [(24,0), (24,1), (24,2), (24,3), (24,4), (24,5), (24,19), (24,20), (24,21), (24,22), (24,23), (24,24)]
    obstacles+=[(23,0), (23,24)]
    obstacles+=[(22,0),(22,3),(22,4), (22,8), (22,9), (22,11), (22,12), (22,13), (22,15), (22,16), (22,20), (22,21), (22,24)]
    obstacles+=[(21,0), (21,2), (21,3), (21,4), (21,8), (21,9), (21,11), (21,13), (21,15), (21,16), (21,20), (21,21), (21,22), (21,24)]
    obstacles+=[(20,0), (20,2), (20,3), (20,4), (20,20), (20,21), (20,22), (20,24)]
    obstacles+=[(19,0),(19,24)]
    obstacles+=[(16,2),(16,3), (16,8), (16,9), (16,10), (16,11), (16,13), (16,14), (16,15), (16,16), (16,21), (16,22)]
    obstacles+=[(15,2),(15,3), (15,8), (15,9), (15,10), (15,14), (15,15), (15,16), (15,21), (15,22)]
    obstacles+=[(14,8), (14,9), (14,15), (14,16)]
    obstacles+=[(13,2),(13,3), (13,8), (13,16), (13,21), (13,22)]

    test= State(obstacles)
    test.print_grid_terminal()