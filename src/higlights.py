"""Module defining a highlight that points to a specific cell in the Sudoku grid."""

from termcolor import colored


class FieldPointer:
    """A type of highlight that points to a specific cell in the Sudoku grid."""

    def __init__(self, position: tuple[int, int]) -> None:
        self._position = position

    def get_before(self, position: tuple[int, int]) -> str | None:
        """Gets the highlight before the cell if it matches the pointer's position."""
        if position == self._position:
            return colored(">", "light_green")
        return None

    def get_after(self, position: tuple[int, int]) -> str | None:
        """Gets the highlight after the cell if it matches the pointer's position."""
        if position == self._position:
            return colored("<", "light_green")
        return None
