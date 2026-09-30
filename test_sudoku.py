import unittest
from copy import deepcopy

from Sudoku_Solver import (
    board_is_valid,
    check_valid,
    count_solutions,
    generate_puzzle,
    solve_sudoku,
)


PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


class SudokuTests(unittest.TestCase):
    def test_known_puzzle_solves(self):
        board = deepcopy(PUZZLE)
        self.assertTrue(solve_sudoku(board))
        self.assertTrue(board_is_valid(board))
        self.assertTrue(all(value for row in board for value in row))
        self.assertEqual(board[0], [5, 3, 4, 6, 7, 8, 9, 1, 2])

    def test_invalid_move_is_rejected(self):
        self.assertFalse(check_valid(PUZZLE, 5, (0, 2)))
        self.assertTrue(check_valid(PUZZLE, 4, (0, 2)))

    def test_invalid_board_is_not_solved(self):
        board = deepcopy(PUZZLE)
        board[0][2] = 5
        self.assertFalse(solve_sudoku(board))

    def test_generated_puzzle_has_unique_solution(self):
        puzzle, solution = generate_puzzle(level=35, seed=1234)
        self.assertTrue(board_is_valid(puzzle))
        self.assertEqual(count_solutions(puzzle, limit=2), 1)

        solved = deepcopy(puzzle)
        self.assertTrue(solve_sudoku(solved))
        self.assertEqual(solved, solution)


if __name__ == "__main__":
    unittest.main()
