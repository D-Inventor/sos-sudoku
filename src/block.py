"""Module representing a 3x3 block in a Sudoku puzzle."""

from src.cell import Cell, EmptyCell
from src.cellcollection import CellCollection


class Block(CellCollection):
    """Represents a 3x3 block in a Sudoku puzzle."""

    def __init__(
        self, offset: tuple[int, int], cells: dict[tuple[int, int], Cell]
    ) -> None:
        (self._offset_x, self._offset_y) = offset
        self._cells = cells

    def get(self, x: int, y: int) -> Cell:
        """Gets a cell from the block using local coordinates."""
        return self._cells[(x, y)] if (x, y) in self._cells else EmptyCell.create()

    def local_to_global(self, x: int, y: int) -> tuple[int, int]:
        """Converts local block coordinates to global Sudoku coordinates."""
        return (x + self._offset_x, y + self._offset_y)

    def global_to_local_row(self, y: int) -> int:
        """Converts a global row index to a local block row index."""
        result = y - self._offset_y
        if result < 1 or result > 3:
            raise ValueError("The given row does not intersect this block")
        return result

    def global_to_local_column(self, x: int) -> int:
        """Converts a global column index to a local block column index."""
        result = x - self._offset_x
        if result < 1 or result > 3:
            raise ValueError("The given column does not intersect with this block")
        return result

    @property
    def cells(self) -> list[Cell]:
        return list(self._cells.values())
