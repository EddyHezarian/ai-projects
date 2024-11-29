
import math
from collections import deque

class Node:
    def __init__(self, parent=None, value=None, action=None):
        self.parent = parent
        self.value = value
        self.action = action
    def __str__(self):
        if(self.parent): return f"{self.parent}\n{self.action}--{self.value}"
        else: return f"{self.value}"
    def getCounter(self):
        if(self.parent):
            return self.parent.getCounter()+1
        else :
            return 0 

def main():

    target = int(input("enter ypur name >>"))
    frontier = deque()
    explored = set()    
    # Initialize the first node
    initial_node = Node(parent=None, value=4)
    frontier.appendleft(initial_node)
    # Loop 
    while True:
        # Failure condition
        if not frontier:
            print("Failure")
            return 0
        # Choosing the first node (L)
        L = frontier.popleft()
        # Goal test
        if L.value == target:
            print(L)
            print(f'founded number in {L.getCounter()} Steps')
            #show_route(L)
            return 0
        # Add L to the explored  
        # Expand the node
        multipule_value = L.value * 2
        sqrt_value = math.sqrt(L.value)
        floor_value = math.floor(L.value)
        # Add new nodes to the frontier if not already explored
        if multipule_value not in explored:
            frontier.append(Node(value=multipule_value, parent=L, action="X"))
            explored.add(multipule_value)
        if sqrt_value not in explored:
            frontier.append(Node(value=sqrt_value, parent=L, action="sqrt"))
            explored.add(sqrt_value)
        if floor_value not in explored:
            frontier.append(Node(value=floor_value, parent=L, action="floor"))
            explored.add(floor_value)
        
if __name__ == "__main__":
    main()

def showing_rout(L):
    step = 0
    while True :
        step+=1
        print(f"step{step}:{L.value}--{L.action}")
        if(L.parent==None):
           break
        L = L.parent
        
