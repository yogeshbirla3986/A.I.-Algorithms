#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

class Board:
        
    def __init__(self): 
        
        self.globalQueue = []
        self.goalMat = np.zeros([3,3],int)
        self.mat = np.zeros([3,3],int)
        self.blanki = None
        self.blankj = None
        self.solution = []
        self.state = ""
        self.ClosedQueue = []
       
        k = 1
        for i in range(3):
            tmp = list(map(int,input().split()))
            for j in range(3):
                if tmp[j] == 0:
                    self.blanki = i
                    self.blankj = j
                    
                self.mat[i][j] = tmp[j]
                self.state += str(self.mat[i][j])
                
                self.goalMat[i][j] = k
                k += 1
                
        self.original = np.copy(self.mat)
        self.goalMat[2][2] = 0
        print("Stating Execution ... ")

        
        
    def isGoal(self,mat):
        for i in range(3):
            for j in range(3):
                
                if mat[i][j] != self.goalMat[i][j]:
                    return(False)
        return(True)
    
    def ShowResult(self,obj):
        
        for i in range(3):
            for j in range(3):
                print(obj.mat[i][j],end = " ")
            print()
        print("Blank Position ",obj.blanki,obj.blankj)
        print()
        
    def Astar(self,maxDepth,gVal): 
        
        obj = Node(self.mat,self.blanki,self.blankj,gVal,gVal)
        self.PushInGlobalQueue(obj)
        
        while(len(self.globalQueue) != 0 and maxDepth > 0):
            
            maxDepth -= 1
            
            obj = self.getMinimumCostNode()
            self.ClosedQueue.append(obj.state)
            
            self.ShowResult(obj)
            
            if self.isGoal(obj.mat):
                return True

            if obj.blanki > 0:  #can move Top 
                obj.moveTop()
                
                hVal = self.getValue(obj.mat)
                temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                self.PushInGlobalQueue(temp)

                obj.moveBottom()

                
            if obj.blanki < 2:  #Can move Bottom
                obj.moveBottom()

                hVal = self.getValue(obj.mat)
                temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                self.PushInGlobalQueue(temp)

                obj.moveTop()

            if obj.blankj > 0: #Can move Left
                obj.moveLeft()
                
                hVal = self.getValue(obj.mat)
                temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                self.PushInGlobalQueue(temp)

                obj.moveRight()

            if obj.blankj < 2: #Can move Right
                obj.moveRight()

                hVal = self.getValue(obj.mat)
                temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                self.PushInGlobalQueue(temp)

                obj.moveLeft()
            

    def PushInGlobalQueue(self,temp):
        
        if temp.state == None:
            temp.setState()
            
        length1 = len(self.ClosedQueue)
        
        for i in range(length1):
            
            if self.ClosedQueue[i] == temp.state :
                
                print("This configuration is found in Closed Queue ...")
                return(False)
            
            
        length2 = len(self.globalQueue)
        
        for i in range(length2):
            
            if self.globalQueue[i].state == temp.state:
                
                tempFVal = temp.gVal + temp.hVal
                queueFVal = self.globalQueue[i].gVal + self.globalQueue[i].hVal
                
                if tempFVal < queueFVal :
                    
                    self.globalQueue[i].gVal = temp.gVal
                    self.globalQueue[i].hVal = temp.hVal
                    print("This configuration is found in Opend list , minimized Value to",[queueFVal,tempFVal])
                    
                else:
                    
                    print("This configuration is found in Opend list , cannot minimized ",[queueFVal,tempFVal])
                
                return(False)
        
        self.globalQueue.append(temp)
        return(True)
            
        
    def getMinimumCostNode(self):
        
        length1 = len(self.globalQueue)
        minF = float('inf')
        index = None
        
        print(" getMin queue size if --> ",length1)
        
        for i in range(length1):
            
            tempF = self.globalQueue[i].gVal + self.globalQueue[i].hVal
            print(tempF,end="<->")
            if tempF < minF:
                minF = tempF
                index = i
        
        obj = self.globalQueue[index]
        self.globalQueue.remove(obj)
        print()
        print("selected ",obj.gVal+obj.hVal)
        print()
        return(obj)
    
    
    def getValue(self,mat):
        
        Hval = 0
        # Gval will be same for all the nodes ...
        for i in range(3):
            for j in range(3):
                Hval += abs(mat[i][j] - self.goalMat[i][j])
        
        return(Hval)
        
    def gettingStarted(self, maxDepth): 
        
        if self.isValidInput() == False:
            print("Input is not valid ...")
            return(False)
        elif self.isSolvable() == False:
            print("given problem is unsolvable ")
            return False
        else:
            print("problem is solvable ")
            return self.Astar(maxDepth,0)

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
    


# In[2]:


class Node():
    
    def __init__(self,mat,blanki,blankj,gVal,hVal):
        
        self.mat = np.copy(mat)
        self.blanki = blanki
        self.blankj = blankj
        self.gVal = gVal
        self.hVal = hVal
        self.state = None
        
    def setState(self):
        
        self.state = ""
        
        for i in range(3):
            for j in range(3):
                self.state += str(self.mat[i][j])
                

    def moveTop(self):
        
        val = self.mat[self.blanki-1][self.blankj]
        self.mat[self.blanki][self.blankj] = val
        self.mat[self.blanki-1][self.blankj] = 0
        
        self.blanki -= 1

        
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
        
    def moveBottom(self):
        
        val = self.mat[self.blanki+1][self.blankj]
        self.mat[self.blanki][self.blankj] = val
        self.mat[self.blanki+1][self.blankj] = 0
        
        self.blanki += 1   


# 
# 

# In[3]:


currState = Board()

if(currState.gettingStarted(2000)):
    print("Congatulations solution found ... ")
else:
    print("No solution found ...")


# In[ ]:


Test cases :
    
1 2 3
5 6 0
7 8 4

1 8 2
0 4 3
7 6 5

1 2 0
5 6 8
4 3 7

0 1 2
3 4 5
6 7 8


# In[ ]:




