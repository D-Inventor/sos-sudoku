"""Module for eliminating possible numbers by extrapolating lines into blocks."""

import itertools
from dataclasses import dataclass
from typing import Callable

from src.block import Block
from src.cell import EmptyCell
from src.line import Column, Line, Row
from src.sudoku import Sudoku


@dataclass(frozen=True)
class RowIntoBlockExtrapolation:
    """The row and block that were matched with extrapolation"""

    row_index: int
    block_index: tuple[int, int]
    number: int


@dataclass(frozen=True)
class ColumnIntoBlockExtrapolation:
    """The column and block that were matched with extrapolation"""

    column_index: int
    block_index: tuple[int, int]
    number: int


def find_extrapolations_from_rows(sudoku: Sudoku) -> list[RowIntoBlockExtrapolation]:
    """Finds all extrapolations from rows into blocks."""
    potential_result = [
        result
        for index in range(1, 10)
        for result in find_extrapolations_from_single_row(sudoku.getrow(index))
    ]
    return [
        result
        for result in potential_result
        if will_eliminate_row_numbers_in_block(
            sudoku.getblock(*result.block_index), result
        )
    ]


def find_extrapolations_from_columns(
    sudoku: Sudoku,
) -> list[ColumnIntoBlockExtrapolation]:
    """Finds all extrapolations from columns into blocks."""
    potential_result = [
        result
        for index in range(1, 10)
        for result in find_extrapolations_from_single_column(sudoku.getcolumn(index))
    ]
    return [
        result
        for result in potential_result
        if will_eliminate_column_numbers_in_block(
            sudoku.getblock(*result.block_index), result
        )
    ]


def find_extrapolations_from_single_row(row: Row) -> list[RowIntoBlockExtrapolation]:
    """Finds all extrapolations from a single row into blocks."""
    numbers_and_blocks = get_blocks_by_number_from_line(
        row, lambda x: (line_to_block_index(x), line_to_block_index(row.index))
    )
    return [
        RowIntoBlockExtrapolation(row.index, next(iter(numbers_and_blocks[key])), key)
        for key in numbers_and_blocks
        if len(numbers_and_blocks[key]) == 1
    ]


def find_extrapolations_from_single_column(
    column: Column,
) -> list[ColumnIntoBlockExtrapolation]:
    """Finds all extrapolations from a single column into blocks."""
    numbers_and_blocks = get_blocks_by_number_from_line(
        column, lambda y: (line_to_block_index(column.index), line_to_block_index(y))
    )
    return [
        ColumnIntoBlockExtrapolation(
            column.index, next(iter(numbers_and_blocks[key])), key
        )
        for key in numbers_and_blocks
        if len(numbers_and_blocks[key]) == 1
    ]


def get_blocks_by_number_from_line(
    line: Line, index_to_block_index: Callable[[int], tuple[int, int]]
) -> dict[int, set[tuple[int, int]]]:
    """Gets a mapping of numbers to the blocks they appear in for a line."""
    numbers_and_blocks: dict[int, set[tuple[int, int]]] = {
        number: set() for number in range(1, 10)
    }
    cells = [(index, line.get(index)) for index in range(1, 10)]
    empty_cells = [
        (index, cell) for index, cell in cells if isinstance(cell, EmptyCell)
    ]
    for x, cell in empty_cells:
        block_index = index_to_block_index(x)
        for possible_number in cell.possible_numbers:
            numbers_and_blocks[possible_number].add(block_index)
    return numbers_and_blocks


def line_to_block_index(index: int) -> int:
    """Converts a line index to a block index."""
    return ((index - 1) // 3) + 1


def will_eliminate_row_numbers_in_block(
    block: Block, result: RowIntoBlockExtrapolation
) -> bool:
    """Checks if the extrapolation will eliminate numbers in the block."""
    block_row = block.global_to_local_row(result.row_index)
    cells_to_check = [
        block.get(x, y)
        for x, y in itertools.product(range(1, 4), range(1, 4))
        if y != block_row
    ]
    return any(
        isinstance(cell, EmptyCell) and cell.couldbe(result.number)
        for cell in cells_to_check
    )


def will_eliminate_column_numbers_in_block(
    block: Block, result: ColumnIntoBlockExtrapolation
) -> bool:
    """Checks if the extrapolation will eliminate numbers in the block."""
    block_column = block.global_to_local_column(result.column_index)
    cells_to_check = [
        block.get(x, y)
        for x, y in itertools.product(range(1, 4), range(1, 4))
        if x != block_column
    ]
    return any(
        isinstance(cell, EmptyCell) and cell.couldbe(result.number)
        for cell in cells_to_check
    )


def eliminate_from_list_of_extrapolated_rows(
    sudoku: Sudoku, extrapolations: list[RowIntoBlockExtrapolation]
) -> Sudoku:
    """Eliminates possible numbers from a list of row extrapolations."""
    for extrapolation in extrapolations:
        sudoku = eliminate_from_extrapolated_row(sudoku, extrapolation)

    return sudoku


def eliminate_from_extrapolated_row(
    sudoku: Sudoku, extrapolation: RowIntoBlockExtrapolation
) -> Sudoku:
    """Eliminates possible numbers from an extrapolated row."""
    block = sudoku.getblock(*extrapolation.block_index)
    block_row = block.global_to_local_row(extrapolation.row_index)

    cells_to_update = [
        (block.local_to_global(x, y), block.get(x, y))
        for x, y in itertools.product(range(1, 4), range(1, 4))
        if y != block_row
    ]
    cells_to_update = [
        (position, cell)
        for position, cell in cells_to_update
        if isinstance(cell, EmptyCell)
    ]

    for position, cell in cells_to_update:
        sudoku = sudoku.set(*position, cell.eliminate(extrapolation.number))

    return sudoku


def eliminate_from_list_of_extrapolated_columns(
    sudoku: Sudoku, extrapolations: list[ColumnIntoBlockExtrapolation]
) -> Sudoku:
    """Eliminates possible numbers from a list of column extrapolations."""
    for extrapolation in extrapolations:
        sudoku = eliminate_from_extrapolated_column(sudoku, extrapolation)

    return sudoku


def eliminate_from_extrapolated_column(
    sudoku: Sudoku, extrapolation: ColumnIntoBlockExtrapolation
) -> Sudoku:
    """Eliminates possible numbers from an extrapolated column."""
    block = sudoku.getblock(*extrapolation.block_index)
    block_column = block.global_to_local_column(extrapolation.column_index)

    cells_to_update = [
        (block.local_to_global(x, y), block.get(x, y))
        for x, y in itertools.product(range(1, 4), range(1, 4))
        if x != block_column
    ]
    cells_to_update = [
        (position, cell)
        for position, cell in cells_to_update
        if isinstance(cell, EmptyCell)
    ]

    for position, cell in cells_to_update:
        sudoku = sudoku.set(*position, cell.eliminate(extrapolation.number))

    return sudoku
