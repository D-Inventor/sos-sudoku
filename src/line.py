"""Module representing a line (row or column) in a Sudoku puzzle."""

from src.cellcollection import CellCollection

from .cell import Cell, EmptyCell


class Line(CellCollection):
    """Abstract base class for a line (row or column) in a Sudoku puzzle."""

    def __init__(self, index: int, cells: dict[int, Cell]) -> None:
        if index < 1 or index > 9:
            raise ValueError("Index must be a value between 1 and 9")

        self._cells: dict[int, Cell] = cells
        self._index = index

    def get(self, index: int) -> Cell:
        """Gets a cell from the line using local coordinates."""
        if index < 1 or index > 9:
            raise ValueError("Index must be a value between 1 and 9")

        return self._cells[index] if index in self._cells else EmptyCell.create()

    @property
    def cells(self) -> list[Cell]:
        return list(self._cells.values())

    @property
    def index(self) -> int:
        """Returns the index of the line (row or column)."""
        return self._index


class Row(Line):
    """Represents a row in a Sudoku puzzle."""

    def local_to_global(self, x: int) -> tuple[int, int]:
        """Converts local row coordinates to global Sudoku coordinates."""
        return (x, self._index)


class Column(Line):
    """Represents a column in a Sudoku puzzle."""

    def local_to_global(self, y: int) -> tuple[int, int]:
        """Converts local column coordinates to global Sudoku coordinates."""
        return (self._index, y)
