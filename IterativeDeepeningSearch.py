#!/usr/bin/env python
# coding: utf-8

# In[28]:


import numpy as np

class Board: 
  
    def __init__(self): 
        
        self.goalMat = np.zeros([3,3],int)
        self.mat = np.zeros([3,3],int)
        self.blanki = None
        self.blankj = None
        self.solution = []
        
        print("Enter 3x3 initial configuration of board ...")
        k = 1
        for i in range(3):
            tmp = list(map(int,input().split()))
            for j in range(3):
                if tmp[j] == 0:
                    self.blanki = i
                    self.blankj = j
                    
                self.mat[i][j] = tmp[j]
                self.goalMat[i][j] = k
                k += 1
                
        self.original = np.copy(self.mat)
        self.goalMat[2][2] = 0

    def moveLeft(self):
        
        val = self.mat[self.blanki][self.blankj-1]
        self.mat[self.blanki][self.blankj] = val
        self.mat[self.blanki][self.blankj-1] = 0
        
        self.blankj -= 1

    def moveRight(self):
        
        val = self.mat[self.blanki][self.blankj+1]
        self.mat[self.blanki][self.blankj] = val
        self.mat[self.blanki][self.blankj+1] = 0
        
        self.blankj += 1
        
    def moveTop(self):
        
        val = self.mat[self.blanki-1][self.blankj]
        self.mat[self.blanki][self.blankj] = val
        self.mat[self.blanki-1][self.blankj] = 0
        
        self.blanki -= 1
        
    def moveBottom(self):
        
        val = self.mat[self.blanki+1][self.blankj]
        self.mat[self.blanki][self.blankj] = val
        self.mat[self.blanki+1][self.blankj] = 0
        
        self.blanki += 1
        
        
    def isGoal(self,currState):
        for i in range(3):
            for j in range(3):
                
                if currState.mat[i][j] != self.goalMat[i][j]:
                    return(False)
        return(True)    
        
    def ShowResult(self):
        self.mat = self.original
        
        print("Original Matrix was ... ")
        for i in range(3):
            for j in range(3):
                if self.mat[i][j] == 0:
                    self.blanki = i
                    self.blankj = j
                print(self.mat[i][j],end = " ")
            print()
        
        print()
        k = 1
        for action in self.solution[::-1]:
            
            print("iteration ",k,end = " ")
            k += 1
            print(" move ",action)
            
            if action == "right":
                self.moveRight()
            elif action == "left":
                self.moveLeft()
            elif action == "top":
                self.moveTop()
            else:
                self.moveBottom()
                
            for i in range(3):
                for j in range(3):
                    print(self.mat[i][j],end = " ")
                print()
            print()
        print("Congratulations solution found ... ")
                    
        
    def DLS(self,maxDepth): 
        
        if self.isGoal(currState): return True

        if maxDepth <= 0 : return False
            
        if self.blanki > 0:  #Top move
                self.moveTop()
                if(self.DLS(maxDepth-1)):
                    self.solution.append("top")
                    return True
                else:
                    self.moveBottom()
        
        if self.blanki < 2:  #Bottom move
            self.moveBottom()
            if(self.DLS(maxDepth-1)):
                self.solution.append("bottom")
                return True
            else:
                self.moveTop()
                
        if self.blankj > 0: #Left move
            self.moveLeft()
            if(self.DLS(maxDepth-1)):
                self.solution.append("left")
                return True
            else:
                self.moveRight()
                
        if self.blankj < 2: #Right move
            self.moveRight()
            if(self.DLS(maxDepth-1)):
                self.solution.append("right")
                return True
            else:
                self.moveLeft()
                
        return False

    def IDDFS(self, maxDepth): 
        
        if self.isValidInput() == False:
            print("Input is not valid ...")
            return False
        
        if self.isSolvable() == False:
            print("no solution possible for this config ...")
            return False
        else:
            print("given problem is solvable")
        
        for i in range(maxDepth): 
            if (self.DLS(i)): 
                return True
        return False

    def isValidInput(self):
        
        temp = np.ones([10],int)
        
        for i in range(3):
            for j in range(3):
                if temp[self.mat[i][j]] > 0:
                    temp[self.mat[i][j]] -= 1
                else:
                    return(False)
        return(True)
    
    def isSolvable(self):
        
        noInversions = 0
        temp = np.copy(self.mat)
        temp = np.resize(temp, (9))
        
        for i in range(9):
            for j in range(i+1,9):
                
                if int(temp[j]) != 0 and int(temp[i]) != 0 and int(temp[j]) < int(temp[i]):
                    noInversions += 1
                    
        print("number of inversion's : ",noInversions)
        # N here is 3, odd value so that problem is solvable if inversions is even
        return noInversions%2 == 0
    


# In[29]:


currState = Board()
if(currState.IDDFS(15)):
    print("Solution Found ...")
    currState.ShowResult()
else:
    print("No solution found ...")


# In[ ]:


1 2 3
5 6 0
7 8 4

1 8 2
0 4 3
7 6 5

