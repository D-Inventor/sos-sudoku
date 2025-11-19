import pytest

from src.cell import EmptyCell, FullCell
from src.sudoku import Sudoku


class TestSudokuConstructor:
    def test_creates_empty_sudoku(self):
        # given

        # when
        sudoku = Sudoku.empty()

        # then
        for cell in sudoku.cells:
            assert isinstance(cell, EmptyCell)

    @pytest.mark.parametrize("x,y,expected", [(1, 1, 1), (2, 3, 8), (5, 9, 4)])
    def test_creates_from_2D_array(self, x: int, y: int, expected: int):
        # given
        value = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 4, 5, 6, 7, 8, 9, 1],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
        ]

        # when
        sudoku = Sudoku.fromarray(value)

        # then
        assert sudoku.get(x, y).value == expected

    def test_creates_empty_cell_from_none(self):
        # given
        value: list[list[int | None]] = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 4, 5, 6, 7, 8, 9, 1],
            [5, 6, 7, 8, None, 1, 2, 3, 4],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
        ]

        # when
        sudoku = Sudoku.fromarray(value)

        # then
        assert isinstance(sudoku.get(5, 5), EmptyCell)

    def test_creates_empty_cells_with_valid_possible_numbers(self):
        # given
        value = [
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, 4, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, 5, 9, None, None, None],
            [None, None, None, 6, None, 8, None, None, None],
            [None, 2, None, None, None, None, None, 3, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, 1, None, None, None, None],
        ]

        # when
        sudoku = Sudoku.fromarray(value)

        # then
        assert not sudoku.get(5, 6).couldbe(5)


class TestSudokuSet:
    def test_can_set_cell_by_location(self):
        # given
        sudoku = Sudoku.empty()

        # when
        sudoku = sudoku.set(3, 4, 8)

        # then
        assert isinstance(sudoku.get(3, 4), FullCell)

    def test_number_is_stored_in_cell(self):
        # given
        sudoku = Sudoku.empty()

        # when
        sudoku = sudoku.set(3, 4, 8)

        # then
        assert sudoku.get(3, 4).value == 8

    def test_set_creates_new_sudoku(self):
        # given
        sudoku = Sudoku.empty()

        # when
        new_sudoku = sudoku.set(3, 4, 8)

        # then
        assert new_sudoku is not sudoku

    def test_set_does_not_affect_old_sudoku(self):
        # given
        sudoku = Sudoku.empty()

        # when
        sudoku.set(3, 4, 8)

        # then
        assert isinstance(sudoku.get(3, 4), EmptyCell)

    def test_cannot_set_number_if_number_already_in_row(self):
        sudoku = Sudoku.empty().set(4, 6, FullCell(7))

        with pytest.raises(ValueError):
            sudoku.set(8, 6, FullCell(7))

    def test_cannot_set_number_if_number_already_in_column(self):
        sudoku = Sudoku.empty().set(4, 6, FullCell(7))

        with pytest.raises(ValueError):
            sudoku.set(4, 8, FullCell(7))

    def test_cannot_set_number_if_number_already_in_block(self):
        sudoku = Sudoku.empty().set(4, 6, FullCell(7))

        with pytest.raises(ValueError):
            sudoku.set(5, 4, FullCell(7))

    @pytest.mark.parametrize("x,y", [(10, 5), (0, 5), (5, 10), (5, 0)])
    def test_cannot_set_value_outside_of_bounds(self, x: int, y: int):
        sudoku = Sudoku.empty()

        with pytest.raises(ValueError):
            sudoku.set(x, y, 3)

    def test_can_override_cell_with_value(self):
        sudoku = Sudoku.empty().set(3, 4, 8)

        sudoku = sudoku.set(3, 4, EmptyCell.create())

        assert isinstance(sudoku.get(3, 4), EmptyCell)

    @pytest.mark.parametrize("x,y", [(8, 4), (3, 1), (2, 5)])
    def test_set_eliminates_number_from_empty_cells(self, x: int, y: int):
        sudoku = Sudoku.empty()

        sudoku = sudoku.set(3, 4, FullCell(5))

        assert not sudoku.get(x, y).couldbe(5)


class TestSudokuGet:
    def test_cell_is_empty_by_default(self):
        # given / when
        sudoku = Sudoku.empty()

        # then
        assert isinstance(sudoku.get(3, 4), EmptyCell)


class TestSudokuGetRow:
    def test_getrow_returns_row_from_sudoku(self):
        sudoku = Sudoku.empty().set(2, 4, FullCell(7)).set(6, 4, FullCell(8))

        result = sudoku.getrow(4)

        assert result.get(2).value == 7
        assert result.get(6).value == 8


class TestSudokuGetColumn:
    def test_getcolumn_returns_column_from_sudoku(self):
        sudoku = Sudoku.empty().set(4, 2, FullCell(7)).set(4, 6, FullCell(9))

        result = sudoku.getcolumn(4)

        assert result.get(2).value == 7
        assert result.get(6).value == 9
