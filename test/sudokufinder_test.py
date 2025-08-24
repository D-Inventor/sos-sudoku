from src.sudoku import Sudoku
from src.sudokufinder import findCellsWithSingleOption, findCellsWithUniqueNumberInBlocks, findCellsWithUniqueNumberInColumns, findCellsWithUniqueNumberInRows


def test_finds_cell_with_only_one_possible_number():
    sudoku = Sudoku.fromarray([
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, 4,    None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, 5,    9,    None, None, None],
        [None, None, None, 6,    None, 8,    None, None, None],
        [None, 2,    None, None, None, None, None, 3,    None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, 1,    None, None, None, None],
    ])

    result = findCellsWithSingleOption(sudoku)

    assert (5, 6) in result

def test_finds_cell_with_unique_value_in_row():
    sudoku = Sudoku.fromarray([
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, 4,    None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, 8,    None, None, 5,    9,    None, None, None],
        [None, None, None, 6,    None, 8,    None, None, None],
        [None, 2,    None, None, None, None, None, 3,    None],
        [None, None, None, None, None, None, 8,    None, None],
        [3   , None, None, None, None, None, None, None, None],
        [None, None, None, 8,    1,    None, None, None, None],
    ])

    result = findCellsWithUniqueNumberInRows(sudoku)

    assert (3, 8) in result

def test_finds_cell_with_unique_value_in_column():
    sudoku = Sudoku.fromarray([
        [None, None, None, 9,    None, None, None, None, None],
        [None, None, None, None, 4,    None, 5,    None, None],
        [None, None, None, 7,    None, None, None, None, None],
        [None, 8,    None, None, 5,    9,    None, None, None],
        [None, None, None, 6,    None, 8,    None, None, None],
        [None, 2,    None, None, None, None, None, 3,    None],
        [None, None, None, None, None, None, 8,    None, None],
        [3   , None, 5,    None, None, None, None, None, None],
        [None, None, None, 8,    1,    None, None, None, None],
    ])

    result = findCellsWithUniqueNumberInColumns(sudoku)

    assert (4, 7) in result

def test_finds_cell_with_unique_value_in_block():
    sudoku = Sudoku.fromarray([
        [8,    None, None, 9,    None, None, None, None, None],
        [None, None, None, None, 4,    None, 5,    None, None],
        [None, None, None, 7,    None, None, None, None, None],
        [None, 8,    None, None, 5,    9,    None, None, None],
        [None, None, None, 6,    None, 8,    None, None, None],
        [None, 2,    None, None, None, None, None, 3,    None],
        [None, None, None, None, None, None, 8,    None, None],
        [3   , 5,    None, None, None, None, None, None, None],
        [None, None, None, 8,    1,    None, None, None, None],
    ])

    result = findCellsWithUniqueNumberInBlocks(sudoku)

    assert (5, 3) in result