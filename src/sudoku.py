"""Module representing a Sudoku puzzle and its operations."""

import itertools

from src.block import Block

from .cell import Cell, EmptyCell, FullCell
from .line import Column, Row


class Sudoku:
    """Represents a Sudoku puzzle."""

    def __init__(self, cells: dict[tuple[int, int], Cell]) -> None:
        self._cells: dict[tuple[int, int], Cell] = cells

    @property
    def cells(self) -> list[tuple[tuple[int, int], Cell]]:
        """Returns a list of all cells in the Sudoku puzzle with their positions."""
        return [(position, self._cells[position]) for position in self._cells]

    def set(self, x: int, y: int, number: int | Cell) -> "Sudoku":
        """Creates a copy with the specified cell set to the given number."""
        ensure_position_inside_bounds(x, y)

        number = ensure_number_is_cell(number)

        if isinstance(number, FullCell):
            ensure_no_collisions(self, x, y, number)

        new_cells = self._cells.copy()
        if isinstance(number, FullCell):
            new_cells = new_cells | self.eliminate_row(y, number.value)
            new_cells = new_cells | self.eliminate_column(x, number.value)
            new_cells = new_cells | self.eliminate_block(x, y, number.value)

        new_cells[(x, y)] = number
        return Sudoku(new_cells)

    def eliminate_row(self, y: int, number: int) -> dict[tuple[int, int], Cell]:
        """Eliminates the given number from all empty cells in the specified row."""
        row = self.getrow(y)
        row_cells = [(x, row.get(x)) for x in range(1, 10)]
        return {
            (x, y): cell.eliminate(number)
            for x, cell in row_cells
            if isinstance(cell, EmptyCell)
        }

    def eliminate_column(self, x: int, number: int) -> dict[tuple[int, int], Cell]:
        """Eliminates the given number from all empty cells in the specified column."""
        column = self.getcolumn(x)
        column_cells = [(y, column.get(y)) for y in range(1, 10)]
        return {
            (x, y): cell.eliminate(number)
            for y, cell in column_cells
            if isinstance(cell, EmptyCell)
        }

    def eliminate_block(
        self, x: int, y: int, number: int
    ) -> dict[tuple[int, int], Cell]:
        """Eliminates the given number from all empty cells in the specified block."""
        block = self.getblockfromcell(x, y)
        cells = [
            (blockx, blocky, block.get(blockx, blocky))
            for blockx, blocky in itertools.product(range(1, 4), range(1, 4))
        ]
        return {
            block.local_to_global(blockx, blocky): cell.eliminate(number)
            for blockx, blocky, cell in cells
            if isinstance(cell, EmptyCell)
        }

    def getrow(self, index: int) -> Row:
        """Gets a row from the Sudoku puzzle."""
        row = {x: self._cells[(x, y)] for x, y in self._cells.keys() if y == index}
        return Row(index, row)

    def getcolumn(self, index: int) -> Column:
        """Gets a column from the Sudoku puzzle."""
        column = {y: self._cells[(x, y)] for x, y in self._cells.keys() if x == index}
        return Column(index, column)

    def getblock(self, x: int, y: int) -> Block:
        """Gets a 3x3 block from the Sudoku puzzle."""
        if x < 1 or x > 3:
            raise ValueError("x must be between 1 and 3")
        if y < 1 or y > 3:
            raise ValueError("y must be between 1 and 3")

        min_x = x * 3 - 2
        min_y = y * 3 - 2
        max_x = min_x + 3
        max_y = min_y + 3
        block = {
            (x - min_x + 1, y - min_y + 1): self._cells[(x, y)]
            for x, y in self._cells.keys()
            if min_x <= x < max_x and min_y <= y < max_y
        }
        return Block((min_x - 1, min_y - 1), block)

    def getblockfromcell(self, x: int, y: int) -> Block:
        """Gets the block that contains the specified cell."""
        blockx = ((x - 1) // 3) + 1
        blocky = ((y - 1) // 3) + 1
        return self.getblock(blockx, blocky)

    def get(self, x: int, y: int) -> Cell:
        """Gets a cell from the Sudoku puzzle using global coordinates."""
        return self._cells[(x, y)] if (x, y) in self._cells else EmptyCell.create()

    @staticmethod
    def empty() -> "Sudoku":
        """Creates an empty Sudoku puzzle."""
        return Sudoku({})

    @staticmethod
    def fromarray(values: list[list[int | None]]) -> "Sudoku":
        """Creates a Sudoku puzzle from a 2D array representation."""
        result = Sudoku.empty()
        for x, y in itertools.product(range(0, 9), range(0, 9)):
            if input_is_number(values, x, y):
                result = result.set(x + 1, y + 1, FullCell(values[y][x]))
        return result


def input_is_number(values: list[list[int | None]], x: int, y: int) -> bool:
    """Checks if the input at the given coordinates is a number."""
    return len(values) > y and len(values[y]) > x and values[y][x] is not None


def ensure_no_collisions(sudoku: Sudoku, x: int, y: int, number: FullCell) -> None:
    """Ensure that it is valid to place the given number at the specified position."""
    if sudoku.getrow(y).contains(number.value):
        raise ValueError("Same number is already present in this row")
    if sudoku.getcolumn(x).contains(number.value):
        raise ValueError("Same number is already present in this column")
    if sudoku.getblockfromcell(x, y).contains(number.value):
        raise ValueError("Same number is already present in this block")


def ensure_number_is_cell(number: int | Cell) -> Cell:
    """Ensures that the given number is wrapped in a Cell instance."""
    return FullCell(number) if isinstance(number, int) else number


def ensure_position_inside_bounds(x: int, y: int) -> None:
    """Ensures that the given position is within the bounds of the Sudoku grid."""
    ensure_x_inside_bounds(x)
    ensure_y_inside_bounds(y)


def ensure_y_inside_bounds(y: int) -> None:
    """Ensures that the y coordinate is within the bounds of the Sudoku grid."""
    ensure_inside_bounds(y, "y must be between 1 and 9")


def ensure_x_inside_bounds(x: int) -> None:
    """Ensures that the x coordinate is within the bounds of the Sudoku grid."""
    ensure_inside_bounds(x, "x must be between 1 and 9")


def ensure_inside_bounds(number: int, error_message: str) -> None:
    """Ensures that the given number is between 1 and 9."""
    if number > 9 or number < 1:
        raise ValueError(error_message)
