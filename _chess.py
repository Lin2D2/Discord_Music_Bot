import chess


symbol_to_text = {
    "k": "King", "q": "Queen",
    "r": "Rook", "b": "Bishop",
    "n": "Knights", "p": "Pawn"

}


class Chess:
    def __init__(self):
        self.board = chess.Board()
        self.player1 = None
        self.player2 = None
        self.newBoard = []
        self.update()

    def make_move(self, str_move):
        move = chess.Move.from_uci(str_move)
        if self.board.is_legal(move):
            if self.board.is_capture(move):
                conqueror = self.get_piece(str_move[:2])
                conquered = self.get_piece(str_move[2:])
                event = ("Capture", '''The {} {} captured {} {} of {}'''.format(
                    "White" if str(conqueror).isupper() else "Black",
                    symbol_to_text[str(conqueror).lower()],
                    "the" if symbol_to_text[str(conquered).lower()] == "Queen" or "King" else "a",
                    symbol_to_text[str(conquered).lower()],
                    "White" if str(conquered).isupper() else "Black")
                         )

            else:
                event = True
            self.board.push(move)
            self.update()
            return event
        else:
            return False

    def update(self):
        for line in str(self.board).split("\n"):
            self.newBoard.append(line.split(" "))
        self.newBoard.reverse()
        return

    def get_piece(self, location):
        sq = chess.SQUARES[chess.SQUARE_NAMES.index(location)]
        return chess.Board.piece_at(self.board, sq)


# __chess = Chess()
# print(chess.SQUARE_NAMES)
# print(__chess.board)
# __chess.make_move("b2", "b4")
# print(__chess.board)
# change = {
#     "K": "♔", "Q": "♕",
#     "R": "♖", "B": "♗",
#     "N": "♘", "P": "♙",
#     "k": "♚", "q": "♛",
#     "r": "♜", "b": "♝",
#     "n": "♞", "p": "♟",
#     ".": "⬜", "+": "⬛",
#     " ": " "
# }
# i = 0
# lines = [7, 15, 23, 31, 39, 47, 55, 63]
# new_Board = []
# for char in str(__chess.board):
#     try:
#         new_Board.append(change[char])
#         i += 1
#     except:
#         new_Board.append(char)
#         i += 1


