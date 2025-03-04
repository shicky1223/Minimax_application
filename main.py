import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Set window dimensions and colors
WIDTH, HEIGHT = 600, 600
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
CROSS_COLOR = (66, 66, 66)
CIRCLE_COLOR = (242, 85, 96)

# Define board parameters
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Define players and empty cell marker
HUMAN = "O"
AI = "X"
EMPTY = " "

# Initialize the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Minimax AI")
screen.fill(BG_COLOR)

# Board representation: a list with 9 elements
board = [EMPTY for _ in range(9)]

def draw_lines():
    # Draw the two horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), 15)
    # Draw the two vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), 15)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            index = row * BOARD_COLS + col
            if board[index] == HUMAN:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE/2), int(row * SQUARE_SIZE + SQUARE_SIZE/2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[index] == AI:
                # Draw two lines for an X (cross)
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def available_moves(state):
    return [i for i, spot in enumerate(state) if spot == EMPTY]

def is_winner(state, player):
    win_states = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    return any(all(state[i] == player for i in line) for line in win_states)

def is_terminal(state):
    return is_winner(state, HUMAN) or is_winner(state, AI) or len(available_moves(state)) == 0

def evaluate(state):
    if is_winner(state, AI):
        return 1
    elif is_winner(state, HUMAN):
        return -1
    else:
        return 0

def minimax(state, depth, is_maximizing):
    if is_terminal(state):
        return evaluate(state)

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(state):
            state[move] = AI
            score = minimax(state, depth + 1, False)
            state[move] = EMPTY
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(state):
            state[move] = HUMAN
            score = minimax(state, depth + 1, True)
            state[move] = EMPTY
            best_score = min(best_score, score)
        return best_score

def best_move(state):
    best_score = -math.inf
    move = None
    for i in available_moves(state):
        state[i] = AI
        score = minimax(state, 0, False)
        state[i] = EMPTY
        if score > best_score:
            best_score = score
            move = i
    return move

def restart_game():
    global board
    board = [EMPTY for _ in range(9)]
    screen.fill(BG_COLOR)
    draw_lines()
    pygame.display.update()

def draw_status():
    # Optionally display a message if game over
    font = pygame.font.SysFont(None, 60)
    if is_winner(board, HUMAN):
        text = font.render("You win!", True, (0, 255, 0))
    elif is_winner(board, AI):
        text = font.render("AI wins!", True, (255, 0, 0))
    elif len(available_moves(board)) == 0:
        text = font.render("It's a tie!", True, (0, 0, 255))
    else:
        return
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(2000)
    restart_game()

# Draw initial board lines
draw_lines()

# Main game loop
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Process human move on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            index = clicked_row * BOARD_COLS + clicked_col

            if board[index] == EMPTY:
                board[index] = HUMAN
                draw_figures()
                pygame.display.update()

                if is_terminal(board):
                    draw_status()
                    continue

                # AI turn using minimax
                ai_move = best_move(board)
                if ai_move is not None:
                    board[ai_move] = AI
                    draw_figures()
                    pygame.display.update()

                if is_terminal(board):
                    draw_status()

    pygame.display.update()
