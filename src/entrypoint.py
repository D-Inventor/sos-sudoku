from os import path

from src.higlights import FieldPointer
from src.sudokuextrapolateline import (
    eliminateFromListOfExtrapolatedColumns,
    eliminateFromListOfExtrapolatedRows,
    findExtrapolationsFromColumns,
    findExtrapolationsFromRows,
)
from src.sudokufinder import (
    findCellsWithSingleOption,
    findCellsWithUniqueNumberInBlocks,
    findCellsWithUniqueNumberInColumns,
    findCellsWithUniqueNumberInRows,
)
from src.sudokuprinter import printSudoku
from src.sudokureader import sudokuFromFile


def entrypoint() -> None:
    sudoku = sudokuFromFile(path.join("puzzles", "13.txt"))

    oldSudoku = None
    newSudoku = sudoku
    while oldSudoku is not newSudoku:
        oldSudoku = newSudoku
        extrapolations = findExtrapolationsFromRows(oldSudoku)
        newSudoku = eliminateFromListOfExtrapolatedRows(newSudoku, extrapolations)

        extrapolations = findExtrapolationsFromColumns(oldSudoku)
        newSudoku = eliminateFromListOfExtrapolatedColumns(newSudoku, extrapolations)

    positions = set()
    positions = positions | {position for position in findCellsWithSingleOption(sudoku)}
    positions = positions | {
        position for position in findCellsWithUniqueNumberInRows(sudoku)
    }
    positions = positions | {
        position for position in findCellsWithUniqueNumberInColumns(sudoku)
    }
    positions = positions | {
        position for position in findCellsWithUniqueNumberInBlocks(sudoku)
    }

    highlights = [FieldPointer(position) for position in positions]

    output = printSudoku(sudoku, highlights)
    print(output)
