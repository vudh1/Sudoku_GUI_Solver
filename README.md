# Sudoku GUI Solver

A playable Sudoku desktop app backed by a backtracking solver and a puzzle generator that preserves a **unique solution** while removing clues.

## Features

- backtracking Sudoku solver;
- randomized complete-board generation;
- puzzle generation with uniqueness checking;
- Pygame GUI with penciled values, strikes, and timer;
- immutable starting clues;
- deterministic generation support through a seed for testing.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python GUI.py
```

On Windows:

```powershell
.venv\\Scripts\\activate
```

## Controls

1. Click an empty square.
2. Press a number key to sketch a value.
3. Press Enter to commit it.
4. Delete/Backspace clears the sketch.

## Solver-only usage

```python
from Sudoku_Solver import generate_puzzle, solve_sudoku

puzzle, solution = generate_puzzle(level=40, seed=42)
solve_sudoku(puzzle)
assert puzzle == solution
```

## Test

```bash
python -m unittest -v
```

The tests verify solving, move validation, rejection of invalid boards, and unique-solution puzzle generation.
