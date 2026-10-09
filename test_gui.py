"""Headless checks of the real GUI's click, keyboard, and clue behavior."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import unittest
from unittest.mock import patch
import pygame
import GUI
from Sudoku_Solver import generate_puzzle


class GuiTests(unittest.TestCase):
    def board(self):
        with patch.object(GUI, "generate_puzzle", lambda level: generate_puzzle(level, seed=42)):
            return GUI.Grid(9, 9, 540, 540)

    def test_click_event_position_and_keyboard_commit(self):
        board = self.board()
        row, col = next((r, c) for r in range(9) for c in range(9) if not board.board[r][c])
        value = board.solution[row][col]
        inputs = [
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(col * 60 + 30, row * 60 + 30), button=1)],
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_0 + value)],
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)],
            [pygame.event.Event(pygame.QUIT)],
        ]
        with patch.object(GUI, "Grid", return_value=board), \
             patch.object(pygame.event, "get", side_effect=inputs):
            GUI.main()
        self.assertEqual(board.selected, (row, col))
        self.assertEqual(board.model[row][col], value)
        self.assertEqual(board.cubes[row][col].temp, 0)

    def test_clues_are_immutable_and_wrong_entries_are_rejected(self):
        board = self.board()
        row, col = next((r, c) for r in range(9) for c in range(9) if board.board[r][c])
        original = board.board[row][col]
        board.select(row, col)
        board.sketch_value(original % 9 + 1)
        self.assertFalse(board.place_value(original % 9 + 1))
        self.assertEqual(board.cubes[row][col].value, original)
        self.assertEqual(board.cubes[row][col].temp, 0)
        row, col = next((r, c) for r in range(9) for c in range(9) if not board.board[r][c])
        board.select(row, col)
        wrong = board.solution[row][col] % 9 + 1
        board.sketch_value(wrong)
        self.assertFalse(board.place_value(wrong))
        self.assertEqual(board.model[row][col], 0)
        board.sketch_value(board.solution[row][col])
        board.clear()
        self.assertEqual(board.cubes[row][col].temp, 0)


if __name__ == "__main__":
    unittest.main()
