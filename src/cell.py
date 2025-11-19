from typing import Union


class EmptyCell:
    def __init__(self, eliminated: set[int]) -> None:
        self._eliminated: set[int] = eliminated

    def couldbe(self, number: int) -> bool:
        if number < 1 or number > 9:
            return False
        return number not in self._eliminated

    def eliminate(self, number: int) -> "EmptyCell":
        if number < 1 or number > 9:
            raise ValueError("Number must be between 1 and 9")
        eliminated = self._eliminated.copy()
        eliminated.add(number)
        return EmptyCell(eliminated)

    def reconsider(self, number: int) -> "EmptyCell":
        if number < 1 or number > 9:
            raise ValueError("Number must be between 1 and 9")
        if number in self._eliminated:
            eliminated = self._eliminated.copy()
            eliminated.remove(number)
            return EmptyCell(eliminated)
        return self

    @property
    def possible_numbers(self) -> list[int]:
        return [number for number in range(1, 10) if number not in self._eliminated]

    @staticmethod
    def create() -> "EmptyCell":
        return EmptyCell(set())


class FullCell:
    def __init__(self, value: int) -> None:
        if value > 9 or value < 1:
            raise ValueError("Value must be between 1 and 9")
        self._value = value

    @property
    def value(self) -> int:
        return self._value


type Cell = Union[EmptyCell, FullCell]
