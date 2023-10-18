from enum import Enum

class Cell(Enum):
    EMPTY = "⬜"
    WALL = "⬛"
    BOX = "📦"
    PLAYER = "🧔"
    PALYER_OVER_BUTTON = 'J'
    BUTTON = "🔘"
    SOLVED = "X"




class Board:
    def __init__(self, size : int) -> None:
        self.size = size
        self.matrix = [[Cell.EMPTY] * size] * size

        self.boxes : list[(int, int)] = []
        self.buttons : list[(int, int)] = []
        self.player : (int, int) | None = None

    def set(self, p : (int, int), value : Cell):
        pass

    def get(self, p : (int, int)) -> Cell:
        pass

    def __eval_cell(self, p : (int, int)) -> int:
        return 0

    def eval(self) -> int:
        return sum(map(self.buttons, self.__eval_cell)) + self.__eval_cell(self.player) - 1 

    def print(self) -> None:
        for line in self.matrix:
            for cell in line: print(cell, end="")
            print("")

    