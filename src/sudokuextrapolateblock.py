from dataclasses import dataclass

from src.block import Block


@dataclass(frozen=True)
class BlockIntoRowExtrapolation:
    row_index: int
    block_index: tuple[int, int]
    number: int


@dataclass(frozen=True)
class BlockIntoColumnExtrapolation:
    column_index: int
    block_index: tuple[int, int]
    number: int


def find_extrapolations_from_single_block(
    block: Block,
) -> list[BlockIntoRowExtrapolation | BlockIntoColumnExtrapolation]:
    return []
