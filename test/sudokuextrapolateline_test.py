from src.cell import Cell, EmptyCell, FullCell
from src.line import Column, Row
from src.sudoku import Sudoku
from src.sudokuextrapolateline import ColumnIntoBlockExtrapolation, RowIntoBlockExtrapolation, eliminateFromExtrapolatedColumn, eliminateFromExtrapolatedRow, findExtrapolationsFromColumns, findExtrapolationsFromRows, findExtrapolationsFromSingleColumn, findExtrapolationsFromSingleRow


def test_finds_number_in_row_in_single_block():
    # given
    emptyCellWithoutThree = EmptyCell.create().eliminate(3)
    cells:dict[int,Cell] = dict()
    cells[1] = FullCell(5)
    cells[4] = emptyCellWithoutThree
    cells[5] = emptyCellWithoutThree
    cells[6] = FullCell(9)
    cells[7] = emptyCellWithoutThree
    cells[8] = FullCell(7)
    cells[9] = emptyCellWithoutThree
    
    row = Row(4, cells)

    # when
    result = findExtrapolationsFromSingleRow(row)

    # then
    assert RowIntoBlockExtrapolation(4, (1, 2), 3) in result

def test_remove_extrapolation_that_does_not_eliminate_any_options():
    sudoku = Sudoku.fromarray([
        [8,    None, None, 9,    None, None, None, None, None],
        [None, None, None, None, 4,    None, 5,    None, None],
        [None, None, None, 7,    None, None, None, None, None],
        [None, 8,    None, None, 5,    9,    None, None, None],
        [None, None, None, 6,    3,    8,    None, None, None],
        [None, 2,    None, None, None, None, None, 3,    None],
        [None, None, None, None, None, None, 8,    None, None],
        [3   , 5,    None, None, None, None, None, None, None],
        [None, None, None, 8,    1,    None, None, None, None],
    ])

    result = findExtrapolationsFromRows(sudoku)

    assert RowIntoBlockExtrapolation(4, (1, 2), 3) not in result

def test_eliminates_extrapolated_numbers():
    sudoku = Sudoku.fromarray([
        [8,    None, None, 9,    None, None, None, None, None],
        [None, None, None, None, 4,    None, 5,    None, None],
        [None, None, None, 7,    None, None, None, None, None],
        [None, 8,    None, None, 5,    9,    None, None, None],
        [None, None, None, 6,    3,    8,    None, None, None],
        [None, 2,    None, None, None, None, None, 3,    None],
        [None, None, None, None, None, None, 8,    None, None],
        [3   , 5,    None, None, None, None, None, None, None],
        [None, None, None, 8,    1,    None, None, None, None],
    ])

    result = findExtrapolationsFromRows(sudoku)
    for item in result:
        sudoku = eliminateFromExtrapolatedRow(sudoku, item)

    assert not sudoku.get(8, 3).couldbe(8)

def test_finds_number_in_column_in_single_block():
    # given
    emptyCellWithoutThree = EmptyCell.create().eliminate(3)
    cells:dict[int,Cell] = dict()
    cells[1] = FullCell(5)
    cells[4] = emptyCellWithoutThree
    cells[5] = emptyCellWithoutThree
    cells[6] = FullCell(9)
    cells[7] = emptyCellWithoutThree
    cells[8] = FullCell(7)
    cells[9] = emptyCellWithoutThree
    
    column = Column(4, cells)

    # when
    result = findExtrapolationsFromSingleColumn(column)

    # then
    assert ColumnIntoBlockExtrapolation(4, (2, 1), 3) in result

def test_remove_extrapolation_that_does_not_eliminate_any_options():
    sudoku = Sudoku.fromarray([
        [8,    None, None, 9,    None, None, None, None, None],
        [None, None, None, None, 4,    None, 5,    None, None],
        [None, None, None, 7,    None, None, None, None, None],
        [None, 8,    None, None, 5,    9,    None, None, None],
        [None, None, None, 6,    8,    3,    None, None, None],
        [None, 2,    None, None, None, None, None, 3,    None],
        [None, None, None, None, 3,    None, 8,    None, None],
        [3   , 5,    None, None, None, None, None, None, None],
        [None, None, None, 8,    1,    None, None, None, None],
    ])

    result = findExtrapolationsFromColumns(sudoku)

    assert ColumnIntoBlockExtrapolation(4, (2, 1), 3) not in result

def test_eliminates_extrapolated_numbers():
    sudoku = Sudoku.fromarray([
        [None, None, None, 9,    None, None, None, None, None],
        [None, None, None, None, 4,    None, 5,    None, None],
        [None, None, None, 7,    None, None, None, None, None],
        [None, 8,    None, None, 5,    9,    None, None, 6   ],
        [None, None, None, 6,    3,    8,    None, None, None],
        [None, 2,    None, None, None, None, None, 3,    7   ],
        [None, None, None, None, None, None, 8,    None, None],
        [3   , 5,    None, None, None, None, None, None, None],
        [None, None, None, 8,    1,    None, None, None, None],
    ])

    result = findExtrapolationsFromColumns(sudoku)
    for item in result:
        sudoku = eliminateFromExtrapolatedColumn(sudoku, item)

    assert not sudoku.get(8, 3).couldbe(8)