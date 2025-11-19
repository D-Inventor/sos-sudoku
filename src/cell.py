"""Module representing a cell in a Sudoku puzzle."""

from dataclasses import dataclass
from typing import Union


class EmptyCell:
    """Represents an empty cell in a Sudoku puzzle, tracking eliminated numbers."""

    def __init__(self, eliminated: set[int]) -> None:
        self._eliminated: set[int] = eliminated

    def couldbe(self, number: int) -> bool:
        """Checks if the cell could be a certain number."""
        if number < 1 or number > 9:
            return False
        return number not in self._eliminated

    def eliminate(self, number: int) -> "EmptyCell":
        """Creates a new cell with the given number eliminated."""
        if number < 1 or number > 9:
            raise ValueError("Number must be between 1 and 9")
        eliminated = self._eliminated.copy()
        eliminated.add(number)
        return EmptyCell(eliminated)

    def reconsider(self, number: int) -> "EmptyCell":
        """Creates a new cell with the given number reconsidered."""
        if number < 1 or number > 9:
            raise ValueError("Number must be between 1 and 9")
        if number in self._eliminated:
            eliminated = self._eliminated.copy()
            eliminated.remove(number)
            return EmptyCell(eliminated)
        return self

    @property
    def possible_numbers(self) -> list[int]:
        """Returns a list of possible numbers for this cell."""
        return [number for number in range(1, 10) if number not in self._eliminated]

    @staticmethod
    def create() -> "EmptyCell":
        """Creates a new empty cell with no eliminated numbers."""
        return EmptyCell(set())


@dataclass(frozen=True)
class FullCell:
    """Represents a filled cell in a Sudoku puzzle."""

    value: int

    def __post_init__(self) -> None:
        if self.value > 9 or self.value < 1:
            raise ValueError("Value must be between 1 and 9")


type Cell = Union[EmptyCell, FullCell]
