import pygame
import chess
import time
from bot.minimax import find_best_move
from bot.opening_book import OpeningBook

WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8

PIECES = {}

def load_images():
    pieces = ['r','n','b','q','k','p','R','N','B','Q','K','P']
    for piece in pieces:
        PIECES[piece] = pygame.transform.scale(
            pygame.image.load(f"assets/images/{piece}.png"), (SQ_SIZE, SQ_SIZE)
        )

def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(8):
        for c in range(8):
            color = colors[(r+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row, col = 7 - square // 8, square % 8
            screen.blit(PIECES[piece.symbol()], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlight_squares(screen, board, selected_square):
    if selected_square is None:
        return
    legal_moves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]
    for sq in legal_moves:
        row, col = 7 - sq // 8, sq % 8
        pygame.draw.circle(screen, pygame.Color("green"), (col * SQ_SIZE + SQ_SIZE//2, row * SQ_SIZE + SQ_SIZE//2), 10)

def draw_material_info(screen, board):
    font = pygame.font.SysFont("arial", 18)
    white_score, black_score = 0, 0
    piece_values = {'p':1, 'n':3, 'b':3, 'r':5, 'q':9}

    for piece in board.piece_map().values():
        value = piece_values.get(piece.symbol().lower(), 0)
        if piece.color == chess.WHITE:
            white_score += value
        else:
            black_score += value

    diff = white_score - black_score
    if diff > 0:
        info = f"Material: White +{diff}"
        color = pygame.Color('green')
    elif diff < 0:
        info = f"Material: Black +{-diff}"
        color = pygame.Color('red')
    else:
        info = "Material: Equal"
        color = pygame.Color('black')

    pygame.draw.rect(screen, pygame.Color('lightgray'), (0, HEIGHT, WIDTH, 30))
    text = font.render(info, True, color)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT + 5))

def animate_move(screen, board, move, clock):
    frames = 10
    from_sq = move.from_square
    to_sq = move.to_square

    from_row, from_col = 7 - from_sq // 8, from_sq % 8
    to_row, to_col = 7 - to_sq // 8, to_sq % 8
    dx = (to_col - from_col) * SQ_SIZE // frames
    dy = (to_row - from_row) * SQ_SIZE // frames

    piece = board.piece_at(to_sq)
    for i in range(frames):
        draw_board(screen)
        draw_pieces(screen, board)
        draw_material_info(screen, board)

        x = from_col * SQ_SIZE + dx * i
        y = from_row * SQ_SIZE + dy * i
        if piece:
            screen.blit(PIECES[piece.symbol()], pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)

def display_end_message(screen, board):
    font = pygame.font.SysFont("arial", 36)
    if board.is_checkmate():
        msg = "Checkmate! " + ("White wins" if board.turn == chess.BLACK else "Black wins")
    elif board.is_stalemate():
        msg = "Stalemate!"
    elif board.is_insufficient_material():
        msg = "Draw: Insufficient material"
    elif board.can_claim_fifty_moves():
        msg = "Draw: 50-move rule"
    elif board.can_claim_threefold_repetition():
        msg = "Draw: Threefold repetition"
    else:
        return
    text = font.render(msg, True, pygame.Color('red'))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 30))
    pygame.display.set_caption("Chess Bot")
    clock = pygame.time.Clock()
    board = chess.Board()
    load_images()
    opening_book = OpeningBook()

    selected_square = None
    running = True
    move = None

    while running:
        draw_board(screen)
        highlight_squares(screen, board, selected_square)
        draw_pieces(screen, board)
        draw_material_info(screen, board)
        display_end_message(screen, board)
        pygame.display.flip()

        if board.turn == chess.BLACK and not board.is_game_over():
            time.sleep(0.8)
            if board.fullmove_number <= 10:
                opening_move = opening_book.get_move(board)
                if opening_move:
                    board.push(opening_move)
                    animate_move(screen, board, opening_move, clock)
                    continue
            move = find_best_move(board, 2)
            board.push(move)
            animate_move(screen, board, move, clock)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE and not board.is_game_over():
                x, y = pygame.mouse.get_pos()
                row, col = 7 - y // SQ_SIZE, x // SQ_SIZE
                square = chess.square(col, row)

                if selected_square is None:
                    if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        animate_move(screen, board, move, clock)
                        selected_square = None
                    else:
                        selected_square = square if board.piece_at(square) and board.piece_at(square).color == chess.WHITE else None

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
