from src.block import Block
from src.cell import Cell, FullCell


def test_block_contains_number():
    cells: dict[tuple[int, int], Cell] = {}
    cells[(2, 2)] = FullCell(6)
    block = Block((0, 0), cells)

    assert block.contains(6)


def test_block_does_not_contain_number():
    cells: dict[tuple[int, int], Cell] = {}
    cells[(2, 2)] = FullCell(6)
    block = Block((0, 0), cells)

    assert not block.contains(3)
