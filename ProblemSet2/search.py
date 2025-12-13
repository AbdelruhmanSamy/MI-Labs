from typing import Optional, Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
from typing import Callable, Generic, Iterable, List, TypeVar, Union

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].




def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    
    def max_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth: int, max_depth: int = -1)-> Tuple[float, A]:
        # This function is called when the agent = 0, it searches in the child nodes, get values and picks the max-value among them
        
        # initializing curr_val with negative infinity (min value in float) in order to optimize by looking at child nodes
        # and action with None
        curr_val = float('-inf')
        curr_action = None        
        
        # combining actions and next_states  into one interatable in order to check for child node values
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        for (action, next_state) in actions_states:
            # getting child value and ignoring the action, by calling minimax_value function
            new_val, _ = minimax_value(game, next_state, heuristic, curr_depth + 1, max_depth)

            # comparing new value to the current value
            # if greater, replace the curr_val with new_val and save the action to be returned
            if new_val > curr_val:
                curr_val = new_val
                curr_action = action
                
        # returning the max value reached and the action lead to this value
        return curr_val, curr_action
                    
    def min_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth: int, max_depth: int = -1)-> Tuple[float, A]:
        # This function is called when the agent >  0, it searches in the child nodes, get values and picks the min-value among them
        
        # initializing curr_val with infinity (max value in float) in order to optimize by looking at child nodes
        # and action with None
        curr_val = float('inf')
        curr_action = None
        
        # combining actions and next_states  into one interatable in order to check for child node values
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        
        for (action, next_state) in actions_states:
            # getting child value and ignoring the action, by calling minimax_value function
            new_val, _ = minimax_value(game, next_state, heuristic, curr_depth + 1, max_depth)
            
            # comparing new value to the current value
            # if smaller, replace the curr_val with new_val and save the action to be returned
            if new_val < curr_val:
                curr_val = new_val
                curr_action = action

        # returning the min value reached and the action lead to this value
        return curr_val, curr_action
    
    def minimax_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth,  max_depth: int = -1)-> Tuple[float, A]:
        # this function is called initially when the the main minimax function is called
        # and called inside both min_value() and max_value() function, it does termination
        # checks,decides whether searching with min or max values according to agent
        
        # getting agent which helps in deciding whether applying min or max search
        agent = game.get_turn(state)
        
        # checking for terminal node
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None 
        
        # checking for reaching max depth
        if max_depth != -1 and curr_depth == max_depth:
            return heuristic(game, state, 0), None
        
        # decision of next node type (max or min) upon next agent
        if agent == 0:
            return max_value(game, state, heuristic, curr_depth, max_depth)
        else:
            return min_value(game, state, heuristic, curr_depth, max_depth)
                
    return minimax_value(game, state, heuristic, 0,  max_depth)
# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def max_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth: int, alpha: float, beta: float, max_depth: int = -1)-> Tuple[float, A]:
        # This function is called when the agent = 0, it searches in the child nodes, get values and picks the max-value among them
        
        # initializing curr_val with negative infinity (min value in float) in order to optimize by looking at child nodes
        # and action with None
        curr_val = float('-inf')
        curr_action = None        
        # combining actions and next_states  into one interatable in order to check for child node values
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        for (action, next_state) in actions_states:
            # getting child value and ignoring the action, by calling minimax_value function
            new_val, _ = minimax_value(game, next_state, heuristic, curr_depth + 1,alpha, beta, max_depth)

            # comparing new value to the current value
            # if greater, replace the curr_val with new_val and save the action to be returned
            if new_val > curr_val:
                curr_val = new_val
                curr_action = action
            
            # prunning if the new value is greater than the best value selected for above min nodes
            if new_val >= beta:
                return new_val, action
            
            # updating alpha value upon getting a value greater than the current alpha value
            alpha = max(alpha, new_val)
        # returning the max value reached and the action lead to this value
        return curr_val, curr_action
                    
    def min_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth: int, alpha: float, beta: float, max_depth: int = -1)-> Tuple[float, A]:
        # This function is called when the agent >  0, it searches in the child nodes, get values and picks the min-value among them
        
        # initializing curr_val with infinity (max value in float) in order to optimize by looking at child nodes
        # and action with None
        curr_val = float('inf')
        curr_action = None
        
        # combining actions and next_states  into one interatable in order to check for child node values
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        
        for (action, next_state) in actions_states:
            # getting child value and ignoring the action, by calling minimax_value function
            new_val, _ = minimax_value(game, next_state, heuristic, curr_depth + 1, alpha, beta, max_depth)
            
            # comparing new value to the current value
            # if smaller, replace the curr_val with new_val and save the action to be returned
            if new_val < curr_val:
                curr_val = new_val
                curr_action = action

            # prunning if the new value is less than the best value selected for above max nodes
            if new_val <= alpha:
                return new_val , action
            
            # updating beta value upon getting a value greater than the current alpha value
            beta = min(beta, new_val)
        # returning the min value reached and the action lead to this value
        return curr_val, curr_action
    
    def minimax_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth,  alpha: float, beta: float, max_depth: int = -1)-> Tuple[float, A]:
        # this function is called initially when the the main minimax function is called
        # and called inside both min_value() and max_value() function, it does termination
        # checks,decides whether searching with min or max values according to agent
        
        # getting agent which helps in deciding whether applying min or max search
        agent = game.get_turn(state)
        
        # checking for terminal node
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None 
        
        # checking for reaching max depth
        if max_depth != -1 and curr_depth == max_depth:
            return heuristic(game, state, 0), None
        
        # decision of next node type (max or min) upon next agent
        if agent == 0:
            return max_value(game, state, heuristic, curr_depth, alpha, beta, max_depth)
        else:
            return min_value(game, state, heuristic, curr_depth,alpha, beta, max_depth)
    
    return minimax_value(game, state, heuristic, 0, float('-inf'), float('inf'), max_depth)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def sort_val(a: Tuple[A , S]):
        # key function for sorting (action , state) lists to apply move ordering
        # A heuristic function is used to give an estimate of the state
        # as we cannot do perfect sorting (metareasoning problem)
        return heuristic(game, a[1], 0)
    
    def max_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth: int, alpha: float, beta: float, max_depth: int = -1)-> Tuple[float, A]:
        # This function is called when the agent = 0, it searches in the child nodes, get values and picks the max-value among them
        
        # initializing curr_val with negative infinity (min value in float) in order to optimize by looking at child nodes
        # and action with None
        curr_val = float('-inf')
        curr_action = None        
        # combining actions and next_states  into one interatable in order to check for child node values
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # sorting (action , next_state) descendingly according to heuristic in order to apply move ordering 
        sorted_actions_states = sorted(actions_states, key=sort_val, reverse=True)
        
        for (action, next_state) in sorted_actions_states:
            # getting child value and ignoring the action, by calling minimax_value function
            new_val, _ = minimax_value(game, next_state, heuristic, curr_depth + 1,alpha, beta, max_depth)

            # comparing new value to the current value
            # if greater, replace the curr_val with new_val and save the action to be returned
            if new_val > curr_val:
                curr_val = new_val
                curr_action = action
            
            # prunning if the new value is greater than the best value selected for above min nodes
            if new_val >= beta:
                return new_val, action
            
            # updating alpha value upon getting a value greater than the current alpha value
            alpha = max(alpha, new_val)
        # returning the max value reached and the action lead to this value
        return curr_val, curr_action
                    
    def min_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth: int, alpha: float, beta: float, max_depth: int = -1)-> Tuple[float, A]:
        # This function is called when the agent >  0, it searches in the child nodes, get values and picks the min-value among them
        
        # initializing curr_val with infinity (max value in float) in order to optimize by looking at child nodes
        # and action with None
        curr_val = float('inf')
        curr_action = None
        
        # combining actions and next_states  into one interatable in order to check for child node values
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        
        # sorting (action , next_state) ascendingly according to heuristic in order to apply move ordering 
        sorted_actions_states = sorted(actions_states, key=sort_val)
        
        for (action, next_state) in sorted_actions_states:
            # getting child value and ignoring the action, by calling minimax_value function
            new_val, _ = minimax_value(game, next_state, heuristic, curr_depth + 1, alpha, beta, max_depth)
            
            # comparing new value to the current value
            # if smaller, replace the curr_val with new_val and save the action to be returned
            if new_val < curr_val:
                curr_val = new_val
                curr_action = action

            # prunning if the new value is less than the best value selected for above max nodes
            if new_val <= alpha:
                return new_val , action
            
            # updating beta value upon getting a value greater than the current alpha value
            beta = min(beta, new_val)
        # returning the min value reached and the action lead to this value
        return curr_val, curr_action
    
    def minimax_value(game: Game[S, A], state: S, heuristic: HeuristicFunction, curr_depth,  alpha: float, beta: float, max_depth: int = -1)-> Tuple[float, A]:
        # this function is called initially when the the main minimax function is called
        # and called inside both min_value() and max_value() function, it does termination
        # checks,decides whether searching with min or max values according to agent
        
        # getting agent which helps in deciding whether applying min or max search
        agent = game.get_turn(state)
        
        # checking for terminal node
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None 
        
        # checking for reaching max depth
        if max_depth != -1 and curr_depth == max_depth:
            return heuristic(game, state, 0), None
        
        # decision of next node type (max or min) upon next agent
        if agent == 0:
            return max_value(game, state, heuristic, curr_depth, alpha, beta, max_depth)
        else:
            return min_value(game, state, heuristic, curr_depth,alpha, beta, max_depth)
    
    return minimax_value(game, state, heuristic, 0, float('-inf'), float('inf'), max_depth)

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def expectimax_value(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # check if the current state is terminal then return the first value for the player & no action
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None
        # if we reach max depth return the heuristic value for state
        if max_depth != -1 and depth == max_depth:
            return heuristic(game, state, 0), None 
        # if it is the player turn maximize else calculate the expected value for chance nodes
        if game.get_turn(state) == 0:  
            return max_value(state,depth)
        else:
            return chance_value(state,depth)
    
    def chance_value(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # if there is no actions then return the heuristic value
        if len(game.get_actions(state)) == 0:
            return heuristic(game,state,0), None
        expected = 0
        for action in game.get_actions(state):  
            successor = game.get_successor(state, action)  
            value, _ = expectimax_value(successor, depth + 1)  
            # add the contribution of this action to the expected value by average
            expected += value / len(game.get_actions(state))
        return expected, None
    
    def max_value(state: S, depth: int) -> Tuple[float, Optional[A]]:
        # start with the lowest possible value & no action
        max_v = float('-inf')
        best_action = None
        for action in game.get_actions(state):  # go through all possible actions
            successor = game.get_successor(state, action)  # get the result state
            value, _ = expectimax_value(successor, depth + 1)  # evaluate the successor usee recursion 
            # update max value and record action if this value is better
            if value > max_v:
                max_v = value
                best_action = action
        return max_v, best_action
    return expectimax_value(state, 0)