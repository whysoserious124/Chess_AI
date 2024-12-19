import chess
import openai

# Replace with your OpenAI API key
openai.api_key = ""

# Map chess piece symbols to Unicode characters
piece_map = {
    'K': '♔', 'Q': '♕', 'B': '♗', 'N': '♘', 'P': '♙', 'R': '♖',
    'k': '♚', 'q': '♛', 'b': '♝', 'n': '♞', 'p': '♟', 'r': '♜'
}

def chatgpt_suggest_move(board):
    """
    Queries ChatGPT to suggest a move based on the current board state.
    """
    prompt = (
        f"The current chess board in FEN format is:\n{board.fen()}\n"
        "Suggest the best move for Black in UCI format (e.g., e2e4). "
        "Respond with only the move, no explanation."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        move = response['choices'][0]['message']['content'].strip()
        
        # Validate and return the move
        if chess.Move.from_uci(move) in board.legal_moves:
            return move
        else:
            raise ValueError(f"ChatGPT suggested an invalid move: {move}")
    except Exception as e:
        raise RuntimeError(f"Failed to get move from ChatGPT: {str(e)}")

def print_board(board):
    """
    Prints the board with custom Unicode chess pieces.
    """
    board_str = str(board)
    # Replace each character with the corresponding Unicode chess piece
    for piece, symbol in piece_map.items():
        board_str = board_str.replace(piece, symbol)
    print(board_str)

def main():
    """
    Main function to play a chess game where ChatGPT plays as Black against a human.
    """
    board = chess.Board()
    
    while not board.is_game_over():
        print("\nCurrent Board:")
        print_board(board)

        if board.turn:  # Your turn (White)
            print("\nYour Turn:")
            user_move = input("Enter your move in UCI notation (e.g., e2e4): ").strip()

            try:
                move = chess.Move.from_uci(user_move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move. Try again.")
                    continue
            except ValueError:
                print("Invalid move format. Use UCI notation (e.g., e2e4).")
                continue
        else:  # ChatGPT's turn (Black)
            print("\nChatGPT's Turn:")
            try:
                chatgpt_move = chatgpt_suggest_move(board)
                print(f"ChatGPT suggests: {chatgpt_move}")
                board.push(chess.Move.from_uci(chatgpt_move))
            except Exception as e:
                print(f"Error during ChatGPT's turn: {e}")
                break

    # Game Over
    print("\nGame Over!")
    print(f"Result: {board.result()}")

if __name__ == "__main__":
    main()
