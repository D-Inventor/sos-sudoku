from src.sudoku import Sudoku


def sudokuFromFile(filename:str) -> Sudoku:
    lines:list[list[int|None]] = []
    with open(filename) as file:
        while line := file.readline():
            lines.append(sudokuLineToList(line))

    return Sudoku.fromarray(lines)

def sudokuLineToList(line:str) -> list[int|None]:
    return [sudokuCharacterToNumber(x) for x in line]

def sudokuCharacterToNumber(char:str):
    return int(char) if char.isdigit() else None