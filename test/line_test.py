import pytest

from src.cell import Cell, EmptyCell, FullCell
from src.line import Line


def test_get_returns_cell_value():
    cells: dict[int, Cell] = {}
    cells[2] = FullCell(4)
    row = Line(1, cells)

    result = row.get(2)

    assert result.value == 4

def test_get_returns_empty_cell_by_default():
    row = Line(1, {})

    result = row.get(4)

    assert isinstance(result, EmptyCell)

@pytest.mark.parametrize("index", [0, 10])
def test_cannot_create_row_out_of_bounds(index:int):
    with pytest.raises(ValueError):
        Line(index, {})

@pytest.mark.parametrize("index", [0, 10])
def test_cannot_get_row_out_of_bounds(index:int):
    row = Line(1, {})
    with pytest.raises(ValueError):
        row.get(index)

def test_can_check_if_number_in_line():
    cells: dict[int, Cell] = {}
    cells[4] = FullCell(6)
    line = Line(1, cells)

    assert line.contains(6)

def test_can_check_if_number_not_in_line():
    cells: dict[int, Cell] = {}
    cells[4] = FullCell(6)
    line = Line(1, cells)

    assert not line.contains(3)