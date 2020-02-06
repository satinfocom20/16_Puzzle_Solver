#!/bin/python
'''
Formulation: The 16 puzzle problem can be considered as search problem in which we have to find  the shortest sequence of moves that restores the canonical conguration (on the left above) given an initial board conguration.

Abstraction -

Initial State: Any random arrangement of tiles from 1-16.
Goal State: Tiles arranged in ascending order from 1-16 .

state from initial node, heuristic value of that node and the evaluation value ie. g(s) + h(s)

Successor Function: the player can either (1) choose a row of the puzzle and slide the entire row of tiles left or right, with the left- or right-most tile \wrapping around"
to the other side of the board, or (2) choose a column of the puzzle and slide the entire the column up or down, with the top- or bottom-most tile \wrapping around."

Edge Weights: This is constant since we do not have any cost associated with edge transitions.

Heuristic Function: max of (manhatten distance, misplaced and linear conflict)
 manhatten distance = sum of manhattan distances of each tile from its original position divided by 4 as in each move 4 tiles are moved


A* Algorithm:

1. Create state object for initial_board (State object calculates heuristic and evaluation function in constructor)

2. Add the state to the queue

3. Till the queue is not empty repeat steps below

4. Pop the the element from queue with lowest f(g)

5. Add state to closed

6. Check if goal. If yes print the solution

7. Generate successors for state

8. If successor exists in the closed. compare heuristics and keep the better once.



The challenge we have faced is the running time of the program and number of nodes to be visited to reach the optimal path for board12 which is almost one hour despite it takes few seconds to solve board 2 to board 8.

'''


from queue import PriorityQueue
#from Queue import PriorityQueue
#rom queue import PriorityQueue
from random import randrange, sample
import sys
import string
from datetime import datetime
import numpy as np
import math

# shift a specified row left (1) or right (-1)
from typing import Any


def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)]
    return ( state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print ('%3d %3d %3d %3d' % (row[j:(j+4)]))

# return a list of possible successor states
def successors(state):

    return [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ] 

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)

def Eulicdean(x):
# use Eulicdean distnce  function
    a = np.array(sorted(x))
    b = np.array(x)
    return np.linalg.norm(a-b)/4



def misplaced(x):
# misplaced tiles
    misplaced = 0
    y = sorted(x)
    for i in range(len(x)):
        if y[i]!= x[i]:
            misplaced += 1
    return misplaced/4



def Ncolrow(x):
# number of incorrect rows + number of incorrect columns

    a = np.array(sorted(x)).reshape(4, 4)

    b = np.array(x).reshape(4, 4)

    return 8-(np.sum(np.all(np.equal(a, b), axis=1))) + (np.sum(np.all(np.equal(a, b), axis=0)))




goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
coordinates=[[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[3,3]]


def manhatten(board):

    h = 0
    for i in range(0, 16):

        x = math.fabs(coordinates[i][0] - coordinates[board[i] - 1][0])
        y = math.fabs(coordinates[i][1] - coordinates[board[i] - 1][1])
        h += x + y
    return int(h)/4


def linearConflict(board):

    linear_conflict = 0

    for i in range(0, 16 - 1):
        element = board[i]
        for j in range(i + 1, 16):
            b = board[j]
            if b < element and b != 0:
                should_be = coordinates[element - 1]
                also_should_be = coordinates[b - 1]
                element_current = [i // 4, i % 4]
                board_j_current = [j // 4, j % 4]
                if (should_be == board_j_current and also_should_be == element_current):
                    linear_conflict += 2
    return linear_conflict




# The solver! - using A* right now
def solve(initial_board):
    #fringe = [ (0,initial_board, "",0) ]

    queue = PriorityQueue()


    queue.put((0, initial_board, ""))
    visited = {initial_board: 0}
    while not queue.empty():

        #(f, state, route_so_far, cost) = queue.get()
        (f, state, route_so_far) = queue.get()
        for (succ, move) in successors( state ):

            if is_goal(succ):
                return ( route_so_far + " " + move )
            path = route_so_far + " " + move

            path_cost = len(path)/3

            if succ not in visited or path_cost < visited[succ]:
                visited[succ] = path_cost
                #h = max( , Eulicdean(succ), manhatten(succ),Ncolrow(succ), misplaced(succ), Maxmisplaced(succ) )
                h = max(manhatten(succ), linearConflict(succ),misplaced(succ))
                #h = max(manhatten(succ) ,Eulicdean(succ))
                f = h + path_cost
                queue.put((f, succ, path))


    return False


# test cases
start_state = []
with open(input( "Enter the name of the board: "), 'r') as file:
#with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

if len(start_state) != 16:
    print ("Error: couldn't parse start state file")

print ("Start state: ")


start_time = datetime.now()
print_board(tuple(start_state))

print ("Solving...")
route = solve(tuple(start_state))


print ("Solution found in " + str(len(route)/3) + " moves:" + "\n" + route)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))