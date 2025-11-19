import pytest

from src.sudokureader import sudokuLineToList


@pytest.mark.parametrize(
    "input,expected",
    [
        ("123456789", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("987654321", [9, 8, 7, 6, 5, 4, 3, 2, 1]),
        ("1.3.5.7.9", [1, None, 3, None, 5, None, 7, None, 9]),
    ],
)
def test_read_string_as_line_of_numbers(input: str, expected: list[int | None]):
    result = sudokuLineToList(input)
    assert result == expected
