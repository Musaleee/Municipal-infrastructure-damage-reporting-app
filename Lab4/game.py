from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    has_legal_move,
    has_capture,
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        print("   " + "-" * (SIZE * 2 - 1))
        for r, row in enumerate(self.board):
            display_row = []
            for piece in row:
                if piece == "RK":
                    display_row.append("r")
                elif piece == "BK":
                    display_row.append("b")
                else:
                    display_row.append(piece)
            print(f"{r}  " + " ".join(display_row))
        print("Legend: R/B = normal pieces, r/b = kings")

    def set_test_position(self, board, player):
        """Optional helper for testing custom in-memory positions."""
        self.board = board
        self.player = player

    def player_has_piece(self):
        return any(
            piece in (self.player, self.player + "K")
            for row in self.board
            for piece in row
        )

    def check_game_over(self):
        """Check whether the current player has lost at the start of a turn."""
        if not self.player_has_piece():
            winner = "B" if self.player == "R" else "R"
            print(f"{winner} wins! {self.player} has no pieces.")
            return True

        if not has_legal_move(self.board, self.player):
            winner = "B" if self.player == "R" else "R"
            print(f"{winner} wins! {self.player} has no legal moves.")
            return True

        return False

    def get_move(self):
        """Read and validate the basic input format."""
        raw = input(f"{self.player}> ").strip().lower().split()

        if raw == ["q"]:
            return "quit"

        if len(raw) != 4:
            print("Enter four coordinates.")
            return None

        try:
            sr, sc, er, ec = map(int, raw)
        except ValueError:
            print("Coordinates must be numbers.")
            return None

        if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
            print("Outside board.")
            return None

        return (sr, sc), (er, ec)

    def make_move(self, start, end):
        """Apply a validated capture or simple move."""
        sr, sc = start
        er, ec = end

        if capture_move(self.board, self.player, start, end):
            mr, mc = (sr + er) // 2, (sc + ec) // 2

            move_piece(self.board, start, end)
            self.board[mr][mc] = "."

            was_promoted = promote(self.board)

            return "capture", was_promoted

        if simple_move(self.board, self.player, start, end):
            move_piece(self.board, start, end)

            was_promoted = promote(self.board)

            return "simple", was_promoted

        return None, False

    def run(self):
        print("Checkers — move: sr sc er ec")

        while True:
            # Check game-over conditions at the start of every turn.
            self.print_board()

            if self.check_game_over():
                return

            forced_capture = has_capture(self.board, self.player)
            forced_piece = None

            while True:
                if forced_piece is not None:
                    print(
                        f"Continue capture with piece at "
                        f"({forced_piece[0]}, {forced_piece[1]})."
                    )

                result = self.get_move()

                if result == "quit":
                    return

                if result is None:
                    continue

                start, end = result
                sr, sc = start

                # During a multi-capture, only the same piece can move.
                if forced_piece is not None and start != forced_piece:
                    print("You must continue capturing with the same piece.")
                    continue

                if self.board[sr][sc] not in (
                    self.player,
                    self.player + "K",
                ):
                    print("That is not your piece.")
                    continue

                move_type, was_promoted = self.make_move(start, end)

                if move_type is None:
                    if forced_piece is None and forced_capture:
                        print("A capture is available. You must capture.")
                    elif forced_piece is not None:
                        print("You must make another capture with that piece.")
                    else:
                        print("Invalid move.")
                    continue

                # A simple move always ends the turn.
                if move_type == "simple":
                    break

                # Capture happened.
                # Promotion during a capture immediately ends the turn.
                if was_promoted:
                    break

                # Check whether this exact piece can capture again.
                new_position = end

                if has_capture(
                    self.board,
                    self.player,
                    only_from=new_position,
                ):
                    forced_piece = new_position
                    self.print_board()
                    continue

                # No more captures for this piece.
                break

            self.player = "B" if self.player == "R" else "R"