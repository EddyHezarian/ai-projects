import math
import random

class State:
    def __init__(self, assigns, task_durations, worker_num, access):
        self.assigns = assigns
        self.task_durations = task_durations
        self.access = access
        self.worker_num = worker_num
        self.fitness = self.evaluate(assigns, task_durations, worker_num)

    def get_fitness(self):
        return self.fitness

    def get_random_neighbor(self):
        new_assigns = self.assigns[:]
        index = random.randint(0, len(new_assigns) - 1)
        valid_workers = [i for i in range(len(self.access[index])) if self.access[index][i] == 1]
        new_assigns[index] = random.choice(valid_workers) 
        return State(new_assigns, self.task_durations, self.worker_num, self.access)
    
    def evaluate(self, state, task_times, num_workers):
        worker_times = [0] * num_workers
        for i in range(len(state)):
            worker_times[state[i]] += task_times[i]
        return max(worker_times) - min(worker_times)

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        task_num, worker_num = map(int, file.readline().split())
        
        task_durations = list(map(int, file.readline().split()))
        
        access = []
        for _ in range(task_num):
            access.append(list(map(int, file.readline().split())))
            
    return task_num, worker_num, task_durations, access

def create_initial_state(task_num, worker_num, access, task_durations):
    initial_assigns = []
    for i in range(task_num):
        valid_workers = [j for j in range(worker_num) if access[i][j] == 1]
        initial_assigns.append(random.choice(valid_workers))
    
    return State(initial_assigns, task_durations, worker_num, access)

def first_choice(task_num:int, worker_num:int, task_durations:list, access):
    current = create_initial_state(task_num, worker_num, access, task_durations)

    for _ in range(100000):
        neighbor = current.get_random_neighbor()
        if neighbor.get_fitness() < current.get_fitness():
            current = neighbor
        if current.get_fitness() == 0:
            break
    return current

def golab_hill(task_num, worker_num, task_durations, access):
    limit = 5
    current = create_initial_state(task_num, worker_num, access, task_durations)
    soul = create_initial_state(task_num, worker_num, access, task_durations)
    badStep = 0
    for _ in range(10000000):
        soul = soul.get_random_neighbor()
        if soul.get_fitness() < current.get_fitness():
            current = soul
            badStep=0
        else:
            badStep +=1
            if(badStep > limit):
                soul = current  
                badStep = 0      
    return current

def annealing(task_num, worker_num, task_durations, access):
    current = create_initial_state(task_num, worker_num, access, task_durations)
    best = current
    T = 1000000  
    cooling_rate = 0.999
    while T > 1:
        neighbor = current.get_random_neighbor()
        delta_fitness = neighbor.get_fitness() - current.get_fitness() 
        if delta_fitness < 0 or random.random() < math.exp(-delta_fitness / T):           
            current = neighbor
        if current.get_fitness() < best.get_fitness():
            best = current    
        T *= cooling_rate 
    return best

if __name__ == "__main__":
    task_num, worker_num, task_durations, access = read_data_from_file('tasks.txt')
    
    final_state_first_choice = first_choice(task_num, worker_num, task_durations, access)
    print("\n\n first choice :\n")
    print("Best allocation:", final_state_first_choice.assigns)
    print("Best value (minimized max-min difference):", final_state_first_choice.get_fitness())

    final_state_golab_search = golab_hill(task_num, worker_num, task_durations, access)
    print("\n\n\n golab search : \n")
    print("Best allocation:", final_state_golab_search.assigns)
    print("Best value (minimized max-min difference):", final_state_golab_search.get_fitness())

    final_state_annealing = annealing(task_num , worker_num , task_durations , access)    
    print("\n\n\n annealing :\n")
    print("Best allocation:", final_state_annealing.assigns)
    print("Best value (minimized max-min difference):", final_state_annealing.get_fitness())