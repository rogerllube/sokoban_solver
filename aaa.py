from typing import List, Tuple
import heapq
from enum import Enum
import copy

class CellType(Enum):
    EMPTY = "⬜"
    WALL = "⬛"
    BOX = "📦"
    PLAYER = "🧔"
    PALYER_OVER_BUTTON = 'J'
    BUTTON = "🔘"
    SOLVED = "X"

    def is_solid (self) -> bool:
        return self in [CellType.WALL, CellType.BOX, CellType.SOLVED]

class Direction(Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"

DIRECTIONS = list(Direction)

def pos_plus_dir (pos : (int, int), dir : Direction) -> (int, int):
    match dir:
        case Direction.UP: return (pos[0], pos[1] - 1)
        case Direction.RIGHT: return (pos[0] + 1, pos[1])
        case Direction.DOWN: return (pos[0], pos[1] + 1)
        case Direction.LEFT: return (pos[0] - 1, pos[1])
        case other: return (pos[0], pos[1])

class Board:
    def __init__(self, size : int) -> None:
        self.size = size
        self.matrix = [[CellType.EMPTY for _ in range(size)] for _ in range(size)]

    def clone(self):
        return copy.deepcopy(self)

    def set(self, p : (int, int), value : CellType):
        if self.player and value in [CellType.PLAYER, CellType.PALYER_OVER_BUTTON]:
            x = self.player[0]
            y = self.player[1]
            self.matrix[y][x] = CellType.EMPTY

        x = p[0]
        y = p[1]
        self.matrix[y][x] = value

    def get(self, p : (int, int)) -> CellType:
        return self.matrix[p[1]][p[0]]
    
    def is_inside (self, pos : (int, int)) -> bool:
        x = pos[0]
        y = pos[1]
        s = self.size
        return x >= 0 and y >= 0 and x < s and y < s

    def cell_can_move_to (self, p : (int, int), dir : Direction):
        new_pos = pos_plus_dir(p, dir)
        if (not self.is_inside(new_pos)): return False

        match self.get(new_pos):
            case CellType.EMPTY: return True

            case CellType.BOX:
                newest_pos = pos_plus_dir(new_pos, dir)
                return True if (
                    self.is_inside(newest_pos) 
                    and self.get(newest_pos) in [CellType.EMPTY, CellType.BUTTON]
                ) else False
            
            case other: return False

    def cell_can_move_to (self, p : (int, int), dir : Direction):
        new_pos = pos_plus_dir(p, dir)
        if (not self.is_inside(new_pos)): return False

        match self.get(new_pos):
            case CellType.EMPTY: return True

            case CellType.BOX:
                newest_pos = pos_plus_dir(new_pos, dir)
                return True if (
                    self.is_inside(newest_pos) 
                    and self.get(newest_pos) in [CellType.EMPTY, CellType.BUTTON]
                ) else False
            
            case other: return False
        
    def options (self, pos : (int, int)):
        return filter(lambda d: self.cell_can_move_to(pos, d), Direction)
    
    def neighbors (self, pos : (int, int)):
        return map(lambda d: pos_plus_dir(pos, d), self.options(pos))
    

    def astar_dist(self, source: Tuple[int, int], destiny: Tuple[int, int]) -> int:
    # Define a heuristic function for estimating the remaining cost (Manhattan distance).
    def heuristic(cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    open_list = []  # Priority queue for cells to be evaluated
    closed_list = set()  # Set of evaluated cells
    g_score = {source: 0}  # Dictionary to store the distance from the start
    f_score = {source: heuristic(source, destiny)}  # Dictionary for estimated total cost
    came_from = {}  # Dictionary to store the parent cell for each cell

    heapq.heappush(open_list, (f_score[source], source))

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == destiny:
            # Reconstruct the path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)

            # Update the cells in the path to CellType.PATH
            for cell in path:
                if self.get(cell) != CellType.PLAYER:
                    self.set(cell, CellType.PATH)

            return g_score[destiny]  # Distance from source to destination

        closed_list.add(current)

        for neighbor in self.neighbors(current):
            if neighbor in closed_list:
                continue

            tentative_g_score = g_score[current] + 1  # Distance from source to neighbor

            if neighbor not in open_list or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, destiny)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    # If the open list is empty and the destination is not reached, return a large value
    return float('inf')


# Usage example:
board = Board(5)  # Replace with your desired board size
distance = board.astar_dist((0, 0), (2, 2))  # Replace with your source and destination
print("Shortest distance:", distance)
