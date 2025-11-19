from src.cell import Cell, EmptyCell, FullCell
from src.line import Column, Row
from src.sudoku import Sudoku
from src.sudokuextrapolateline import (
    ColumnIntoBlockExtrapolation,
    RowIntoBlockExtrapolation,
    eliminate_from_extrapolated_column,
    eliminate_from_extrapolated_row,
    find_extrapolations_from_columns,
    find_extrapolations_from_rows,
    find_extrapolations_from_single_column,
    find_extrapolations_from_single_row,
)


def test_finds_number_in_row_in_single_block():
    # given
    empty_cell_without_three = EmptyCell.create().eliminate(3)
    cells: dict[int, Cell] = dict()
    cells[1] = FullCell(5)
    cells[4] = empty_cell_without_three
    cells[5] = empty_cell_without_three
    cells[6] = FullCell(9)
    cells[7] = empty_cell_without_three
    cells[8] = FullCell(7)
    cells[9] = empty_cell_without_three

    row = Row(4, cells)

    # when
    result = find_extrapolations_from_single_row(row)

    # then
    assert RowIntoBlockExtrapolation(4, (1, 2), 3) in result


def test_remove_extrapolation_that_does_not_eliminate_any_options():
    sudoku = Sudoku.fromarray(
        [
            [8, None, None, 9, None, None, None, None, None],
            [None, None, None, None, 4, None, 5, None, None],
            [None, None, None, 7, None, None, None, None, None],
            [None, 8, None, None, 5, 9, None, None, None],
            [None, None, None, 6, 3, 8, None, None, None],
            [None, 2, None, None, None, None, None, 3, None],
            [None, None, None, None, None, None, 8, None, None],
            [3, 5, None, None, None, None, None, None, None],
            [None, None, None, 8, 1, None, None, None, None],
        ]
    )

    result = find_extrapolations_from_rows(sudoku)

    assert RowIntoBlockExtrapolation(4, (1, 2), 3) not in result


def test_eliminates_extrapolated_numbers():
    sudoku = Sudoku.fromarray(
        [
            [8, None, None, 9, None, None, None, None, None],
            [None, None, None, None, 4, None, 5, None, None],
            [None, None, None, 7, None, None, None, None, None],
            [None, 8, None, None, 5, 9, None, None, None],
            [None, None, None, 6, 3, 8, None, None, None],
            [None, 2, None, None, None, None, None, 3, None],
            [None, None, None, None, None, None, 8, None, None],
            [3, 5, None, None, None, None, None, None, None],
            [None, None, None, 8, 1, None, None, None, None],
        ]
    )

    result = find_extrapolations_from_rows(sudoku)
    for item in result:
        sudoku = eliminate_from_extrapolated_row(sudoku, item)

    assert not sudoku.get(8, 3).couldbe(8)


def test_finds_number_in_column_in_single_block():
    # given
    empty_cell_without_three = EmptyCell.create().eliminate(3)
    cells: dict[int, Cell] = dict()
    cells[1] = FullCell(5)
    cells[4] = empty_cell_without_three
    cells[5] = empty_cell_without_three
    cells[6] = FullCell(9)
    cells[7] = empty_cell_without_three
    cells[8] = FullCell(7)
    cells[9] = empty_cell_without_three

    column = Column(4, cells)

    # when
    result = find_extrapolations_from_single_column(column)

    # then
    assert ColumnIntoBlockExtrapolation(4, (2, 1), 3) in result


def test_remove_extrapolation_that_does_not_eliminate_any_options():
    sudoku = Sudoku.fromarray(
        [
            [8, None, None, 9, None, None, None, None, None],
            [None, None, None, None, 4, None, 5, None, None],
            [None, None, None, 7, None, None, None, None, None],
            [None, 8, None, None, 5, 9, None, None, None],
            [None, None, None, 6, 8, 3, None, None, None],
            [None, 2, None, None, None, None, None, 3, None],
            [None, None, None, None, 3, None, 8, None, None],
            [3, 5, None, None, None, None, None, None, None],
            [None, None, None, 8, 1, None, None, None, None],
        ]
    )

    result = find_extrapolations_from_columns(sudoku)

    assert ColumnIntoBlockExtrapolation(4, (2, 1), 3) not in result


def test_eliminates_extrapolated_numbers():
    sudoku = Sudoku.fromarray(
        [
            [None, None, None, 9, None, None, None, None, None],
            [None, None, None, None, 4, None, 5, None, None],
            [None, None, None, 7, None, None, None, None, None],
            [None, 8, None, None, 5, 9, None, None, 6],
            [None, None, None, 6, 3, 8, None, None, None],
            [None, 2, None, None, None, None, None, 3, 7],
            [None, None, None, None, None, None, 8, None, None],
            [3, 5, None, None, None, None, None, None, None],
            [None, None, None, 8, 1, None, None, None, None],
        ]
    )

    result = find_extrapolations_from_columns(sudoku)
    for item in result:
        sudoku = eliminate_from_extrapolated_column(sudoku, item)

    assert not sudoku.get(8, 3).couldbe(8)
