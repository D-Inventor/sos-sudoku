from termcolor import colored

from src.cell import Cell


class FieldPointer:
    def __init__(self, position: tuple[int, int]) -> None:
        self._position = position

    def getBefore(self, cell: Cell, position: tuple[int, int]) -> str | None:
        if position == self._position:
            return colored(">", "light_green")
        return None

    def getAfter(self, cell: Cell, position: tuple[int, int]) -> str | None:
        if position == self._position:
            return colored("<", "light_green")
        return None
