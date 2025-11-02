import itertools

from src.block import Block
from .cell import Cell, EmptyCell, FullCell
from .line import Column, Row


class Sudoku:
    def __init__(self, cells: dict[tuple[int, int], Cell]):
        self._cells: dict[tuple[int, int], Cell] = cells

    @property
    def cells(self) -> list[tuple[tuple[int, int], Cell]]:
        return [(position, self._cells[position]) for position in self._cells]

    def set(self, x: int, y: int, number: int | Cell) -> "Sudoku":
        ensurePositionInsideBounds(x, y)

        number = ensureNumberIsCell(number)

        if isinstance(number, FullCell):
            ensureNoCollisions(self, x, y, number)

        newInstance = self.copy()
        if isinstance(number, FullCell):
            newInstance._cells = newInstance._cells | self.eliminateRow(y, number.value)
            newInstance._cells = newInstance._cells | self.eliminateColumn(
                x, number.value
            )
            newInstance._cells = newInstance._cells | self.eliminateBlock(
                x, y, number.value
            )

        newInstance._cells[(x, y)] = number
        return newInstance

    def eliminateRow(self, y: int, number: int):
        row = self.getrow(y)
        rowCells = [(x, row.get(x)) for x in range(1, 10)]
        return {
            (x, y): cell.eliminate(number)
            for x, cell in rowCells
            if isinstance(cell, EmptyCell)
        }

    def eliminateColumn(self, x: int, number: int):
        column = self.getcolumn(x)
        columnCells = [(y, column.get(y)) for y in range(1, 10)]
        return {
            (x, y): cell.eliminate(number)
            for y, cell in columnCells
            if isinstance(cell, EmptyCell)
        }

    def eliminateBlock(self, x: int, y: int, number: int):
        block = self.getblockfromcell(x, y)
        cells = [
            (blockx, blocky, block.get(blockx, blocky))
            for blockx, blocky in itertools.product(range(1, 4), range(1, 4))
        ]
        return {
            block.localToGlobal(blockx, blocky): cell.eliminate(number)
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

        minX = x * 3 - 2
        minY = y * 3 - 2
        maxX = minX + 3
        maxY = minY + 3
        block = {
            (x - minX + 1, y - minY + 1): self._cells[(x, y)]
            for x, y in self._cells.keys()
            if minX <= x < maxX and minY <= y < maxY
        }
        return Block((minX - 1, minY - 1), block)

    def getblockfromcell(self, x: int, y: int):
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
            if inputIsNumber(input, x, y):
                result = result.set(x + 1, y + 1, FullCell(input[y][x]))
        return result


def inputIsNumber(input: list[list[int | None]], x: int, y: int) -> bool:
    return len(input) > y and len(input[y]) > x and input[y][x] is not None


def ensureNoCollisions(sudoku: Sudoku, x: int, y: int, number: FullCell):
    if sudoku.getrow(y).contains(number.value):
        raise ValueError("Same number is already present in this row")
    if sudoku.getcolumn(x).contains(number.value):
        raise ValueError("Same number is already present in this column")
    if sudoku.getblockfromcell(x, y).contains(number.value):
        raise ValueError("Same number is already present in this block")


def ensureNumberIsCell(number: int | Cell) -> Cell:
    return FullCell(number) if isinstance(number, int) else number


def ensurePositionInsideBounds(x: int, y: int):
    ensureXInsideBounds(x)
    ensureYInsideBounds(y)


def ensureYInsideBounds(y: int):
    ensureInsideBounds(y, "y must be between 1 and 9")


def ensureXInsideBounds(x: int):
    ensureInsideBounds(x, "x must be between 1 and 9")


def ensureInsideBounds(number: int, errorMessage: str):
    if number > 9 or number < 1:
        raise ValueError(errorMessage)
