from typing import List, Tuple
import heapq
from enum import Enum
import copy

class CellType(Enum):
    EMPTY = "⬜"
    WALL = "⬛"
    PATH = "🟥"
    BOX = "📦"
    PLAYER = "🧔"
    PALYER_OVER_BUTTON = 'J'
    BUTTON = "🔘"
    SOLVED = "X"

    def is_solid (self) -> bool:
        return self in [CellType.WALL]

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

SCORE_RELEVANT_CELLS = [CellType.BUTTON, CellType.PLAYER, CellType.PALYER_OVER_BUTTON]

class Board:
    def __init__(self, size : int) -> None:
        self.size = size
        self.matrix = [[CellType.EMPTY for _ in range(size)] for _ in range(size)]

        self.boxes : list[(int, int)] = []
        self.buttons : list[(int, int)] = []
        self.player : (int, int) | None = None
        self.score = None

    def is_solid_at (self, p : (int, int)):
        return self.get(p) in [CellType.WALL, CellType.BOX, CellType.SOLVED]

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

        match value:
            case CellType.BOX: self.boxes.append(p)
            case CellType.BUTTON: self.buttons.append(p)
            case CellType.PLAYER | CellType.PALYER_OVER_BUTTON: self.player = p
        
        return self

    def get(self, p : (int, int)) -> CellType:
        return self.matrix[p[1]][p[0]]
    
    def __inner_a_star(self, start : (int, int), destiny : (int, int) ):
        pass
        vizited = [[False] * self.size] * self.size
    
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
            case CellType.BUTTON: return True
            case CellType.BOX:
                newest_pos = pos_plus_dir(new_pos, dir)
                return True if (
                    self.is_inside(newest_pos) 
                    and self.get(newest_pos) in [CellType.EMPTY, CellType.BUTTON]
                ) else False
            
            case other: return False
    
    # def can_move (self, dir : Direction):
    #     return self.cell_can_move_to(self.player, dir)
        
    def options (self, pos : (int, int)):
        return filter(lambda d: self.cell_can_move_to(pos, d), Direction)
    
    def neighbors (self, pos : (int, int)):
        return map(lambda d: pos_plus_dir(pos, d), self.options(pos))
    
    def mutable_move (self, dir : Direction)
        

    def move (self, dir : Direction):
        b = self.clone()
        return self.mutable_move(dir)

    
    def __get_box_dist(self, p : (int, int)) -> int:
        pass

    def eval_cell(self, p : (int, int)) -> int:
        c = self.get(p)
        if (c not in SCORE_RELEVANT_CELLS): return 0
        return self.get_min_box_dist(p)

    def eval(self) -> int:
        relevant_cells = self.buttons + [self.player]
        return sum(map(self.eval_cell, relevant_cells))

    def print(self) -> None:
        for line in self.matrix:
            for cell in line: print(cell.value, end="")
            print("")

    def astar_dist(self, source: Tuple[int, int], destiny: Tuple[int, int], mark : bool = False) -> int:
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
                if mark: 
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

    # TODO: improve this solution
    def get_min_box_dist (self, point: (int, int)):
        return min([self.astar_dist(point, btn) for btn in self.buttons])

if '__main__' == __name__:
    # b = Board(7)
    # b.set((1, 1), CellType.PLAYER)
    # b.set((1, 2), CellType.WALL)
    # b.set((3, 3), CellType.BOX)
    # b.set((5, 5), CellType.BUTTON)
    # b.set((0, 0), CellType.PLAYER)
    # b.set((1, 0), CellType.WALL)
    # b.set((1, 1), CellType.WALL)
    # b.set((1, 2), CellType.WALL)
    # b.set((1, 3), CellType.WALL)
    # b.set((1, 4), CellType.WALL)
    # b.set((1, 5), CellType.WALL)
    # b.set((2, 5), CellType.WALL)
    # b.set((3, 5), CellType.WALL)
    # b.set((3, 1), CellType.BUTTON)
    
    # print("Movement options availble:", list(b.options((0, 0))))
    # b.print()
    # print("Min dist between player and box: ", b.astar_dist((0, 0), (3, 1), mark=True))
    # b.print()
    # print("SCORE: ", b.eval())
    # print(b.matrix)

    b = Board(3)
    b.set((1, 0), CellType.PLAYER)
    b.set((1, 1), CellType.BOX)
    b.set((2, 2), CellType.BUTTON)
    b.print()
    print("SCORE: ", b.eval())
