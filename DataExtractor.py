import MineSweeper as ms
import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt

import sys
import json


# Create board
# Scan border regions
# Extract 3x3 or 5x5 area around each square in border
# Recreate board

# Should return all unknown blocks that border a known block 
# Return list of blocks that touch 0 that arent 0?
# maybe make all border blocks use actual val?
# List of tuples?

# Make mask where cell != 0 and at least 1 neighbor = 0
# another mask where cell isnt in first mask, has neighbor in first mask, where neighbor != 0 

def getNeighbors(x,y):
    neighbors = []
    for a in range(x-1,x+2):
        for b in range(y-1,y+2):
            if (a != x or b != y):
                neighbors.append((a,b))
            
    return neighbors

# Gets a list of the coordinates of all the zero cells in the current board
def getZeroes(board):
    
    zeroArray = []
    
    for ix, x, in enumerate(board):
        for iy, y in enumerate(x):
            
            if (y == 0):
                zeroArray.append((ix,iy))
    
    return (zeroArray) 

# Creates a boolean matrix of the board where that shows which cells are zero
def getZeroCells(board):
    zeroCells = np.zeros(board.shape)
    for i in getZeroes(board):
        zeroCells[i[0]][i[1]] = 1
    return zeroCells
    pass       
    
# Gets cells are adjacent to a zero cell, but arent a zero cell themselves
def getBorderCells(board, zeros):
    
    borderCells = np.zeros(board.shape)
    
    for ix, x, in enumerate(borderCells):
        for iy, y in enumerate(x):
            if (zeros[ix][iy] != 1) :
                for i in getNeighbors(ix,iy):
                    if (i[0] in range(board.shape[0]) and i[1] in range(board.shape[1]))  :
                        if (zeros[i[0]][i[1]] == 1 ):
                            #print('zeros{} = 1 so borders{} = 1'.format((i[0],i[1]),(ix,iy)))
                            borderCells[ix][iy] = 1
                            break
                            
    return borderCells

# Gets cells that border the cells in getBorderCells that arent zero cells
# Should always return masked cells
def getBorderBorders(borders, data):
    
    testCells = np.zeros(data.shape)
    testCellArray = []
    
    for ix, x, in enumerate(borders):
        for iy, y in enumerate(x):
            for i in getNeighbors(ix,iy):
                try:
                    if (data[i[0]][i[1]] != 0 and borders[i[0]][i[1]] != 1):
                        testCells[i[0]][i[1]] = 1
                        testCellArray.append((i[0],i[1]))
                except :
                    pass
    return testCells
    

# Returns visible data from square area of board
# Non-visible cells are stored as -1, out of bounds cells are stored as -2
def getCellSquares(board, x, y, size) :
    
    squares = []
    
    for a in range(y-size,y+size+1):
        for b in range(x-size,x+size+1):
        
            if a in range(board.shape[0]) and b in range(board.shape[1]):
                
                if board[a][b] not in range(9):
                    squares.append(-1)
                else:
                    squares.append(int(board[a][b]))
            else:
                squares.append(-2)
            
   
    return squares

# Returns data from getCellSquares along with a boolean representing whether or not the center cell is a mine or not 
def getMLinput(board, x, y, size):
    mine = 0
    if board.data[x][y] == 9:
        mine = 1
    
    inp = getCellSquares(board, x, y, size)   
    inp.append(mine) 
    
    return inp
    
# Returns array coordinate labels of squares
def getCellLabels(size) :
    labels = []
    for a in range(-size,size+1):
        for b in range(-size,size+1):
            labels.append('({0:{1}}, {2:{3}})'.format(b, '+' if b else '', a, '+' if a else ''))
    labels.append('IsMine')
    return tuple(labels)
    

class boardTest:
    def __init__(self, x, y, mines):
        self.board = ms.MineSweeperBoard()
        self.board.generate(x,y,mines)
       
        
        self.zeros = getZeroCells(self.board.data)
        self.bords = getBorderCells(self.board.data, self.zeros)
        self.tests = getBorderBorders(self.bords,self.board.data)
        self.maskd = ma.masked_array(self.board.data, mask = self.tests)
    
    def showMask(self):
        plt.pcolormesh(np.transpose(self.maskd),cmap='viridis',vmin=0,vmax=9)
        plt.show()
        
    def showBoard(self):
        plt.pcolormesh(np.transpose(self.board.data),cmap='viridis',vmin=0,vmax=9)
    
        for idx, x in enumerate(self.board.data) :
            for idy, y in enumerate(x) :
                
                label = ''
                
                if (self.zeros[idx][idy] == 1) :
                    label += '0'
                    
                if (self.bords[idx][idy] == 1) :
                    label += 'B'
                
                if (self.tests[idx][idy] == 1) :
                    label += 'T'
                    
                #if (self.masks[idx][idy] == 1) :
                #    label += 'M'
                
                plt.annotate(xy=[idx,idy],text=label,textcoords='data',xytext=[idx+.25,idy+.25])
        
        plt.show()

outputDict = {
    'labels' : [],
    'data' : []
}        

# Counter to keep track of how many inputs are in the output dict before stopping
datums = 0

#radius of stuff
kernalSize = 3

outputDict['labels'] = getCellLabels(kernalSize)

def cycle():
    bt0= boardTest(16,16,40)
    msb = bt0.board
    
    #print('data : \n{}'.format(msb.data))

    #print(msb.data)
    
    zeroCells = getZeroCells(msb.data)
    
    bordCells = getBorderCells(msb.data,zeroCells)
    #print('bord : \n{}'.format(bordCells))
    
    testCells = getBorderBorders(bordCells,msb.data)
    
    for ix, x, in enumerate(testCells):
        for iy, y in enumerate(x):
            
            if (y == 1):
                #print((ix,iy))
                #print( getMLinput(bt0.maskd,ix,iy,1) )
                outputDict['data'].append(getMLinput(bt0.maskd,ix,iy,kernalSize))
                
    
    

#while (len(outputDict['data']) < 1000):
#    cycle()
#    print(len(outputDict['data']))




#with open("results3.json", "w") as outfile:
#    json.dump(outputDict, outfile)
#print(outputDict)



#while (True) :
    #cycle()
    #bt0 = boardTest(16,16,40)
    #bt0.showBoard()
    #bt0.showMask()
    
    #bordCells = getBorderCells(bt0.data)
    #print('bord : \n{}'.format(bordCells))
    
    #testCells = getBorderBorders(bordCells,bt0.data)
    #print('test : \n{}'.format(testCells))
    
    #for idx, x in enumerate(bt0.maskd) :
    #    for idy, y in enumerate(x) :
    #        print(y)
    
#    pass 