from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from collections import deque
from typing import Dict
# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use


def bfs(point , passage):
    frontier = deque()
    
    frontier.append((point, 0))
    
    destinations = {point: 0}
    
    while frontier:
        curr_pos, curr_dist = frontier.popleft()
        
        for direction in Direction:
            new_pos = curr_pos + direction.to_vector()
            if new_pos in passage and new_pos not in destinations:

                destinations[new_pos] = curr_dist + 1
                frontier.append((new_pos, curr_dist + 1))
            
    return destinations

def build_cost_matrix(state, points_dist):
    n_row = len(state.crates)
    n_col = len(state.layout.goals)
    
    n = max(n_row, n_col)
    
    cost_matrix = [[0]* n for _ in range(n)]
    for i, crate in enumerate(state.crates):
        for j, goal in  enumerate(state.layout.goals):
            cost_matrix[i][j] = points_dist[(crate, goal)]

    return cost_matrix


def _find_augmenting_path(matrix, row, visited, row_match, col_match):
    n = len(matrix)
    for col in range(n):
        if matrix[row][col] == 0 and not visited[col]:
            visited[col] = True
            
            if col_match[col] == -1 or \
                _find_augmenting_path(matrix, col_match[col], visited, row_match, col_match):
                    row_match[row] = col
                    col_match[col] = row
                    return True
    return False


def find_matches(matrix, row_match, col_match):
    """Returns the number of matches found"""
    n = len(matrix)
    match_count = 0
    
    for row in range(n):
        if row_match[row] == -1:
            visited = [False] * n
            if _find_augmenting_path(matrix, row, visited, row_match, col_match):
                match_count += 1
    
    return match_count


def get_cover(matrix, row_match, col_match, n):
    """
    Find minimum vertex cover using alternating paths.
    This is the tricky part - we need to mark rows/cols properly.
    """
    # Start with all unmatched rows marked
    marked_rows = [row_match[i] == -1 for i in range(n)]
    marked_cols = [False] * n
    
    # Repeatedly mark cols reachable from marked rows via zeros,
    # then mark rows matched to those cols
    changed = True
    while changed:
        changed = False
        
        # Mark columns that have zeros in marked rows
        for i in range(n):
            if marked_rows[i]:
                for j in range(n):
                    if matrix[i][j] == 0 and not marked_cols[j]:
                        marked_cols[j] = True
                        changed = True
        
        # Mark rows that are matched to marked columns
        for j in range(n):
            if marked_cols[j] and col_match[j] != -1:
                row = col_match[j]
                if not marked_rows[row]:
                    marked_rows[row] = True
                    changed = True
    
    # The cover is: unmarked rows + marked columns
    covered_rows = [not marked for marked in marked_rows]
    covered_cols = marked_cols
    
    return covered_rows, covered_cols


def hangarian_algorithm(cost_matrix):
    n = len(cost_matrix)
    
    # Make a copy
    matrix = [row[:] for row in cost_matrix]
    
    # Step 1: Row reduction
    for i in range(n):
        row_min = min(matrix[i])
        for j in range(n):
            matrix[i][j] -= row_min
    
    # Step 2: Column reduction
    for j in range(n):
        col_min = min(matrix[i][j] for i in range(n))
        for i in range(n):
            matrix[i][j] -= col_min
    
    # Step 3: Find initial matching
    row_match = [-1] * n
    col_match = [-1] * n
    
    max_match = find_matches(matrix, row_match, col_match)
    
    # Step 4: If not perfect matching, iterate
    max_iterations = n * n  # Safety limit
    iteration = 0
    
    while max_match < n and iteration < max_iterations:
        iteration += 1
        
        # Find covering
        covered_rows, covered_cols = get_cover(matrix, row_match, col_match, n)
        
        # Find minimum uncovered value
        min_val = float('inf')
        for i in range(n):
            for j in range(n):
                if not covered_rows[i] and not covered_cols[j]:
                    min_val = min(min_val, matrix[i][j])
        
        if min_val == float('inf'):
            # Should not happen if algorithm is correct
            break
        
        # Adjust matrix
        for i in range(n):
            for j in range(n):
                if not covered_rows[i] and not covered_cols[j]:
                    matrix[i][j] -= min_val
                elif covered_rows[i] and covered_cols[j]:
                    matrix[i][j] += min_val
        
        # Try to find more matches
        new_matches = find_matches(matrix, row_match, col_match)
        max_match += new_matches
    
    # Calculate result
    assignments = []
    total_cost = 0
    
    for i in range(n):
        j = row_match[i]
        if j != -1:  # Safety check
            assignments.append((i, j))
            total_cost += cost_matrix[i][j]
    
    return total_cost, assignments

from scipy.optimize import linear_sum_assignment
import numpy as np

def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function

    cache = problem.cache()

    if 'points_dist' in cache: 
        points_dist = cache['points_dist']
    else:
        passages = list(state.layout.walkable)

        points_dist: Dict[(Point, Point), int] = {}

        for point in passages:
            distances = bfs(point,state.layout.walkable)
            
            for dest, dist in distances.items():
                points_dist[(point, dest)] = dist
            
        cache['points_dist'] = points_dist
        
    cost_matrix = build_cost_matrix(state, points_dist)    

    total_cost, _ = hangarian_algorithm(cost_matrix)
    
    return total_cost
