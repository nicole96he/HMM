import numpy as np

class filter:
    '''
    Initialize all needed information.
    '''
    def __init__(self, sensors, maze, colors):
        self.sensors = sensors #  a list
        self.maze = maze # a maze stored in list, includes walls and floor information
        self.loc_color = colors # colors of each location of the maze
        self.walls = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
               if self.maze[i][j] == '#':
                   self.walls.append([i,j])


    '''
    Purpose: Calculate distribution using filtering method.
    Args: all information from initialization.
    Return: distribution
    '''
    def markov_filter(self):
        distributions = []
        O = self.sensor_model() # call sensor_model to get observation model matrix
        T = self.transition_model() # call transition model to get T value
        T_T = T.transpose() #transpose T
        O_0 = np.mat(O[0]) #red
        O_1 = np.mat(O[1]) #green
        O_2 = np.mat(O[2]) #yellow
        O_3 = np.mat(O[3]) #blue
        possible = 1.0 / (16 - len(self.walls)) # Initial possibility of each location is same
        ini = [[possible] for i in range(16-len(self.walls))] # store in a 7*1 list
        f_pre = np.mat(ini) # transfer list to matrix

        for i in self.sensors: #do loop step by step
            if i=='  red ':
                f = np.dot(np.dot(O_0, T_T), f_pre)
            elif i==' green':
                f = np.dot(np.dot(O_1, T_T), f_pre)
            elif i=='yellow':
                f = np.dot(np.dot(O_2, T_T), f_pre)
            else:
                f = np.dot(np.dot(O_3, T_T), f_pre)
            f1 = np.reshape(f,len(self.loc_color)) # change f from 1*7 to 7*1
            dis = self.normalize(f1) # normalize distribution
            distributions.append(dis)
            f_pre = f
        return distributions

    def transition_model(self):
        t_list = []
        for i in range(16):
            l = [0.00]*(16-len(self.walls))
            ix = i // 4
            iy = i - ix*4
            a = 0.00 # a is used to count the times of robot staying in current location.
            index = -1
            stay = 0
            if [ix,iy] in self.walls:
                continue
            for j in range(16):
                jx = j // 4
                jy = j - jx*4
                if [jx,jy] in self.walls:
                    continue
                else:
                    index += 1
                    if jx == (ix-1) and jy == iy:
                        l[index] = 0.25
                        a += 1
                    if jx == (ix + 1) and jy == iy:
                        l[index] = 0.25
                        a += 1
                    if jx == ix and jy == (iy-1):
                        l[index] = 0.25
                        a += 1
                    if jx == ix and jy == (iy+1):
                        l[index] = 0.25
                        a += 1
                    if i == j:
                        stay = index

            l[stay] = (4-a)*0.25
            t_list.append(l)
        T = np.mat(t_list)

        return T


    def sensor_model(self):
        O = []
        red = []
        green = []
        yellow = []
        blue = []
        for i in range(16):
            ix = i // 4
            iy = i - ix * 4
            if self.maze[ix][iy] == '#':
                continue
            redsub = [0.00]*(16-len(self.walls))
            greensub = [0.00]*(16-len(self.walls))
            yellowsub = [0.00]*(16-len(self.walls))
            bluesub = [0.00]*(16-len(self.walls))
            index = -1
            for j in range(16):
                jx = j // 4
                jy = j - jx * 4
                if self.maze[jx][jy] == '#':
                    continue
                index += 1
                if ix == jx and iy == jy:
                    if self.loc_color[(jx,jy)] == '   red  ':
                        redsub[index] = 0.88
                        greensub[index] = 0.04
                        yellowsub[index] = 0.04
                        bluesub[index] = 0.04
                    elif self.loc_color[(jx, jy)] == '  green ':
                        redsub[index] = 0.04
                        greensub[index] = 0.88
                        yellowsub[index] = 0.04
                        bluesub[index] = 0.04
                    elif self.loc_color[(jx, jy)] == ' yellow ':
                        redsub[index] = 0.04
                        greensub[index] = 0.04
                        yellowsub[index] = 0.88
                        bluesub[index] = 0.04
                    elif self.loc_color[(jx, jy)] == '  blue  ':
                        redsub[index] = 0.04
                        greensub[index] = 0.04
                        yellowsub[index] = 0.04
                        bluesub[index] = 0.88
            red.append(redsub)
            green.append(greensub)
            yellow.append(yellowsub)
            blue.append(bluesub)

        O.append(red)
        O.append(green)
        O.append(yellow)
        O.append(blue)
        return O

    def normalize(self,f):
        a = f/np.sum(f,axis=1)
        return a

