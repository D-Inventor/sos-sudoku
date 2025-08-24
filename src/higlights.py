from termcolor import colored
from src.cell import Cell


class FieldPointer:
    def __init__(self, position: tuple[int,int]):
        self._position = position

    def getBefore(self, cell: Cell, position: tuple[int,int]):
        if position == self._position:
            return colored(">", "light_green")
        return None
    
    def getAfter(self, cell: Cell, position: tuple[int,int]):
        if (position == self._position):
            return colored("<", "light_green")
        return None