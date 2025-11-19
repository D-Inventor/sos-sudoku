"""Module for reading Sudoku puzzles from files."""

from src.sudoku import Sudoku


def sudoku_from_file(filename: str) -> Sudoku:
    """Reads a Sudoku puzzle from a file."""
    lines: list[list[int | None]] = []
    with open(filename, encoding="utf-8") as file:
        while line := file.readline():
            lines.append(sudoku_line_to_list(line))

    return Sudoku.fromarray(lines)


def sudoku_line_to_list(line: str) -> list[int | None]:
    """Converts a line from the Sudoku file into a list of numbers."""
    return [sudoku_character_to_number(x) for x in line]


def sudoku_character_to_number(char: str) -> int | None:
    """Converts a character from the Sudoku file into a number."""
    return int(char) if char.isdigit() else None
