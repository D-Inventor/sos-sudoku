from src.higlights import FieldPointer

from .cell import Cell, EmptyCell
from .line import Row
from .sudoku import Sudoku

SUDOKU_TOP = "┏━━━━━━━┳━━━━━━━┳━━━━━━━┓"
SUDOKU_MIDDLE = "┣━━━━━━━╋━━━━━━━╋━━━━━━━┫"
SUDOKU_BOTTOM = "┗━━━━━━━┻━━━━━━━┻━━━━━━━┛"


def print_sudoku(sudoku: Sudoku, highlights: list[FieldPointer]) -> str:
    result = SUDOKU_TOP + "\n"
    for y in range(1, 10):
        result = result + print_sudoku_row(sudoku.getrow(y), y, highlights) + "\n"
        if y < 9 and (y % 3) == 0:
            result = result + SUDOKU_MIDDLE + "\n"

    result = result + SUDOKU_BOTTOM
    return result


# def print_sudoku_row(row: Row):
#     result:str = ""
#     for i in range(0, 3):
#         result = result + "┃ "
#         for j in range(1, 4):
#             result = result + print_sudoku_cell(row.get((i * 3) + j)) + " "
#     result = result + "┃\n"
#     return result


def print_sudoku_row(row: Row, y: int, highlight: list[FieldPointer]) -> str:
    result: str = ""
    for x in range(1, 10):
        cell = row.get(x)
        position = (x, y)
        if x % 3 == 1:
            result = result + "┃"
        result = result + print_sudoku_before_cell(position, highlight)
        result = result + print_sudoku_cell(cell)
        if x % 3 == 0:
            result = result + print_sudoku_after_cell(position, highlight)
    result = result + "┃"
    return result


def print_sudoku_before_cell(
    position: tuple[int, int], highlights: list[FieldPointer]
) -> str:
    (x, y) = position
    value = None
    if x % 3 != 1:
        value = next(
            (
                val
                for val in [highlight.get_after((x - 1, y)) for highlight in highlights]
                if val is not None
            ),
            None,
        )
    if value is None:
        value = next(
            (
                val
                for val in [highlight.get_before(position) for highlight in highlights]
                if val is not None
            ),
            None,
        )
    return value if value is not None else " "


def print_sudoku_cell(cell: Cell) -> str:
    return " " if isinstance(cell, EmptyCell) else str(cell.value)


def print_sudoku_after_cell(
    position: tuple[int, int], highlights: list[FieldPointer]
) -> str:
    return next(
        (
            val
            for val in [highlight.get_after(position) for highlight in highlights]
            if val is not None
        ),
        " ",
    )
