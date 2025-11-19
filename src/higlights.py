from termcolor import colored


class FieldPointer:
    def __init__(self, position: tuple[int, int]) -> None:
        self._position = position

    def get_before(self, position: tuple[int, int]) -> str | None:
        if position == self._position:
            return colored(">", "light_green")
        return None

    def get_after(self, position: tuple[int, int]) -> str | None:
        if position == self._position:
            return colored("<", "light_green")
        return None
