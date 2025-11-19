from src.higlights import FieldPointer

from .cell import Cell, EmptyCell
from .line import Row
from .sudoku import Sudoku

sudokuTop = "┏━━━━━━━┳━━━━━━━┳━━━━━━━┓"
sudokuMiddle = "┣━━━━━━━╋━━━━━━━╋━━━━━━━┫"
sudokuBottom = "┗━━━━━━━┻━━━━━━━┻━━━━━━━┛"


def printSudoku(sudoku: Sudoku, highlights: list[FieldPointer]) -> str:
    result = sudokuTop + "\n"
    for y in range(1, 10):
        result = result + printSudokuRow(sudoku.getrow(y), y, highlights) + "\n"
        if y < 9 and (y % 3) == 0:
            result = result + sudokuMiddle + "\n"

    result = result + sudokuBottom
    return result


# def printSudokuRow(row: Row):
#     result:str = ""
#     for i in range(0, 3):
#         result = result + "┃ "
#         for j in range(1, 4):
#             result = result + printSudokuCell(row.get((i * 3) + j)) + " "
#     result = result + "┃\n"
#     return result


def printSudokuRow(row: Row, y: int, highlight: list[FieldPointer]) -> str:
    result: str = ""
    for x in range(1, 10):
        cell = row.get(x)
        position = (x, y)
        if x % 3 == 1:
            result = result + "┃"
        result = result + printSudokuBeforeCell(cell, position, highlight)
        result = result + printSudokuCell(cell, position, highlight)
        if x % 3 == 0:
            result = result + printSudokuAfterCell(cell, position, highlight)
    result = result + "┃"
    return result


def printSudokuBeforeCell(
    cell: Cell, position: tuple[int, int], highlights: list[FieldPointer]
) -> str:
    (x, y) = position
    value = None
    if x % 3 != 1:
        value = next(
            (
                val
                for val in [
                    highlight.getAfter(cell, (x - 1, y)) for highlight in highlights
                ]
                if val is not None
            ),
            None,
        )
    if value is None:
        value = next(
            (
                val
                for val in [
                    highlight.getBefore(cell, position) for highlight in highlights
                ]
                if val is not None
            ),
            None,
        )
    return value if value is not None else " "


def printSudokuCell(
    cell: Cell, position: tuple[int, int], highlight: list[FieldPointer]
) -> str:
    return " " if isinstance(cell, EmptyCell) else str(cell.value)


def printSudokuAfterCell(
    cell: Cell, position: tuple[int, int], highlights: list[FieldPointer]
) -> str:
    return next(
        (
            val
            for val in [highlight.getAfter(cell, position) for highlight in highlights]
            if val is not None
        ),
        " ",
    )
