from src.cell import Cell, EmptyCell
from src.cellcollection import CellCollection


class Block(CellCollection):

    def __init__(self, offset: tuple[int,int], cells: dict[tuple[int,int], Cell]):
        (self._offsetX, self._offsetY) = offset
        self._cells = cells

    def get(self, x:int, y:int) -> Cell:
        return self._cells[(x, y)] if (x, y) in self._cells else EmptyCell.create()
    
    def localToGlobal(self, x:int, y:int) -> tuple[int,int]:
        return (x + self._offsetX, y + self._offsetY)

    @property
    def cells(self):
        return list(self._cells.values())