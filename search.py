from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

from queue import PriorityQueue
import itertools
import heapq

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
    """
    Depth-dirst search explore by going deep for each path before backtrack
    keep track of visited to avoid loops and returns actions to our goal
    """
    # create shared variables so they exist in all recursive calls
    if not hasattr(DepthFirstSearch, "visited"):
        DepthFirstSearch.visited = set()
    if not hasattr(DepthFirstSearch, "path"):
        DepthFirstSearch.path = []
    current = initial_state
    #stop searching if we have reached our goal
    if problem.is_goal(current):
        result_path = DepthFirstSearch.path.copy()
        #clean up static variables before return
        DepthFirstSearch.visited.clear()
        DepthFirstSearch.path.clear()
        return result_path
    # mark the current state to avoid revisit
    DepthFirstSearch.visited.add(current)
    # try every possible action from this state
    for action in problem.get_actions(current):
        next_state = problem.get_successor(current, action)
        # skip states we hve already explored
        if next_state in DepthFirstSearch.visited:
            continue
        # save this step in our current path
        DepthFirstSearch.path.append(action)
        # go deeper to the next state
        result = DepthFirstSearch(problem, next_state)
        # if we found a valid path return it
        if result is not None:
            return result
        # otherwise undo this step -> backtrack
        DepthFirstSearch.path.pop()
    # If we are back to the start and found nothing then we do reset everything
    if current == problem.get_initial_state():
        DepthFirstSearch.visited.clear()
        DepthFirstSearch.path.clear()
    #no path found
    return None

    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution: 
    
    # Counter passed to frontier in order to prioritize
    # early-enqueued states in case of draw in cost
    counter = itertools.count()   
    
    # queue of the current state and the actions done so far
    # priority is the accumelated cost to reach to the current node
    frontier = PriorityQueue()
    frontier.put((0,next(counter),initial_state, []))
    
    # store visited states to apply graph-search
    visited = set()
    
    while not frontier.empty():        
        curr_cost, _ , curr_state, curr_actions = frontier.get()
        
        # Here goal check cannot be before adding to the frontier as in bfs,
        # because we could get to the same state from different path with lower cost
        # which will be visited before the higher-cost one
        if problem.is_goal(curr_state):
            return curr_actions
        
        # don't process previously visited states
        if curr_state in visited:
            continue
        
        # Marking state as visited
        visited.add(curr_state)
        
        # Expand state
        for action in problem.get_actions(curr_state):
            new_state = problem.get_successor(curr_state, action)
            
            if new_state in visited:
                continue
            
            new_actions = curr_actions + [action]
            
            # The new here is the cost calculation, as the UCS proritize on accumelated cost
            # from the path beggining till reaching the current state
            action_cost = problem.get_cost(curr_state, action)
            frontier.put((curr_cost + action_cost, next(counter), new_state, new_actions))
            
    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    """
    A* search -> combines the actual cost until now with heuristic estimate to choose the most good path
    expands nodes based on the lowest estimated total cost f = g + h
    """
    # if start is our goal
    if problem.is_goal(initial_state):
        return []
    #pq store tuples of (f_cost, order, current_state, path_taken, g_cost )
    frontier = []
    counter = 0
    heapq.heappush(frontier, (0, counter, initial_state, [], 0))
    explored = set()
    while frontier:
        # pick node with the lowest tot. estimated cost
        _,_,current, current_path, current_cost = heapq.heappop(frontier)
        # if reached goal return actions
        if problem.is_goal(current):
            return current_path
        # skip visited 
        if current in explored:
            continue
        #mark state as visited
        explored.add(current)
        #check all possible moves from the curr state
        for action in problem.get_actions(current):
            next_state = problem.get_successor(current, action)
            # avoid re visit visited states
            if next_state in explored:
                continue
            #compute cost
            step_cost = problem.get_cost(current, action)
            total_cost = current_cost + step_cost
            est_total = total_cost + heuristic(problem, next_state)
            #push the new state with its estimated priority
            counter += 1
            heapq.heappush(
                frontier,
                (est_total, counter, next_state, current_path + [action], total_cost)
            )
    # if the queue empty -> no path was found
    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    """
    best first search (greedy) choose the next state to explore based on heuristic estimate
    always expand the state that appears closest to the goal using the heuristic
    """
    
    #DS
    #frontier: pq min heap to always expand state that looks like the best option
    #visited: set to know explored states & prevent re visit them
    frontier = []
    visited = set()
    #heap store tuples of ( heuristic_value,order, current_state, path )
    #'order'ensure tie break when heuristic values equal
    order_counter = 0
    heapq.heappush(frontier, (heuristic(problem, initial_state), order_counter, initial_state, []))
    while frontier:
        # pick state with the smallest heuristic value
        _,_,current, path = heapq.heappop(frontier)
        #if we have reach the goal return actions
        if problem.is_goal(current):
            return path
        # prevent re visit already visited states
        if current in visited:
            continue
        visited.add(current)
        #explore each possible move from curr state
        for action in problem.get_actions(current):
            next_state = problem.get_successor(current, action)
            #ignore explored states
            if next_state in visited:
                continue
            # push new state to pq 
            order_counter += 1
            heapq.heappush(
                frontier,
                (heuristic(problem, next_state), order_counter, next_state, path + [action])
            )
    return None