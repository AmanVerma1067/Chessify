
import chess
from bot.minimax import find_best_move
from bot.opening_book import OpeningBook

def main():
    board = chess.Board()
    opening_book = OpeningBook()
    print("Welcome to Basic Chess Bot!")
    print("Enter moves in UCI format (e.g., e2e4)")

    while not board.is_game_over():
        print("\n", board)
        if board.turn == chess.WHITE:
            move_uci = input("Your move: ")
            try:
                move = chess.Move.from_uci(move_uci)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move!")
            except:
                print("Invalid input!")
        else:
            print("Bot thinking...")
            if board.fullmove_number <= 10:
                opening_move = opening_book.get_move(board)
                if opening_move:
                    board.push(opening_move)
                    continue  # Skip minimax for opening moves
            move = find_best_move(board, depth=2)
            board.push(move)
            print(f"Bot played: {move.uci()}")

    print("\nGame Over:", board.result())

if __name__ == "__main__":
    main()
