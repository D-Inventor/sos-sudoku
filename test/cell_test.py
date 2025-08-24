import pytest

from src.cell import EmptyCell, FullCell


def test_can_create_full_cell():
    # given / when
    cell = FullCell(5)

    # then
    assert cell.value == 5

@pytest.mark.parametrize("value", [10, 0])
def test_cannot_create_cell_with_value_outside_bounds(value: int):
    with pytest.raises(ValueError):
        FullCell(value)

@pytest.mark.parametrize("number", range(1, 10))
def test_empty_cell_can_be_any_number_by_default(number:int):
    # given / when
    cell = EmptyCell.create()

    # then
    assert cell.couldbe(number)

@pytest.mark.parametrize("number", [0, 10])
def test_empty_cell_can_never_be_out_of_bounds(number:int):
    # given / when
    cell = EmptyCell.create()

    # then
    assert not cell.couldbe(number)

def test_empty_cell_cannot_be_eliminated_number():
    # given / when
    cell = EmptyCell.create().eliminate(4)

    # then
    assert not cell.couldbe(4)

@pytest.mark.parametrize("number", [0, 10])
def test_cannot_eliminate_number_out_of_bounds(number:int):
    cell = EmptyCell.create()
    with pytest.raises(ValueError):
        cell.eliminate(number)

def test_eliminate_creates_new_instance():
    cell = EmptyCell.create()
    othercell = cell.eliminate(4)

    assert cell is not othercell

def test_eliminate_does_not_affect_old_cell():
    cell = EmptyCell.create()
    cell.eliminate(4)

    assert cell.couldbe(4)

def test_can_reconsider_number():
    cell = EmptyCell.create().eliminate(4).reconsider(4)

    assert cell.couldbe(4)

def test_can_reconsider_number_that_was_already_possible():
    cell = EmptyCell.create().reconsider(4)

    assert cell.couldbe(4)

def test_reconsider_does_not_affect_old_cell():
    cell = EmptyCell.create().eliminate(4)
    cell.reconsider(4)

    assert not cell.couldbe(4)

@pytest.mark.parametrize("number",[0, 10])
def test_cannot_reconsider_number_out_of_bounds(number:int):
    cell = EmptyCell.create()
    with pytest.raises(ValueError):
        cell.reconsider(number)
