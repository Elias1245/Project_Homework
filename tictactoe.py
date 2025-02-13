import math
import copy
import pygame
import sys

grid_size = 100
window_size = grid_size * 3
X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    if action not in actions(board):
        raise ValueError("Invalid action")
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    return None

def terminal(board):
    return winner(board) is not None or not any(EMPTY in row for row in board)

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def minimax(board):
    if terminal(board):
        return None
    current_player = player(board)
    if current_player == X:
        best_val = -math.inf
        best_move = None
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_val:
                best_val = value
                best_move = action
        return best_move
    else:
        best_val = math.inf
        best_move = None
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_val:
                best_val = value
                best_move = action
        return best_move

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def draw_board(board, screen):
    screen.fill((0, 0, 0))
    for i in range(1, 3):
        pygame.draw.line(screen, (255, 255, 255), (0, i * grid_size), (window_size, i * grid_size), 3)
        pygame.draw.line(screen, (255, 255, 255), (i * grid_size, 0), (i * grid_size, window_size), 3)
    font = pygame.font.Font(None, 80)
    for i in range(3):
        for j in range(3):
            if board[i][j] is not EMPTY:
                text = font.render(board[i][j], True, (255, 255, 255))
                screen.blit(text, (j * grid_size + 30, i * grid_size + 20))
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((window_size, window_size))
    human_player = X
    ai_player = O
    score = {X: 0, O: 0, "Ties": 0}
    
    while True:
        board = initial_state()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and player(board) == human_player:
                    x, y = event.pos
                    row, col = y // grid_size, x // grid_size
                    if (row, col) in actions(board):
                        board = result(board, (row, col))
                        if terminal(board):
                            running = False
            if player(board) == ai_player and not terminal(board):
                pygame.time.delay(500)
                board = result(board, minimax(board))
                if terminal(board):
                    running = False
            draw_board(board, screen)
        
        game_winner = winner(board)
        if game_winner:
            score[game_winner] += 1
        else:
            score["Ties"] += 1
        
        print(f"Score - X: {score[X]}, O: {score[O]}, Ties: {score['Ties']}")
        pygame.time.delay(2000)

if __name__ == "__main__":
    main()

