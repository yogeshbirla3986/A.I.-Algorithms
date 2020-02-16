#!/usr/bin/env python
# coding: utf-8

# In[25]:


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


    def Astar(self,obj,fLimit): 
        
        AstarOpenQueue = []
        AstartCloseQueue = self.ClosedQueue+[]
        temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal,obj.hVal)
        self.AstarPush(AstarOpenQueue,AstartCloseQueue,temp)
        
        while(len(AstarOpenQueue) != 0):
            
            obj = self.getMin(AstarOpenQueue)
            AstartCloseQueue.append(obj.state)
            
            self.ShowResult(obj)
            
            if self.isGoal(obj.mat):
                return True
            
            if obj.gVal+obj.hVal > fLimit:
                return(obj.gVal+obj.hVal)

            if obj.blanki > 0:  #can move Top 
                obj.moveTop()
                
                hVal = self.getValue(obj.mat)
                temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                self.AstarPush(AstarOpenQueue,AstartCloseQueue,temp)

                obj.moveBottom()

                
            if obj.blanki < 2:  #Can move Bottom
                obj.moveBottom()

                hVal = self.getValue(obj.mat)
                temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                self.AstarPush(AstarOpenQueue,AstartCloseQueue,temp)

                obj.moveTop()

            if obj.blankj > 0: #Can move Left
                obj.moveLeft()
                
                hVal = self.getValue(obj.mat)
                temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                self.AstarPush(AstarOpenQueue,AstartCloseQueue,temp)
                
                obj.moveRight()

            if obj.blankj < 2: #Can move Right
                obj.moveRight()

                hVal = self.getValue(obj.mat)
                temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                self.AstarPush(AstarOpenQueue,AstartCloseQueue,temp)

                obj.moveLeft()
            
                

    def RBFS(self,maxDepth,gVal):
        
        obj = Node(self.mat,self.blanki,self.blankj,gVal,gVal)
        self.PushInGlobalQueue(obj)
        
        while(len(self.globalQueue) != 0 and maxDepth > 0):
            
            maxDepth -= 1
            
            temp = self.getMinimumCostNode()
            obj = temp[0]
            fmin = temp[1]
            
            self.ShowResult(obj)
            
            if self.isGoal(obj.mat):
                return True
            elif fmin == float('inf'):
                
                if obj.blanki > 0:
                    
                    obj.moveTop()
                    hVal = self.getValue(obj.mat)
                    temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                    self.PushInGlobalQueue(temp)
                    obj.moveBottom()
                    
                if obj.blankj > 0:
                    
                    obj.moveLeft()
                    hVal = self.getValue(obj.mat)
                    temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                    self.PushInGlobalQueue(temp)
                    obj.moveRight()
                    
                if obj.blanki < 2:
                    
                    obj.moveBottom()
                    hVal = self.getValue(obj.mat)
                    temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                    self.PushInGlobalQueue(temp)
                    obj.moveTop()
                    
                if obj.blankj < 2:
                    
                    obj.moveRight()
                    hVal = self.getValue(obj.mat)
                    temp = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal+1,hVal)
                    self.PushInGlobalQueue(temp)
                    obj.moveLeft()
            else:
                print("--------------Starting Astart--------------------")
                print()
                store_globalQueue = self.globalQueue
                store_ClosedQueue = self.ClosedQueue
                store_node = Node(obj.mat,obj.blanki,obj.blankj,obj.gVal,obj.hVal,obj.state)
                
                newFVal = self.Astar(obj,fmin)
                obj = store_node
                
                if newFVal == True:
                    return True
                else:
                    
                    obj.FVal = newFVal
                    print("Atar comes back with fVal ",obj.FVal)
                    self.globalQueue = store_globalQueue
                    self.ClosedQueue = store_ClosedQueue
                    self.globalQueue.append(obj)
                    print("-----------------End of Astar-----------------")

                    
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
        
        temp.FVal = temp.gVal + temp.hVal
        self.globalQueue.append(temp)
        return(True)
           
        
    def AstarPush(self,AstarOpenQueue,AstarClosedQueue,temp):
        
        if temp.state == None:
            temp.setState()
            
        length1 = len(AstarClosedQueue)
        
        for i in range(length1):
            
            if AstarClosedQueue[i] == temp.state :
                
                print("This configuration is found in Closed Queue ...")
                return(False)
            
            
        length2 = len(AstarOpenQueue)
        
        for i in range(length2):
            
            if AstarOpenQueue[i].state == temp.state:
                
                tempFVal = temp.gVal + temp.hVal
                queueFVal = AstarOpenQueue[i].gVal + AstarOpenQueue[i].hVal
                
                if tempFVal < queueFVal :
                    
                    AstarOpenQueue.gVal = temp.gVal
                    AstarOpenQueue.hVal = temp.hVal
                    print("This configuration is found in Opend list , minimized Value to",[queueFVal,tempFVal])
                    
                else:
                    
                    print("This configuration is found in Opend list , cannot minimized ",[queueFVal,tempFVal])
                
                return(False)
        
        AstarOpenQueue.append(temp)
        return(True)
            
        
    def getMin(self,AstarOpenQueue):
        
        length1 = len(AstarOpenQueue)
        minF = float('inf')
        index = None
        
        print(" getMin queue size if --> ",length1)
        
        for i in range(length1):
            
            tempF = AstarOpenQueue[i].gVal + AstarOpenQueue[i].hVal
            print(tempF,end="<->")
            if tempF < minF:
                minF = tempF
                index = i
        
        obj = AstarOpenQueue[index]
        AstarOpenQueue.remove(obj)
        print()
        print("selected ",obj.gVal+obj.hVal)
        print()
        return(obj)
    
    
    def getMinimumCostNode(self):
        
        length1 = len(self.globalQueue)
        minF = float('inf')
        index = None
        
        print(" getMin queue size if --> ",length1)
        
        for i in range(length1):
            
            if self.globalQueue[i].FVal == None:
                self.globalQueue[i].FVal = self.globalQueue[i].gVal + self.globalQueue[i].hVal
                
            print(self.globalQueue[i].FVal,end="<->")
            if self.globalQueue[i].FVal < minF:
                minF = self.globalQueue[i].FVal
                index = i
                
        SecondMin = float('inf')
        for j in range(length1):
            
            if self.globalQueue[j].FVal < SecondMin and index != j:
                SecondMin = self.globalQueue[j].FVal
        
        
        obj = self.globalQueue[index]
        self.globalQueue.remove(obj)
        self.ClosedQueue.append(obj)
        print()
        print("selected ",obj.gVal+obj.hVal)
        print()
        return([obj,SecondMin])
    
    
    def getValue(self,mat):
        
        Hval = 0
        for i in range(3):
            for j in range(3):
                Hval += abs(mat[i][j] - self.goalMat[i][j])
        
        return(Hval)
        
    def gettingStarted(self, maxDepth): 
        
        if self.isValidInput() == False:
            print("Input is not valid ...")
            return(False)
        else:
            return self.RBFS(maxDepth,0)

    def isValidInput(self):
        
        temp = np.ones([10],int)
        
        for i in range(3):
            for j in range(3):
                if temp[self.mat[i][j]] > 0:
                    temp[self.mat[i][j]] -= 1
                else:
                    return(False)
        return(True)
    


# In[26]:


class Node():
    
    def __init__(self,mat,blanki,blankj,gVal,hVal,state=None):
        
        self.mat = np.copy(mat)
        self.blanki = blanki
        self.blankj = blankj
        self.gVal = gVal
        self.hVal = hVal
        self.FVal = None
        self.state = state
        
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


# In[30]:


currState = Board()

if(currState.gettingStarted(1000)):
    print("Congatulations solution found ... ")
else:
    print("No solution found ...")


# In[ ]:


1 2 3
5 6 0
7 8 4


# In[ ]:




