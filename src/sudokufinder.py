import itertools

from src.block import Block
from src.cell import Cell, EmptyCell
from src.line import Column, Line, Row
from src.sudoku import Sudoku


def find_cells_with_single_option(sudoku: Sudoku) -> list[tuple[int, int]]:
    return [
        position
        for position, cell in sudoku.cells
        if cell_has_one_possible_number(cell)
    ]


def cell_has_one_possible_number(cell: Cell) -> bool:
    return isinstance(cell, EmptyCell) and len(cell.possible_numbers) == 1


def find_cells_with_unique_number_in_rows(sudoku: Sudoku) -> list[tuple[int, int]]:
    return [
        position
        for y in range(1, 10)
        for position in find_cells_with_unique_number_in_single_row(sudoku.getrow(y))
    ]


def find_cells_with_unique_number_in_single_row(row: Row) -> list[tuple[int, int]]:
    return [
        row.local_to_global(x) for x in find_indexes_for_unique_numbers_in_line(row)
    ]


def find_cells_with_unique_number_in_columns(sudoku: Sudoku) -> list[tuple[int, int]]:
    return [
        position
        for x in range(1, 10)
        for position in find_cells_with_unique_number_in_single_column(
            sudoku.getcolumn(x)
        )
    ]


def find_cells_with_unique_number_in_single_column(
    column: Column,
) -> list[tuple[int, int]]:
    return [
        column.local_to_global(y)
        for y in find_indexes_for_unique_numbers_in_line(column)
    ]


def find_indexes_for_unique_numbers_in_line(line: Line) -> list[int]:
    numbers = {key: [] for key in range(1, 10)}
    for index, cell in [(index, line.get(index)) for index in range(1, 10)]:
        if isinstance(cell, EmptyCell):
            for possible_number in cell.possible_numbers:
                numbers[possible_number].append(index)

    return [
        index
        for number in numbers
        if len(numbers[number]) == 1
        for index in numbers[number]
    ]


def find_cells_with_unique_number_in_blocks(sudoku: Sudoku) -> list[tuple[int, int]]:
    return [
        position
        for (x, y) in itertools.product(range(1, 4), range(1, 4))
        for position in find_cells_with_unique_number_in_single_block(
            sudoku.getblock(x, y)
        )
    ]


def find_cells_with_unique_number_in_single_block(
    block: Block,
) -> list[tuple[int, int]]:
    numbers = {key: [] for key in range(1, 10)}
    for x, y, cell in [
        (x, y, block.get(x, y))
        for (x, y) in itertools.product(range(1, 4), range(1, 4))
    ]:
        if isinstance(cell, EmptyCell):
            for possible_number in cell.possible_numbers:
                numbers[possible_number].append((x, y))
    return [
        block.local_to_global(x, y)
        for number in numbers
        if len(numbers[number]) == 1
        for x, y in numbers[number]
    ]
