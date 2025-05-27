from bot.evaluation import evaluate_board

def minimax(board, depth, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board, depth=2):
    best_move = None
    best_value = -float('inf')

    for move in board.legal_moves:
        board.push(move)
        value = minimax(board, depth - 1, False)
        board.pop()
        if value > best_value:
            best_value = value
            best_move = move
    return best_move
