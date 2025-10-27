from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

from queue import PriorityQueue
import itertools

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    
    # returninig an empty list in case if the goal is the initial state
    if problem.is_goal(initial_state):          
            return []               
        
    visited = set()
    frontier = deque()
    
    # In order to track the actions' path taken by the search, i need with each state to save it's current actions list                        
    # Each frontier entry is (state, actions_done_so_far)
    
    frontier.append((initial_state, []))
    
    while frontier:
                
        # FIFO queue
        curr_state, curr_actions = frontier.popleft()      
        
        if curr_state in visited:
            continue
        
        # Mark state as visited
        visited.add(curr_state)             
        
        
        for action in problem.get_actions(curr_state):
            new_state = problem.get_successor(curr_state, action)

            # Don't process previously visited states
            if new_state in visited:    
                continue                    
            
            # append the last action to actions_list to get the  new_actions_list 
            new_actions = curr_actions + [action]  
            
            # Early check of goal to decrease the complexity from O(b^(d+1)) to O(b^(d))
            if problem.is_goal(new_state):
                return new_actions               

            # new state that has not visited before will be appended in the frontier
            # with all actions taken to get the this state
            frontier.append((new_state, new_actions))     
    return None

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution: 
    
    counter = itertools.count()   
    # queue of the current state and the actions done so far
    # priority is the accumelated cost to reach to the current node
    frontier = PriorityQueue()
    frontier.put((0,next(counter),initial_state, []))
    
    visited = set()
    
    while not frontier.empty():        
        curr_cost, _ , curr_state, curr_actions = frontier.get()
        
        if problem.is_goal(curr_state):
            return curr_actions
        
        if curr_state in visited:
            continue
        
        visited.add(curr_state)
        
        for action in problem.get_actions(curr_state):
            new_state = problem.get_successor(curr_state, action)
            
            if new_state in visited:
                continue
            
            new_actions = curr_actions + [action]
            action_cost = problem.get_cost(curr_state, action)
            frontier.put((curr_cost + action_cost, next(counter), new_state, new_actions))
            
    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    NotImplemented()