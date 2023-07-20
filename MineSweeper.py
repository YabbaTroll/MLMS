import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class MineSweeperBoard():
    def __init__(self):
        
        self.states = ('uninit','running','won','lost')
        
        self.state = 'uninit'
        
        self.rules = {
            'width' : 10,
            'height' : 10,
            'mines' : 10
        }
        #Raw data of the board represented as an integer matrix
        #Each contained value equals the amount of adjacent mines, or 9 if the cell is a mine
        self.data = None

        #Boolean matrix responsible for determining if any cell should be displayed or not 
        self.mask = None

        #Data matrix but with the cells determined by the mask matrix as visible
        #non-visible cells are null
        self.visb = None
        
        self.pointStart = None
        
        self.neighbors = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x <= self.rules['width'] and
                                   -1 < y <= self.rules['height'] and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 <= self.rules['width']) and
                                   (0 <= y2 <= self.rules['height']))]
        pass
    
    #generates the minefield

    
    def generate(self, w, h, mines) :
        
        self.rules['width'] = w
        self.rules['height'] = h
        self.rules['mines'] = mines
        
        self.data = np.zeros(w*h)
        for i in range(mines):
            self.data[i] = 9

        #Flags starting square, which will be shuffled along with the mines     
        self.data[mines+1] = -1
        np.random.shuffle(self.data)
        
        self.data = np.reshape(self.data,(w,h))
        self.mask = np.ones(w*h)
        self.mask = np.reshape(self.mask,(w,h))   
        
        #Finds mine cells, and increments adjacent cells
        #After completion 
        for idx, x in enumerate(self.data) :
            for idy, y in enumerate(x) :
                if y == -1: 
                    print('Starting point at ({}, {})'.format(idx, idy))
                    self.pointStart = [idx,idy]
                    self.data[idx][idy] = 0
                if y == 9:
                    for i in self.neighbors(idx,idy):
                        try:
                            if self.data[i[0],i[1]] == -1:
                                self.pointStart = ([i[0],i[1]])
                                self.data[i[0],i[1]] = 0
                            if self.data[i[0],i[1]] != 9:
                                self.data[i[0],i[1]] = self.data[i[0],i[1]] + 1
                        except IndexError:
                            pass
                    
                    
        #Automatically selects starting point to avoid unfair first turn losses
        self.cellSelect(self.pointStart[0],self.pointStart[1])
        self.visb = np.ma.MaskedArray(self.data,self.mask)
        
        self.timeStart = datetime.now()   
    
    #Unmasks all connected 0 blocks, and their neighbors
    def floodFill(self, x, y):
        for i in self.neighbors(x,y):
            try :
                if (self.mask[i[0]][i[1]] == 1): #all neighbors that are hidden
                    self.mask[i[0]][i[1]] = 0
                    if (self.data[i[0]][i[1]] == 0): #only floodfills further 0 blocks
                        self.floodFill(i[0],i[1])
                        pass
            except IndexError :
                pass
    
    #Selects square, returns 1 if it was a mine, floodfills if 0, reveals single square if anything else
    def cellSelect(self, x, y):
        
        print('Selected {}'.format([x,y])) 
        if (self.data[x][y] == 9) :
            print('Oh no, it was a mine D:')
        if (self.data[x][y] == 0) :
            self.floodFill(x,y)
        self.mask[x][y] = 0
        self.visb = np.ma.MaskedArray(self.data,self.mask)
        pass

    ax = None
    #Returns a matplotlib plot of the current visible state of the board
    def getBoard(self):
        
        figure = plt.figure()
        ax = figure.add_subplot()
        
        mesh = plt.pcolormesh(np.transpose(self.visb),cmap='viridis',vmin=0,vmax=9)
        norm = mpl.colors.Normalize(vmin =0,vmax =9)
        
        for idx, x in enumerate(self.visb) :
            for idy, y in enumerate(x) :
                if y!=0 and y!= 9:
                    
                    color = np.subtract([1,1,1,2.0],list(mesh.get_cmap()(norm(self.data[idx][idy]))))
                    plt.annotate(xy=[idx,idy],text=int(y),textcoords='data',xytext=[idx+.25,idy+.25], color = color)

        circ = plt.Circle(xy=(self.pointStart[0]+.5,self.pointStart[1]+.5),radius=.4,fill =False, ec = 'white') 
        ax.add_artist(circ)
        
        ax.set(xlim = (0,self.rules['width']), xticks=np.arange(0,self.rules['width']+1, 1),
            ylim = (0,self.rules['height']), yticks=np.arange(0,self.rules['height']+1, 1))

        ax.set_aspect('equal')

        plt.grid(which='major') 
        
        
        return figure
        
    #Updates the board from the getBoard() function
    def updateBoard(self):
        global ax
        plt.sca()

        for idx, x in enumerate(self.visb) :
            for idy, y in enumerate(x) :
                if y!=0 and y!= 9:
                    
                    norm = mpl.colors.Normalize(vmin =0,vmax =9)
                    mesh = plt.pcolormesh(np.transpose(self.visb),cmap='viridis',vmin=0,vmax=9)
                    color = np.subtract([1,1,1,2.0],list(mesh.get_cmap()(norm(self.data[idx][idy]))))
                    plt.annotate(xy=[idx,idy],text=int(y),textcoords='data',xytext=[idx+.25,idy+.25], color = color)
        pass    
