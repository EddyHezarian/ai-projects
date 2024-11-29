from collections import * 
from math import floor, sqrt
# node
class   Node : 
    def __init__(self, parent=None, val=None, action=None,dp=None):
        self.parent = parent
        self.val = val
        self.dp = dp
        self.action = action
    def __str__(self):
        if(self.parent): return f"{self.parent}\n{self.action}--{self.val}"
        else: return f"{self.val}"
    def getCounter(self):
        if(self.parent):
            return self.parent.getCounter()+1
        else :
            return 0
def main():
    dp = 0
    front = deque()
    init = Node(val=4,dp=0)
    target = 123
    front.append(init)
    #loop
    while(True):
        while len(front):
            L = front.pop()
            if(L.val == target):
                print(L)
                return 0
            if(L.dp < dp):
                front.append(Node(val=2*L.val,parent= L , action="mul",dp=L.dp+1 ))
                front.append(Node(val=floor(L.val),parent= L , action="fl",dp=L.dp+1 )) 
                front.append(Node(val=sqrt(L.val),parent= L , action="sq",dp=L.dp+1 ))
        dp+=1
        front.append(init)
if __name__ == "__main__":
    main()
