"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    move_cnt = 0
    for row in board:
        for cell in row:
            if cell is not EMPTY:
                move_cnt += 1
    
    return X if move_cnt % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    avail_actions = set()
    for r_idx, row in enumerate(board):
        for c_idx, cell in enumerate(row):
            if cell == EMPTY:
                avail_actions.add((r_idx, c_idx))

    return avail_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Not a valid action.")
    
    if action[0] > 2 or action[0] < 0 or action[1] > 2 or action[0] < 0:
        raise Exception("Action out of bounds.")

    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal Lines
    for row in board:
        if row[0] is not EMPTY:
            player = row[0]
            if row[1] == player and row[2] == player:
                return player
    
    # Vertical Lines
    for col_idx, cell in enumerate(board[0]):
        if cell is not EMPTY:
            player = cell
            if board[1][col_idx] == player and board[2][col_idx] == player:
                return player

    # Diagonals
    if board[1][1] is not EMPTY:
        player = board[1][1]
        if (board[0][0] == player and board[2][2] == player) or (board[0][2] == player and board[2][0] == player):
            return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    opt_action = None

    # Player X wants to maximize the utility value
    if player(board) == X:
        value = -1
        opt_action = None
        for action in actions(board):
            child_value = pred_util(result(board,action))
            if child_value > value:
                value = child_value
                opt_action = action
    
    # Player O wants to minimize the utility value
    if player(board) == O:
        value = 1
        opt_action = None
        for action in actions(board):
            child_value = pred_util(result(board,action))
            if child_value < value:
                value = child_value
                opt_action = action

    return opt_action


def pred_util(board, alpha=None, beta=None):
    """
    Returns the predicted utility value of a board using MiniMax Algorithm with Alpha-Beta Pruning
    """
    if terminal(board):
        return utility(board)
    
    if player(board) == X:
        value = -1
        for action in actions(board):
            child_value = pred_util(result(board, action), alpha, beta)
            if child_value > value:
                value = child_value
            
            if beta is not None and value >= beta:
                break

            alpha = value

        return value
    
    if player(board) == O:
        value = 1
        for action in actions(board):
            child_value = pred_util(result(board, action), alpha, beta)
            if child_value < value:
                value = child_value
            
            if alpha is not None and value <= alpha:
                break

            beta = value

        return value

