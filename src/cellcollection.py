from src.cell import Cell, FullCell


class CellCollection:
    @property
    def cells(self) -> list[Cell]:
        raise NotImplementedError(
            "property 'cells' must be implemented by derived type"
        )

    def contains(self, number: int) -> bool:
        return number in [
            cell.value for cell in self.cells if isinstance(cell, FullCell)
        ]
