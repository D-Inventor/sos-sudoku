"""Module representing a collection of Sudoku cells."""

from src.cell import Cell, FullCell


class CellCollection:
    """Abstract base class for a collection of Sudoku cells."""

    @property
    def cells(self) -> list[Cell]:
        """When implemented by a type, returns the list of cells in the collection."""
        raise NotImplementedError(
            "property 'cells' must be implemented by derived type"
        )

    def contains(self, number: int) -> bool:
        """Checks if the collection contains a cell with the given number."""
        return number in [
            cell.value for cell in self.cells if isinstance(cell, FullCell)
        ]
