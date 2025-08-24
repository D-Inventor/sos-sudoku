from src.higlights import FieldPointer
from src.sudokufinder import findCellsWithSingleOption, findCellsWithUniqueNumberInBlocks, findCellsWithUniqueNumberInColumns, findCellsWithUniqueNumberInRows
from src.sudokuprinter import printSudoku
from src.sudokureader import sudokuFromFile

if __name__ == '__main__':
    
    sudoku = sudokuFromFile("35.txt")

    positions = set()
    positions = positions | {position for position in findCellsWithSingleOption(sudoku)}
    positions = positions | {position for position in findCellsWithUniqueNumberInRows(sudoku)}
    positions = positions | {position for position in findCellsWithUniqueNumberInColumns(sudoku)}
    positions = positions | {position for position in findCellsWithUniqueNumberInBlocks(sudoku)}
    highlights = [FieldPointer(position) for position in positions]

    output = printSudoku(sudoku, highlights)
    print(output)