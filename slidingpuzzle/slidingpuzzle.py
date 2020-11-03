#
# Project 0 for AI: CS 460/660/760
# Complete a sliding puzzle solver using search with heuristics
#
# Check for instances of "TODO" in the starter below and get it working using BFS first.
# Then see what heuristics you can apply from Chapter 3 to make this faster.


import random, copy, queue
import math
import numpy as np

class Board:
    def __init__(self, W):
        # Sets up a WxW board in solved position
        self.W = W
        self.data = []
        self.pos = (0,0)
        next = 0
        for i in range(self.W):
            self.data.append([])
            for j in range(self.W):
                self.data[-1].append(next)
                next += 1
    def __eq__(self, other):
        for i in range(self.W):
            for j in range(self.W):
                if self.data[i][j] != other.data[i][j]: return False
        return True
    def __hash__(self):
        h = 0
        for i in range(self.W):
            for j in range(self.W):
                h *= 3
                h ^= hash(self.data[i][j]);
        return h
    def actions(self):
        i,j = self.pos
        a = frozenset()
        if i > 0: a |= {"up"}
        if i < self.W-1: a |= {"down"}
        if j > 0: a |= {"left"}
        if j < self.W-1: a |= {"right"}
        return a
    def step(self, action):
        # Assuming action is applicable, return successor board
        i0, j0 = self.pos
        i1, j1 = i0, j0
        if action == "up": i1 -= 1
        elif action == "down": i1 += 1
        elif action == "left": j1 -= 1
        elif action == "right": j1 += 1
        nextboard = copy.deepcopy(self)
        nextboard.data[i0][j0] = nextboard.data[i1][j1]
        nextboard.data[i1][j1] = 0
        nextboard.pos = (i1,j1)
        return nextboard
    def goal(self):
        next = 0
        for i in range(self.W):
            for j in range(self.W):
                if self.data[i][j] != next: return False
                next += 1
        return True

    
class State:
    def __init__(self, board, moves, pathcost):
        self.board = board
        self.moves = moves
        self.pathcost = pathcost
    def __eq__(self, other):
        if len(self.moves) != len(other.moves): return False
        for i in range(len(self.moves)):
            if self.moves[i] != other.moves[i]: return False
        return self.board == other.board and self.pathcost == other.pathcost
    def __hash__(self):
        h = 0
        for i in range(len(self.moves)):
            h *= 3
            h ^= hash(self.moves[i])
        return h ^ hash(self.board) ^ hash(self.pathcost)
    def __lt__(self, other):
        return self.eval() < other.eval()
    def step(self, act):
        return State(self.board.step(act), self.moves+[act], self.pathcost+1)
    def successors(self):
        pass # TODO: return a frozenset of all successor states
    def goal(self):
        return self.board.goal()
    def eval(self):
        return self.pathcost

# Potentially useful helper for generating randomly permuted boards using State.step
def randomboard(W, steps = 50, seed = 0):
    random.seed(seed)
    b = Board(W)
    st = State(b, [], 0)
    for step in range(steps):
        acts = sorted(st.board.actions())
        randact = random.sample(acts,1)[0]
        st = st.step(randact)
    return st.board

# heuristics
# will add here rather than making extra files

# support data for h1
comps = []
for i in range(7):
    comps.append(np.arange((i+1) * (i+1)).reshape((i+1, i+1)))
    comps[i][0, 0] = -1
        
# h1 from 103
def h1(board):
    # fetch dimension
    W = board.W
        
    # create a comparison board if necessary
    while len(comps) < W:
        i = len(comps) + 1
        comps.append(np.arange(i * i).reshape((i, i)))
        comps[-1][0, 0] = -1
    
    # do the comparison
    temp = np.array(board.data)
    num_correct = np.sum(np.equal(temp, comps[W - 1]))
    return (W * W) - 1 - num_correct

# h2 from 104
# sum of manhattan distance for each piece
def h2(board):
    # fetch dimension
    W = board.W
    
    dist = 0
    for i in range(W):
        for j in range(W):
            if board.data[i][j]:  # ignore 0
                # calculate x distance
                dist += abs(board.data[i][j] % W - j)

                # calculate y distance
                dist += int(abs(board.data[i][j] // W - i))
                
    return dist

# aggregate heuristic function
# uses the maximum on all heuristics to evaluate a board state
def score(board):
    # just doing this manually since I'm not modularizing 
    heuristics = [h1, h2]
    
    max_score = 0
    for h in heuristics:
        max_score = max(h(board), max_score)
            
    return max_score

# checks for the goal state
def check_goal(board):
    return not h1(board)

def solve(startboard):
    # Create a priority queue for the frontier set
    frontier = queue.PriorityQueue()
    # Create a hashset for already-visited boards
    seenset = set()
    # Add a state for the starting board at pathcost==0
    start = State(startboard, [], 0)
    frontier.put(start)
    
    ctr = 0

    # Loop until the frontier is exhausted
    while not frontier.empty():
        ctr += 1
        if ctr > 10000:
            break
            
        # TODO: Pop highest priority (least) element
        #       Check if it's a solution, or has been already seen
        #       If neither, add all its successors to the frontier
        current = frontier.get()
        
        # terminal condition
        if check_goal(current.board):
            print("Found a {} move solution in {} steps.".format(len(current.moves), ctr))
            return State(current.board, current.moves, len(current.moves))
        
        # state is new
        if not current.board in seenset:
            # add board to hashmap
            seenset.add(current.board)
        
            # iterate through each possible action
            for a in current.board.actions():
                next_board = current.board.step(a)
                
                # ignore boards already evaluated to cut down on queue size
                if not next_board in seenset:
                    
                    # fetch heuristic value of subsequent state
                    action_score = score(next_board)
                    #print(current.moves, a, len(current.moves) + 1 + action_score, action_score)
                    #print(next_board.data)
                    #print(current.pathcost)
                    # build state object, add 1 to cost to count the current move
                    next_state = State(next_board, current.moves + [a], len(current.moves) + 1 + action_score)
                    # add to priority queue
                    frontier.put(next_state)
                
                
        
        # simply do nothing to ignore boards previously seen        
        
    # Oops, no solution found
    return None
        
        
