import itertools
from src.block import Block
from src.cell import Cell, EmptyCell
from src.line import Column, Line, Row
from src.sudoku import Sudoku


def findCellsWithSingleOption(sudoku: Sudoku) -> list[tuple[int, int]]:
    return [
        position for position, cell in sudoku.cells if cellHasOnePossibleNumber(cell)
    ]


def cellHasOnePossibleNumber(cell: Cell) -> bool:
    return isinstance(cell, EmptyCell) and len(cell.possibleNumbers) == 1


def findCellsWithUniqueNumberInRows(sudoku: Sudoku) -> list[tuple[int, int]]:
    return [
        position
        for y in range(1, 10)
        for position in findCellsWithUniqueNumberInSingleRow(sudoku.getrow(y))
    ]


def findCellsWithUniqueNumberInSingleRow(row: Row):
    return [row.localToGlobal(x) for x in findIndexesForUniqueNumbersInLine(row)]


def findCellsWithUniqueNumberInColumns(sudoku: Sudoku) -> list[tuple[int, int]]:
    return [
        position
        for x in range(1, 10)
        for position in findCellsWithUniqueNumberInSingleColumn(sudoku.getcolumn(x))
    ]


def findCellsWithUniqueNumberInSingleColumn(column: Column):
    return [column.localToGlobal(y) for y in findIndexesForUniqueNumbersInLine(column)]


def findIndexesForUniqueNumbersInLine(line: Line) -> list[int]:
    numbers = {key: list() for key in range(1, 10)}
    for index, cell in [(index, line.get(index)) for index in range(1, 10)]:
        if isinstance(cell, EmptyCell):
            for possibleNumber in cell.possibleNumbers:
                numbers[possibleNumber].append(index)

    return [
        index
        for number in numbers
        if len(numbers[number]) == 1
        for index in numbers[number]
    ]


def findCellsWithUniqueNumberInBlocks(sudoku: Sudoku) -> list[tuple[int, int]]:
    return [
        position
        for (x, y) in itertools.product(range(1, 4), range(1, 4))
        for position in findCellsWithUniqueNumberInSingleBlock(sudoku.getblock(x, y))
    ]


def findCellsWithUniqueNumberInSingleBlock(block: Block) -> list[tuple[int, int]]:
    numbers = {key: list() for key in range(1, 10)}
    for x, y, cell in [
        (x, y, block.get(x, y))
        for (x, y) in itertools.product(range(1, 4), range(1, 4))
    ]:
        if isinstance(cell, EmptyCell):
            for possibleNumber in cell.possibleNumbers:
                numbers[possibleNumber].append((x, y))
    return [
        block.localToGlobal(x, y)
        for number in numbers
        if len(numbers[number]) == 1
        for x, y in numbers[number]
    ]
