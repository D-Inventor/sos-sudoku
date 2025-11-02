from dataclasses import dataclass
import itertools
from typing import Callable
from src.block import Block
from src.cell import EmptyCell
from src.line import Column, Line, Row
from src.sudoku import Sudoku


@dataclass(frozen=True)
class RowIntoBlockExtrapolation:
    rowIndex: int
    blockIndex: tuple[int, int]
    number: int


@dataclass(frozen=True)
class ColumnIntoBlockExtrapolation:
    columnIndex: int
    blockIndex: tuple[int, int]
    number: int


def findExtrapolationsFromRows(sudoku: Sudoku) -> list[RowIntoBlockExtrapolation]:
    potentialResult = [
        result
        for index in range(1, 10)
        for result in findExtrapolationsFromSingleRow(sudoku.getrow(index))
    ]
    return [
        result
        for result in potentialResult
        if willEliminateRowNumbersInBlock(sudoku.getblock(*result.blockIndex), result)
    ]


def findExtrapolationsFromColumns(sudoku: Sudoku) -> list[ColumnIntoBlockExtrapolation]:
    potentialResult = [
        result
        for index in range(1, 10)
        for result in findExtrapolationsFromSingleColumn(sudoku.getcolumn(index))
    ]
    return [
        result
        for result in potentialResult
        if willEliminateColumnNumbersInBlock(
            sudoku.getblock(*result.blockIndex), result
        )
    ]


def findExtrapolationsFromSingleRow(row: Row) -> list[RowIntoBlockExtrapolation]:
    numbersAndBlocks = getBlocksByNumberFromLine(
        row, lambda x: (lineToBlockIndex(x), lineToBlockIndex(row.index))
    )
    return [
        RowIntoBlockExtrapolation(row.index, next(iter(numbersAndBlocks[key])), key)
        for key in numbersAndBlocks
        if len(numbersAndBlocks[key]) == 1
    ]


def findExtrapolationsFromSingleColumn(
    column: Column,
) -> list[ColumnIntoBlockExtrapolation]:
    numbersAndBlocks = getBlocksByNumberFromLine(
        column, lambda y: (lineToBlockIndex(column.index), lineToBlockIndex(y))
    )
    return [
        ColumnIntoBlockExtrapolation(
            column.index, next(iter(numbersAndBlocks[key])), key
        )
        for key in numbersAndBlocks
        if len(numbersAndBlocks[key]) == 1
    ]


def getBlocksByNumberFromLine(
    line: Line, indexToBlockIndex: Callable[[int], tuple[int, int]]
) -> dict[int, set[tuple[int, int]]]:
    numbersAndBlocks: dict[int, set[tuple[int, int]]] = {
        number: set() for number in range(1, 10)
    }
    cells = [(index, line.get(index)) for index in range(1, 10)]
    emptyCells = [(index, cell) for index, cell in cells if isinstance(cell, EmptyCell)]
    for x, cell in emptyCells:
        blockIndex = indexToBlockIndex(x)
        for possibleNumber in cell.possibleNumbers:
            numbersAndBlocks[possibleNumber].add(blockIndex)
    return numbersAndBlocks


def lineToBlockIndex(index: int):
    return ((index - 1) // 3) + 1


def willEliminateRowNumbersInBlock(block: Block, result: RowIntoBlockExtrapolation):
    blockRow = block.globalToLocalRow(result.rowIndex)
    cellsToCheck = [
        block.get(x, y)
        for x, y in itertools.product(range(1, 4), range(1, 4))
        if y != blockRow
    ]
    return any(
        isinstance(cell, EmptyCell) and cell.couldbe(result.number)
        for cell in cellsToCheck
    )


def willEliminateColumnNumbersInBlock(
    block: Block, result: ColumnIntoBlockExtrapolation
):
    blockColumn = block.globalToLocalColumn(result.columnIndex)
    cellsToCheck = [
        block.get(x, y)
        for x, y in itertools.product(range(1, 4), range(1, 4))
        if x != blockColumn
    ]
    return any(
        isinstance(cell, EmptyCell) and cell.couldbe(result.number)
        for cell in cellsToCheck
    )


def eliminateFromListOfExtrapolatedRows(
    sudoku: Sudoku, extrapolations: list[RowIntoBlockExtrapolation]
):
    for extrapolation in extrapolations:
        sudoku = eliminateFromExtrapolatedRow(sudoku, extrapolation)

    return sudoku


def eliminateFromExtrapolatedRow(
    sudoku: Sudoku, extrapolation: RowIntoBlockExtrapolation
) -> Sudoku:
    block = sudoku.getblock(*extrapolation.blockIndex)
    blockRow = block.globalToLocalRow(extrapolation.rowIndex)

    cellsToUpdate = [
        (block.localToGlobal(x, y), block.get(x, y))
        for x, y in itertools.product(range(1, 4), range(1, 4))
        if y != blockRow
    ]
    cellsToUpdate = [
        (position, cell)
        for position, cell in cellsToUpdate
        if isinstance(cell, EmptyCell)
    ]

    for position, cell in cellsToUpdate:
        sudoku = sudoku.set(*position, cell.eliminate(extrapolation.number))

    return sudoku


def eliminateFromListOfExtrapolatedColumns(
    sudoku: Sudoku, extrapolations: list[ColumnIntoBlockExtrapolation]
):
    for extrapolation in extrapolations:
        sudoku = eliminateFromExtrapolatedColumn(sudoku, extrapolation)

    return sudoku


def eliminateFromExtrapolatedColumn(
    sudoku: Sudoku, extrapolation: ColumnIntoBlockExtrapolation
) -> Sudoku:
    block = sudoku.getblock(*extrapolation.blockIndex)
    blockColumn = block.globalToLocalColumn(extrapolation.columnIndex)

    cellsToUpdate = [
        (block.localToGlobal(x, y), block.get(x, y))
        for x, y in itertools.product(range(1, 4), range(1, 4))
        if x != blockColumn
    ]
    cellsToUpdate = [
        (position, cell)
        for position, cell in cellsToUpdate
        if isinstance(cell, EmptyCell)
    ]

    for position, cell in cellsToUpdate:
        sudoku = sudoku.set(*position, cell.eliminate(extrapolation.number))

    return sudoku
