from src.higlights import FieldPointer
from src.sudoku import Sudoku
from src.sudokuprinter import printSudoku


def test_prints_empty_sudoku():
    # given
    sudoku = Sudoku.empty()

    # when
    result = printSudoku(sudoku, [])

    # then
    expected = """┏━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┗━━━━━━━┻━━━━━━━┻━━━━━━━┛"""
    assert result == expected


def test_prints_full_sudoku():
    # given
    sudoku = Sudoku.fromarray(
        [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 4, 5, 6, 7, 8, 9, 1],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
        ]
    )

    # when
    result = printSudoku(sudoku, [])

    # then
    expected = """┏━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ 1 2 3 ┃ 4 5 6 ┃ 7 8 9 ┃
┃ 4 5 6 ┃ 7 8 9 ┃ 1 2 3 ┃
┃ 7 8 9 ┃ 1 2 3 ┃ 4 5 6 ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃ 2 3 4 ┃ 5 6 7 ┃ 8 9 1 ┃
┃ 5 6 7 ┃ 8 9 1 ┃ 2 3 4 ┃
┃ 8 9 1 ┃ 2 3 4 ┃ 5 6 7 ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃ 3 4 5 ┃ 6 7 8 ┃ 9 1 2 ┃
┃ 6 7 8 ┃ 9 1 2 ┃ 3 4 5 ┃
┃ 9 1 2 ┃ 3 4 5 ┃ 6 7 8 ┃
┗━━━━━━━┻━━━━━━━┻━━━━━━━┛"""
    assert result == expected


def test_prints_highlight():
    # given
    sudoku = Sudoku.empty()

    # when
    result = printSudoku(sudoku, [FieldPointer((8, 2))])

    # then
    expected = """┏━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃       ┃       ┃       ┃
┃       ┃       ┃  > <  ┃
┃       ┃       ┃       ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┗━━━━━━━┻━━━━━━━┻━━━━━━━┛"""
    assert result == expected


def test_prints_highlight_at_block_edge():
    # given
    sudoku = Sudoku.empty()

    # when
    result = printSudoku(sudoku, [FieldPointer((6, 2))])

    # then
    expected = """┏━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃       ┃       ┃       ┃
┃       ┃    > <┃       ┃
┃       ┃       ┃       ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┣━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┃       ┃       ┃       ┃
┗━━━━━━━┻━━━━━━━┻━━━━━━━┛"""
    assert result == expected
