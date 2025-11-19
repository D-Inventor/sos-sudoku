import itertools

from src.block import Block

from .cell import Cell, EmptyCell, FullCell
from .line import Column, Row


class Sudoku:
    def __init__(self, cells: dict[tuple[int, int], Cell]) -> None:
        self._cells: dict[tuple[int, int], Cell] = cells

    @property
    def cells(self) -> list[tuple[tuple[int, int], Cell]]:
        return [(position, self._cells[position]) for position in self._cells]

    def set(self, x: int, y: int, number: int | Cell) -> "Sudoku":
        ensure_position_inside_bounds(x, y)

        number = ensure_number_is_cell(number)

        if isinstance(number, FullCell):
            ensure_no_collisions(self, x, y, number)

        new_instance = self.copy()
        if isinstance(number, FullCell):
            new_instance._cells = new_instance._cells | self.eliminate_row(
                y, number.value
            )
            new_instance._cells = new_instance._cells | self.eliminate_column(
                x, number.value
            )
            new_instance._cells = new_instance._cells | self.eliminate_block(
                x, y, number.value
            )

        new_instance._cells[(x, y)] = number
        return new_instance

    def eliminate_row(self, y: int, number: int) -> dict[tuple[int, int], Cell]:
        row = self.getrow(y)
        row_cells = [(x, row.get(x)) for x in range(1, 10)]
        return {
            (x, y): cell.eliminate(number)
            for x, cell in row_cells
            if isinstance(cell, EmptyCell)
        }

    def eliminate_column(self, x: int, number: int) -> dict[tuple[int, int], Cell]:
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
        row = {x: self._cells[(x, y)] for x, y in self._cells.keys() if y == index}
        return Row(index, row)

    def getcolumn(self, index: int) -> Column:
        column = {y: self._cells[(x, y)] for x, y in self._cells.keys() if x == index}
        return Column(index, column)

    def getblock(self, x: int, y: int) -> Block:
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
        blockx = ((x - 1) // 3) + 1
        blocky = ((y - 1) // 3) + 1
        return self.getblock(blockx, blocky)

    def get(self, x: int, y: int) -> Cell:
        return self._cells[(x, y)] if (x, y) in self._cells else EmptyCell.create()

    def copy(self) -> "Sudoku":
        return Sudoku(self._cells.copy())

    @staticmethod
    def empty() -> "Sudoku":
        return Sudoku({})

    @staticmethod
    def fromarray(input: list[list[int | None]]) -> "Sudoku":
        result = Sudoku.empty()
        for x, y in itertools.product(range(0, 9), range(0, 9)):
            if input_is_number(input, x, y):
                result = result.set(x + 1, y + 1, FullCell(input[y][x]))
        return result


def input_is_number(input: list[list[int | None]], x: int, y: int) -> bool:
    return len(input) > y and len(input[y]) > x and input[y][x] is not None


def ensure_no_collisions(sudoku: Sudoku, x: int, y: int, number: FullCell) -> None:
    if sudoku.getrow(y).contains(number.value):
        raise ValueError("Same number is already present in this row")
    if sudoku.getcolumn(x).contains(number.value):
        raise ValueError("Same number is already present in this column")
    if sudoku.getblockfromcell(x, y).contains(number.value):
        raise ValueError("Same number is already present in this block")


def ensure_number_is_cell(number: int | Cell) -> Cell:
    return FullCell(number) if isinstance(number, int) else number


def ensure_position_inside_bounds(x: int, y: int) -> None:
    ensure_x_inside_bounds(x)
    ensure_y_inside_bounds(y)


def ensure_y_inside_bounds(y: int) -> None:
    ensure_inside_bounds(y, "y must be between 1 and 9")


def ensure_x_inside_bounds(x: int) -> None:
    ensure_inside_bounds(x, "x must be between 1 and 9")


def ensure_inside_bounds(number: int, error_message: str) -> None:
    if number > 9 or number < 1:
        raise ValueError(error_message)
