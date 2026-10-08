from board import initial_board, move_piece, SIZE
from rules import simple_move, capture_move, promote, has_legal_move


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def set_test_position(self, board, player):
        """Optional helper for testing custom in-memory positions."""
        self.board = board
        self.player = player

    def run(self):
        print("Checkers — move: sr sc er ec")
        while True:
            self.print_board()

            # Check whether the side to move has any pieces.
            has_piece = any(
                piece in (self.player, self.player + "K")
                for row in self.board
                for piece in row
            )

            if not has_piece:
                winner = "B" if self.player == "R" else "R"
                print(f"{winner} wins! {self.player} has no pieces.")
                return

            # Check whether the side to move has any legal move.
            if not has_legal_move(self.board, self.player):
                winner = "B" if self.player == "R" else "R"
                print(f"{winner} wins! {self.player} has no legal moves.")
                return

            raw = input(f"{self.player}> ").strip().lower().split()

            if raw == ["q"]:
                return

            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue

            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            start, end = (sr, sc), (er, ec)

            if capture_move(self.board, self.player, start, end):
                mr, mc = (sr + er) // 2, (sc + ec) // 2
                move_piece(self.board, start, end)
                self.board[mr][mc] = "."
            elif simple_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)
            else:
                print("Invalid move.")
                continue

            promote(self.board)
            self.player = "B" if self.player == "R" else "R"