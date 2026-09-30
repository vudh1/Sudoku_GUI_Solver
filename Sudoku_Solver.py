"""Sudoku generation and solving utilities.

The solver uses backtracking. Puzzle generation removes values from a complete
board only when the puzzle still has exactly one solution.
"""

from copy import deepcopy
from random import Random
from typing import List, Optional, Sequence, Tuple

BOARD_SIZE = 9
BOX_SIZE = 3
DIGITS = tuple(range(1, 10))
Board = List[List[int]]
Position = Tuple[int, int]


def create_empty_board() -> Board:
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def _shape_is_valid(board: Sequence[Sequence[int]]) -> bool:
    return (
        len(board) == BOARD_SIZE
        and all(len(row) == BOARD_SIZE for row in board)
        and all(isinstance(value, int) and 0 <= value <= 9 for row in board for value in row)
    )


def find_empty(board: Sequence[Sequence[int]]) -> Optional[Position]:
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                return row, col
    return None


def check_valid(board: Sequence[Sequence[int]], num: int, pos: Position) -> bool:
    """Return True when num can legally be placed at pos."""
    row, col = pos

    if not 1 <= num <= 9:
        return False

    for other_col in range(BOARD_SIZE):
        if other_col != col and board[row][other_col] == num:
            return False

    for other_row in range(BOARD_SIZE):
        if other_row != row and board[other_row][col] == num:
            return False

    box_row = (row // BOX_SIZE) * BOX_SIZE
    box_col = (col // BOX_SIZE) * BOX_SIZE
    for other_row in range(box_row, box_row + BOX_SIZE):
        for other_col in range(box_col, box_col + BOX_SIZE):
            if (other_row, other_col) != pos and board[other_row][other_col] == num:
                return False

    return True


get_valid = check_valid


def board_is_valid(board: Sequence[Sequence[int]]) -> bool:
    if not _shape_is_valid(board):
        return False

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            value = board[row][col]
            if value and not check_valid(board, value, (row, col)):
                return False
    return True


def _solve(board: Board) -> bool:
    empty = find_empty(board)
    if empty is None:
        return True

    row, col = empty
    for number in DIGITS:
        if check_valid(board, number, (row, col)):
            board[row][col] = number
            if _solve(board):
                return True
            board[row][col] = 0

    return False


def solve_sudoku(board: Board) -> bool:
    """Solve board in place. Return False for invalid or unsolvable boards."""
    if not board_is_valid(board):
        return False
    return _solve(board)


def fill_board(board: Board, rng: Optional[Random] = None) -> bool:
    """Fill an empty or partial board with a randomized valid solution."""
    if not board_is_valid(board):
        return False

    rng = rng or Random()

    def fill() -> bool:
        empty = find_empty(board)
        if empty is None:
            return True

        row, col = empty
        candidates = list(DIGITS)
        rng.shuffle(candidates)

        for number in candidates:
            if check_valid(board, number, (row, col)):
                board[row][col] = number
                if fill():
                    return True
                board[row][col] = 0
        return False

    return fill()


def count_solutions(board: Board, limit: int = 2) -> int:
    """Count solutions up to limit without mutating the caller's board."""
    if limit < 1 or not board_is_valid(board):
        return 0

    working = deepcopy(board)
    count = 0

    def search() -> None:
        nonlocal count
        if count >= limit:
            return

        empty = find_empty(working)
        if empty is None:
            count += 1
            return

        row, col = empty
        for number in DIGITS:
            if check_valid(working, number, (row, col)):
                working[row][col] = number
                search()
                working[row][col] = 0
                if count >= limit:
                    return

    search()
    return count


def generate_puzzle(level: int = 40, seed: Optional[int] = None) -> Tuple[Board, Board]:
    """Return a puzzle and its solution with up to level cells removed."""
    holes = max(0, min(int(level), BOARD_SIZE * BOARD_SIZE))
    rng = Random(seed)

    solution = create_empty_board()
    if not fill_board(solution, rng):
        raise RuntimeError("Unable to generate a complete Sudoku board")

    puzzle = deepcopy(solution)
    positions = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)]
    rng.shuffle(positions)

    removed = 0
    for row, col in positions:
        if removed >= holes:
            break

        value = puzzle[row][col]
        puzzle[row][col] = 0

        if count_solutions(puzzle, limit=2) == 1:
            removed += 1
        else:
            puzzle[row][col] = value

    return puzzle, solution


def generate_sudoku(board: Optional[Board] = None, level: int = 40, seed: Optional[int] = None) -> Board:
    """Generate a puzzle, optionally replacing board contents in place."""
    puzzle, _ = generate_puzzle(level=level, seed=seed)

    if board is None:
        return puzzle

    if not _shape_is_valid(board):
        raise ValueError("board must be a 9x9 matrix containing integers from 0 to 9")

    for row in range(BOARD_SIZE):
        board[row][:] = puzzle[row]
    return board


def print_board(board: Sequence[Sequence[int]]) -> None:
    for row in range(BOARD_SIZE):
        if row and row % BOX_SIZE == 0:
            print("-" * 21)
        values = []
        for col in range(BOARD_SIZE):
            if col and col % BOX_SIZE == 0:
                values.append("|")
            values.append(str(board[row][col]))
        print(" ".join(values))


if __name__ == "__main__":
    puzzle, solution = generate_puzzle(level=40)
    print("Puzzle:")
    print_board(puzzle)
    print("\nSolved:")
    solved = deepcopy(puzzle)
    solve_sudoku(solved)
    print_board(solved)
