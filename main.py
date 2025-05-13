import pygame
import random

pygame.init()
FONT = pygame.font.SysFont("Arial", 30)

BLOCK_SIZE = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = COLS * BLOCK_SIZE, ROWS * BLOCK_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

SHAPES = [
    ([[1, 1, 1, 1]], (0, 255, 255)),          # I
    ([[1, 0, 0], [1, 1, 1]], (0, 0, 255)),    # J
    ([[0, 0, 1], [1, 1, 1]], (255, 165, 0)),  # L
    ([[1, 1], [1, 1]], (255, 255, 0)),        # O
    ([[0, 1, 1], [1, 1, 0]], (0, 255, 0)),    # S
    ([[0, 1, 0], [1, 1, 1]], (128, 0, 128)),  # T
    ([[1, 1, 0], [0, 1, 1]], (255, 0, 0))     # Z
]

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(board):
    for y in range(ROWS):
        for x in range(COLS):
            color = board[y][x] if board[y][x] else GRAY
            pygame.draw.rect(SCREEN, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(SCREEN, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(SCREEN, piece.color, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def valid_position(piece, board, dx=0, dy=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = piece.x + x + dx
                ny = piece.y + y + dy
                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False
                if ny >= 0 and board[ny][nx]:
                    return False
    return True

def merge_piece(piece, board):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                board[piece.y + y][piece.x + x] = piece.color

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = ROWS - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [0] * COLS)
    return new_board, cleared

def draw_button(text, rect, color=WHITE):
    pygame.draw.rect(SCREEN, color, rect, border_radius=10)
    label = FONT.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    SCREEN.blit(label, label_rect)

def draw_score(score):
    text = FONT.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(text, (10, 10))

def run_game():
    board = create_board()
    clock = pygame.time.Clock()
    fall_time = 0
    move_time = 0
    move_delay = 100
    shape, color = random.choice(SHAPES)
    current_piece = Piece(shape, color)
    game_over = False
    running = True
    score = 0

    while running:
        SCREEN.fill(BLACK)
        fall_time += clock.get_rawtime()
        move_time += clock.get_rawtime()
        clock.tick()

        if not game_over and fall_time > 500:
            if valid_position(current_piece, board, dy=1):
                current_piece.y += 1
            else:
                merge_piece(current_piece, board)
                board, cleared = clear_lines(board)
                if cleared == 1:
                    score += 100
                elif cleared == 2:
                    score += 300
                elif cleared == 3:
                    score += 500
                elif cleared == 4:
                    score += 800
                shape, color = random.choice(SHAPES)
                current_piece = Piece(shape, color)
                if not valid_position(current_piece, board):
                    game_over = True
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    old_shape = current_piece.shape
                    current_piece.rotate()
                    if not valid_position(current_piece, board):
                        current_piece.shape = old_shape
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if restart_btn.collidepoint(event.pos):
                    return True

        if not game_over:
            keys = pygame.key.get_pressed()
            if move_time > move_delay:
                if keys[pygame.K_LEFT] and valid_position(current_piece, board, dx=-1):
                    current_piece.x -= 1
                    move_time = 0
                elif keys[pygame.K_RIGHT] and valid_position(current_piece, board, dx=1):
                    current_piece.x += 1
                    move_time = 0
                elif keys[pygame.K_DOWN] and valid_position(current_piece, board, dy=1):
                    current_piece.y += 1
                    move_time = 0

        draw_board(board)
        draw_score(score)
        if not game_over:
            draw_piece(current_piece)
        else:
            msg = FONT.render("Game Over", True, WHITE)
            score_text = FONT.render(f"Your Score: {score}", True, WHITE)
            SCREEN.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
            SCREEN.blit(score_text, score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
            restart_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 20, 160, 50)
            draw_button("Restart", restart_btn)

        pygame.display.update()

def main():
    while True:
        SCREEN.fill(BLACK)
        start_btn = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 - 25, 160, 50)
        draw_button("Start", start_btn)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_btn.collidepoint(event.pos):
                        waiting = False
        if not run_game():
            break

if __name__ == "__main__":
    main()
