"""Run GUI.main and capture its actual Pygame display after scripted input."""
import os
import sys
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pygame
from PIL import Image
import GUI
from Sudoku_Solver import board_is_valid, generate_puzzle


def main():
    original_grid = GUI.Grid
    original_update = pygame.display.update
    original_events = pygame.event.get
    frames = []
    state = {"frame": 0}
    events = {}

    def key(value):
        return pygame.event.Event(pygame.KEYDOWN, key=value)

    def click(row, col):
        return pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                  pos=(col * 60 + 30, row * 60 + 30), button=1)

    def create_grid(*args, **kwargs):
        board = original_grid(*args, **kwargs)
        state["board"] = board
        empty = [(r, c) for r in range(9) for c in range(9) if not board.board[r][c]]
        row, col = empty[0]
        value = board.solution[row][col]
        wrong = value % 9 + 1
        events.update({30: click(row, col), 60: key(pygame.K_0 + wrong),
                       90: key(pygame.K_RETURN), 120: key(pygame.K_0 + value),
                       150: key(pygame.K_RETURN)})
        row, col = empty[1]
        value = board.solution[row][col]
        events.update({180: click(row, col), 195: key(pygame.K_0 + value),
                       210: key(pygame.K_BACKSPACE), 240: key(pygame.K_0 + value),
                       255: key(pygame.K_RETURN)})
        for index, (row, col) in enumerate(empty[2:]):
            frame = 285 + index * 9
            events[frame] = click(row, col)
            events[frame + 3] = key(pygame.K_0 + board.solution[row][col])
            events[frame + 6] = key(pygame.K_RETURN)
        state["empty"] = empty
        return board

    def get_events():
        result = original_events()
        event = events.get(state["frame"])
        if event is not None:
            result.append(event)
        if state["frame"] > 900:
            raise AssertionError("GUI did not finish after scripted input")
        return result

    def capture():
        original_update()
        frame = state["frame"]
        board = state["board"]
        first = board.cubes[state["empty"][0][0]][state["empty"][0][1]]
        if frame == 91:
            assert first.value == 0 and first.temp == 0, "Wrong entry was not rejected"
        if frame == 151:
            assert first.value == board.solution[first.row][first.col]
        if frame == 211:
            row, col = state["empty"][1]
            assert board.cubes[row][col].temp == 0, "Backspace did not clear the sketch"
        if frame % 3 == 0:
            surface = pygame.display.get_surface()
            frames.append(Image.frombytes("RGB", surface.get_size(), pygame.image.tobytes(surface, "RGB")))
        state["frame"] += 1

    # Only seed input generation and drive input/capture. All validation, event
    # handling, gameplay and rendering execute inside the actual application.
    with patch.object(GUI, "generate_puzzle", lambda level: generate_puzzle(level, seed=42)), \
         patch.object(GUI, "Grid", create_grid), \
         patch.object(pygame.event, "get", get_events), \
         patch.object(pygame.display, "update", capture):
        GUI.main()

    board = state["board"]
    assert board.is_finished() and board.model == board.solution
    assert board_is_valid(board.model)
    durations = [50] * len(frames)
    durations[-1] = 2000
    frames[0].save(ROOT / "demo.gif", save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True)
    print(f"Captured {len(frames)} real GUI frames; rejected a wrong entry, cleared a sketch, "
          "committed correct entries and completed a valid board through GUI.main.")


if __name__ == "__main__":
    main()
