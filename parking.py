from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point

ParkingState = Tuple[Point]   
# array of immutable points indicating cars' positions
# the point at position 'i' indicates car of index i 
# (this is why i haven't used set as a data structure, although it seems to fit more in the usage (O(1)search))

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        return self.cars    # Initially our state is the cars' initial positions
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        for i,car_pos in enumerate(state):
            if self.slots.get(car_pos) != i:
                return False
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        action_list = []
        for i, car_pos in enumerate(state):
            for direction in Direction:
                new_car_pos = car_pos + direction.to_vector()
                if new_car_pos in  self.passages and new_car_pos not in state: # the new point is a passage and no other car  at the same point
                    action_list.append((i, direction))
        
        return action_list                    
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        car_ind, direction = action
        new_state = list(state) 
        new_state[car_ind] = new_state[car_ind] +  direction.to_vector()
        
        return tuple(new_state)
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        index , _ = action
        return 26 - index 
    
    # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    