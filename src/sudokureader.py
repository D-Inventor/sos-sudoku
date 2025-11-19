from src.sudoku import Sudoku


def sudoku_from_file(filename: str) -> Sudoku:
    lines: list[list[int | None]] = []
    with open(filename) as file:
        while line := file.readline():
            lines.append(sudoku_line_to_list(line))

    return Sudoku.fromarray(lines)


def sudoku_line_to_list(line: str) -> list[int | None]:
    return [sudoku_character_to_number(x) for x in line]


def sudoku_character_to_number(char: str) -> int | None:
    return int(char) if char.isdigit() else None
