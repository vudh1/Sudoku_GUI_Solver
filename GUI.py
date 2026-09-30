import time

import pygame

from Sudoku_Solver import generate_puzzle


WINDOW_WIDTH = 540
GRID_HEIGHT = 540
WINDOW_HEIGHT = 600


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.fixed = value != 0

    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), True, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            color = (0, 0, 0) if self.fixed else (35, 80, 180)
            text = font.render(str(self.value), True, color)
            win.blit(
                text,
                (
                    x + (gap / 2 - text.get_width() / 2),
                    y + (gap / 2 - text.get_height() / 2),
                ),
            )

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, value):
        self.value = value

    def set_temp(self, value):
        self.temp = value


class Grid:
    def __init__(self, rows, cols, width, height, level=40):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.level = level
        self.board, self.solution = generate_puzzle(level=level)
        self.cubes = [
            [Cube(self.board[row][col], row, col, width, height) for col in range(cols)]
            for row in range(rows)
        ]
        self.model = [row[:] for row in self.board]
        self.selected = None

    def draw(self, win):
        gap = self.width / 9
        for index in range(self.rows + 1):
            thickness = 5 if index % 3 == 0 else 1
            pygame.draw.line(
                win, (0, 0, 0), (0, index * gap), (self.width, index * gap), thickness
            )
            pygame.draw.line(
                win, (0, 0, 0), (index * gap, 0), (index * gap, self.height), thickness
            )

        for row in self.cubes:
            for cube in row:
                cube.draw(win)

    def update_model(self):
        self.model = [
            [self.cubes[row][col].value for col in range(self.cols)]
            for row in range(self.rows)
        ]

    def place_value(self, value):
        if self.selected is None:
            return False

        row, col = self.selected
        cube = self.cubes[row][col]
        if cube.fixed:
            return False

        if value == self.solution[row][col]:
            cube.set(value)
            cube.set_temp(0)
            self.update_model()
            return True

        cube.set_temp(0)
        return False

    def sketch_value(self, value):
        if self.selected is None:
            return
        row, col = self.selected
        if not self.cubes[row][col].fixed:
            self.cubes[row][col].set_temp(value)

    def select(self, row, col):
        for cube_row in self.cubes:
            for cube in cube_row:
                cube.selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        if self.selected is None:
            return
        row, col = self.selected
        cube = self.cubes[row][col]
        if not cube.fixed and cube.value == 0:
            cube.set_temp(0)

    def click(self, pos):
        if 0 <= pos[0] < self.width and 0 <= pos[1] < self.height:
            gap = self.width / 9
            return int(pos[1] // gap), int(pos[0] // gap)
        return None

    def is_finished(self):
        return all(cube.value != 0 for row in self.cubes for cube in row)


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def redraw_window(win, board, elapsed, strikes):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 40)

    timer = font.render(f"Time: {format_time(elapsed)}", True, (0, 0, 0))
    win.blit(timer, (WINDOW_WIDTH - 180, 555))

    strike_text = font.render("X " * strikes, True, (255, 0, 0))
    win.blit(strike_text, (20, 555))

    board.draw(win)


def main():
    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sudoku Puzzle")

    board = Grid(9, 9, WINDOW_WIDTH, GRID_HEIGHT, level=40)
    key = None
    running = True
    start = time.time()
    strikes = 0

    while running:
        elapsed = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    key = event.key - pygame.K_0
                elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                    board.clear()
                    key = None
                elif event.key == pygame.K_RETURN and board.selected is not None:
                    row, col = board.selected
                    temp = board.cubes[row][col].temp
                    if temp:
                        if not board.place_value(temp):
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print(f"Solved in {format_time(elapsed)} with {strikes} strike(s).")
                            running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = board.click(pygame.mouse.get_pos())
                if clicked is not None:
                    board.select(*clicked)
                    key = None

        if board.selected is not None and key is not None:
            board.sketch_value(key)

        redraw_window(window, board, elapsed, strikes)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
