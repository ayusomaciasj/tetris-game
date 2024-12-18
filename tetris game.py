import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I

    [[1, 1],
     [1, 1]],        # O

    [[0, 1, 0],
     [1, 1, 1]],     # T

    [[1, 0, 0],
     [1, 1, 1]],     # L

    [[0, 0, 1],
     [1, 1, 1]],     # J

    [[0, 1, 1],
     [1, 1, 0]],     # S

    [[1, 1, 0],
     [0, 1, 1]],     # Z
]

class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def check_collision(board, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (tetrimino.x + x < 0 or
                    tetrimino.x + x >= WIDTH // BLOCK_SIZE or
                    tetrimino.y + y >= HEIGHT // BLOCK_SIZE or
                    board[tetrimino.y + y][tetrimino.x + x]):
                    return True
    return False

def merge_tetrimino(board, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                board[tetrimino.y + y][tetrimino.x + x] = tetrimino.color

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared_lines = len(board) - len(new_board)
    for _ in range(cleared_lines):
        new_board.insert(0, [0] * (WIDTH // BLOCK_SIZE))
    return new_board, cleared_lines

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_tetrimino(screen, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetrimino.color, ((tetrimino.x + x) * BLOCK_SIZE, (tetrimino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY, ((tetrimino.x + x) * BLOCK_SIZE, (tetrimino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()
    board = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]

    current_tetrimino = Tetrimino(random.choice(SHAPES))
    fall_time = 0
    fall_speed = 500

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetrimino.x -= 1
                    if check_collision(board, current_tetrimino):
                        current_tetrimino.x += 1
                if event.key == pygame.K_RIGHT:
                    current_tetrimino.x += 1
                    if check_collision(board, current_tetrimino):
                        current_tetrimino.x -= 1
                if event.key == pygame.K_DOWN:
                    current_tetrimino.y += 1
                    if check_collision(board, current_tetrimino):
                        current_tetrimino.y -= 1
                if event.key == pygame.K_UP:
                    current_tetrimino.rotate()
                    if check_collision(board, current_tetrimino):
                        current_tetrimino.rotate()
                        current_tetrimino.rotate()
                        current_tetrimino.rotate()

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > fall_speed:
            current_tetrimino.y += 1
            if check_collision(board, current_tetrimino):
                current_tetrimino.y -= 1
                merge_tetrimino(board, current_tetrimino)
                board, _ = clear_lines(board)
                current_tetrimino = Tetrimino(random.choice(SHAPES))
                if check_collision(board, current_tetrimino):
                    running = False
            fall_time = 0

        draw_board(screen, board)
        draw_tetrimino(screen, current_tetrimino)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()