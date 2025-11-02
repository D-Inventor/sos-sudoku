from dataclasses import dataclass

from src.block import Block


@dataclass(frozen=True)
class BlockIntoRowExtrapolation:
    rowIndex: int
    blockIndex: tuple[int, int]
    number: int


@dataclass(frozen=True)
class BlockIntoColumnExtrapolation:
    columnIndex: int
    blockIndex: tuple[int, int]
    number: int


def findExtrapolationsFromSingleBlock(
    block: Block,
) -> list[BlockIntoRowExtrapolation | BlockIntoColumnExtrapolation]:
    return []
