"""Main module of the Sudoku solver program."""

from os import path

from src.higlights import FieldPointer
from src.sudokuextrapolateline import (
    eliminate_from_list_of_extrapolated_columns,
    eliminate_from_list_of_extrapolated_rows,
    find_extrapolations_from_columns,
    find_extrapolations_from_rows,
)
from src.sudokufinder import (
    find_cells_with_single_option,
    find_cells_with_unique_number_in_blocks,
    find_cells_with_unique_number_in_columns,
    find_cells_with_unique_number_in_rows,
)
from src.sudokuprinter import print_sudoku
from src.sudokureader import sudoku_from_file


def main() -> None:
    """Main function of the program."""
    sudoku = sudoku_from_file(path.join("puzzles", "13.txt"))

    old_sudoku = None
    new_sudoku = sudoku
    while old_sudoku is not new_sudoku:
        old_sudoku = new_sudoku
        extrapolations = find_extrapolations_from_rows(old_sudoku)
        new_sudoku = eliminate_from_list_of_extrapolated_rows(
            new_sudoku, extrapolations
        )

        extrapolations = find_extrapolations_from_columns(old_sudoku)
        new_sudoku = eliminate_from_list_of_extrapolated_columns(
            new_sudoku, extrapolations
        )

    positions = set()
    positions = positions | set(find_cells_with_single_option(sudoku))
    positions = positions | set(find_cells_with_unique_number_in_rows(sudoku))
    positions = positions | set(find_cells_with_unique_number_in_columns(sudoku))
    positions = positions | set(find_cells_with_unique_number_in_blocks(sudoku))

    highlights = [FieldPointer(position) for position in positions]

    output = print_sudoku(sudoku, highlights)
    print(output)


if __name__ == "__main__":
    main()
