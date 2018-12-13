'''
Environment
'''
graph = {
            'A': ['B', 'D'],
            'B': ['A', 'E'],
            'C': ['D','I'],
            'D': ['A','C','E','G'],
            'E': ['B','D','F'],
            'F': ['E','K'],
            'G': ['D','H','J'],
            'H': ['G'],
            'I': ['C','J'],
            'J': ['G','I','K'],
            'K': ['F','J']
            }   #road-map graph

s = 'A'     #source
d = 'K'     #destination
o = 'I'     #obstacle(junction is under repair, etc.)


traffic_costs = {   ('A', 'B'): 0,
                    ('A', 'D'): 0,
                    ('B', 'E'): 0,
                    ('C', 'D'): 0,
                    ('C', 'I'): 0,
                    ('D', 'E'): 0,
                    ('D', 'G'): 0,
                    ('E', 'F'): 0,
                    ('F', 'K'): 0,
                    ('G', 'H'): 0,
                    ('G', 'J'): 0,
                    ('I', 'J'): 0,
                    ('J', 'K'): 0,
                    }

path_costs = {  ('A', 'B'): 0.04,
                ('A', 'D'): 0.04,
                ('B', 'E'): 0.04,
                ('C', 'D'): 0.04,
                ('C', 'I'): 0.04,
                ('D', 'E'): 0.04,
                ('D', 'G'): 0.04,
                ('E', 'F'): 0.04,
                ('F', 'K'): 0.04,
                ('G', 'H'): 0.04,
                ('G', 'J'): 0.04,
                ('I', 'J'): 0.04,
                ('J', 'K'): 0.04
                }   #Cost = 0.04 + traffic_cost

node_reward = { 'A': 0,
                'B': 0,
                'C': 0,
                'D': 0,
                'E': 0,
                'F': 0,
                'G': 0,
                'H': 0,
                'I': 0,
                'J': 0,
                'K': 0,
                }

def inputNodeDetails():
    global s,d,o
    s = raw_input("Enter Source (A-K):\n")
    d = raw_input("Enter Destination (A-K):\n")
    o = raw_input("Enter Node to be avoided (A-K):\n")

def inputTrafficCosts():
    for x in traffic_costs:
        traffic_costs[x] = raw_input("Enter traffic value for node " + str(x) + " (0 - 0.16)\n")
        path_costs[x] += float(traffic_costs[x])


def travel_reward(junctions):
    for x in path_costs:
        if set(junctions) == set(x):
            return -1 * path_costs[x]

def setup_env():
    inputNodeDetails()
    ch = raw_input("Wish to add your own traffic values? (y/n)\n")
    if ch == 'y' or ch == 'Y':
        inputTrafficCosts()

    node_reward[d] = 1
    node_reward[o] = -1

'''
Navigigation (RL)
'''

alpha = 0.5
gamma = 1

def index(letter):
    return ord(letter)-65

def best(state):
    next_state = 0
    for x in range(11):
        if q_matrix[index(state)][x] > q_matrix[index(state)][next_state]:
            next_state = x
    return chr(65 + next_state)

solution = []

q_matrix = [ #A,  B,  C,  D,  E,  F,  G,  H,  I,  J,  K
            [-1,  0, -1,  0, -1, -1, -1, -1, -1, -1, -1], #A
            [ 0, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1], #B
            [-1, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1], #C
            [ 0, -1,  0, -1,  0, -1, 0, -1, -1,  -1, -1], #D
            [-1,  0, -1,  0, -1,  0, -1, -1, -1, -1, -1], #E
            [-1, -1, -1, -1,  0, -1, -1, -1, -1, -1,  0], #F
            [-1, -1, -1,  0, -1, -1, -1,  0, -1,  0, -1], #G
            [-1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1], #H
            [-1, -1,  0, -1, -1, -1, -1, -1, -1,  0, -1], #I
            [-1, -1, -1, -1, -1, -1,  0, -1,  0, -1,  0], #J
            [-1, -1, -1, -1, -1,  0, -1, -1, -1,  0, -1], #K
            ]
def navig():
    setup_env()
    agent  = s
    path = []
    for i in range(200):
        next_state = best(agent)
        path.append(agent)
        q_matrix[index(agent)][index(next_state)] += alpha * (node_reward[next_state] + travel_reward([agent, next_state]) + gamma * max(q_matrix[index(next_state)]) - q_matrix[index(agent)][index(next_state)])
        agent = next_state
        if next_state == d or next_state == o:
            agent = s
            path.append(next_state)
            solution.append(path)
            path = []


'''
GUI
'''

from Tkinter import *
from time import sleep

coords = {  'I' : [50,50],
            'J' : [200,50],
            'K' : [500,50],
            'G' : [200,200],
            'H' : [350,200],
            'C' : [50,350],
            'D' : [200,350],
            'E' : [350,350],
            'F' : [500,350],
            'A' : [200,500],
            'B' : [350,500]
            }

def mark(alpha, color):
    can.create_oval(coords[alpha][0]-10, coords[alpha][1]-10, coords[alpha][0]+10, coords[alpha][1]+10, fill = color)

def env_setup():
    for x in coords:
        mark(x, "blue")

    for x in graph:
        for y in graph[x]:
            try:
                can.create_line(coords[x][0],coords[x][1],coords[y][0],coords[y][1], width = int(40*path_costs[(x,y)]))
            except:
                pass
    for x in coords:
        canvas_id = can.create_text(coords[x][0]-20, coords[x][1]-20)
        can.itemconfig(canvas_id, text = x)

    mark(d, "green")
    mark(o, "black")


def animate():
    last = s
    for i in range(len(solution)):
        if solution[i]!=solution[i+1]:
            print("Agent is finding the solution...\n")
        else:
            print("Optimal solution found!\n")
            print solution[i]
            for j in range(len(solution[i])-1):
                can.create_line(coords[solution[i][j]][0],coords[solution[i][j]][1],coords[solution[i][j+1]][0],coords[solution[i][j+1]][1], width = 5, fill = "green")
            break
            #exit(1)
        for current in solution[i]:
            mark(last, "blue")
            mark(current, "red")
            can.update()
            last = current
            sleep(0.3)
        print("Path for current iteration: "), solution[i],"\n"
        last = s
        sleep(2)
        env_setup()

navig()
root = Tk()
root.title("RL Path Optimiser")
can = Canvas(root, height = 600, width = 600)
env_setup()

can.pack()
root.after(1000, animate)
root.mainloop()
