from src.cellcollection import CellCollection
from .cell import Cell, EmptyCell


class Line(CellCollection):
    def __init__(self, index: int, cells: dict[int, Cell]):
        if index < 1 or index > 9:
            raise ValueError("Index must be a value between 1 and 9")

        self._cells: dict[int, Cell] = cells
        self._index = index

    def get(self, index: int) -> Cell:
        if index < 1 or index > 9:
            raise ValueError("Index must be a value between 1 and 9")

        return self._cells[index] if index in self._cells else EmptyCell.create()

    @property
    def cells(self):
        return list(self._cells.values())

    @property
    def index(self):
        return self._index


class Row(Line):
    def localToGlobal(self, x: int) -> tuple[int, int]:
        return (x, self._index)


class Column(Line):
    def localToGlobal(self, y: int) -> tuple[int, int]:
        return (self._index, y)
