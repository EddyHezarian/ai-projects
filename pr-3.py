from copy import deepcopy

class MinHeap:
    def __init__(self):
        self.heap = []  

    def push(self, node):
        self.heap.append(node)  
        self._heapify_up(len(self.heap) - 1) 

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()  

        root = self.heap[0] 
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)  
        return root

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2 
        while index > 0 and self.heap[index].f < self.heap[parent_index].f:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def _heapify_down(self, index):
        smallest = index 
        left_child = 2 * index + 1
        right_child = 2 * index + 2

       
        if left_child < len(self.heap) and self.heap[left_child].f < self.heap[smallest].f:
            smallest = left_child

      
        if right_child < len(self.heap) and self.heap[right_child].f < self.heap[smallest].f:
            smallest = right_child

        
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)  # ادامه بازسازی از پایین

    def __len__(self):
        return len(self.heap)  

    def is_empty(self):
        return len(self.heap) == 0 

def is_goal(state):
   stacks = state.stacks

   if not stacks[0]: 
       w1 = sum(stacks[1])
       w2 = sum(stacks[2])
       return w1 == w2
   elif not stacks[1]: 
       w0 = sum(stacks[0])
       w2 = sum(stacks[2])
       return w0 == w2
   elif not stacks[2]:  
       w0 = sum(stacks[0])
       w1 = sum(stacks[1])
       return w0 == w1
   else:
       return False

class State:
   def __init__(self, stacks, g, h, parent=None):
       self.stacks = stacks  
       self.g = g  
       self.h = h  
       self.f = g + h 
       self.parent = parent 

   def __eq__(self, other):
       return self.stacks == other.stacks 

   def __lt__(self, other):
       
        if self.f == other.f:
            return self.g < other.g
        return self.f < other.f

   def __hash__(self):
      
       return hash(str(self.stacks))

def H(stacks):
    sum1 = sum(stacks[0])
    sum2 = sum(stacks[1])
    sum3 = sum(stacks[2])
    diffs = [sum1, sum2, sum3]
    diffs.sort()
    return abs(diffs[1] - diffs[2]) / 2 

def get_neighbors(state):
   neighbors = []
   stacks = state.stacks
   for i in range(3):
       if not stacks[i]:  
           continue
       for j in range(3):
           if i == j:  
               continue
           new_stacks = deepcopy(stacks)  
           weight = new_stacks[i].pop()
           new_stacks[j].append(weight)
           g = state.g + weight 
           h = H(new_stacks) 
           neighbor = State(new_stacks, g, h, parent=state)  
           neighbors.append(neighbor)  
   return neighbors

def reconstruct_path(state):
   path = []
   current = state
   while current:
       path.append(current.stacks)
       current = current.parent
   path.reverse()  
   return path

def a_star_wierd(initial_stacks):
   frontier :MinHeap = MinHeap()
   explore =set()
   initial_h = H(initial_stacks)
   init_node = State(initial_stacks, 0, initial_h)
   frontier.push(init_node)

   while frontier:
       current = frontier.pop()
       if is_goal(current):
           return reconstruct_path(current), current.g
       explore.add(current)
       for neighbor in get_neighbors(current):
            if(neighbor not in explore):
                frontier.push(neighbor)
   return None, None  

def a_star_graph(initial_stacks):
   frontier :MinHeap = MinHeap()
   explore =set()
   initial_h = H(initial_stacks)
   init_node = State(initial_stacks, 0, initial_h)
   frontier.push(init_node)

   while frontier:
       current = frontier.pop()
       if is_goal(current):
           return reconstruct_path(current), current.g
       explore.add(current)
       for neighbor in get_neighbors(current):
            if(neighbor not in explore):
                if(neighbor not in frontier.heap):
                    frontier.push(neighbor)
   return None, None  

def a_star_tree(initial_stacks):
   frontier :MinHeap = MinHeap()
   initial_h = H(initial_stacks)
   init_node = State(initial_stacks, 0, initial_h)
   frontier.push(init_node)
   while frontier:
       current = frontier.pop()
       if is_goal(current):
           return reconstruct_path(current), current.g  
       for neighbor in get_neighbors(current):
            frontier.push(neighbor)
   return None, None  

def read_initial_state(file_path):
   with open(file_path, 'r') as file:
       stacks = [list(map(int, line.strip().split())) for line in file]
       stacks = [stack[::1] for stack in stacks]
   return stacks

initial_state = read_initial_state('weights.txt')
print("Initial State:", initial_state)
print("\n")
path, cost = a_star_graph(initial_state)

if path:
   print("Optimal Path:")
   for step, state in enumerate(path):
       print(f"Step {step}: {state}")
   print("\nTotal Cost:", cost)
else:
   print("No solution found.")


