SIZE = 8


def piece_color(piece):
    """Return R/B for a normal piece or king, otherwise None."""
    if piece in ("R", "RK"):
        return "R"
    if piece in ("B", "BK"):
        return "B"
    return None


def is_king(piece):
    return piece in ("RK", "BK")


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 1 or abs(ec - sc) != 1:
        return False

    piece = board[sr][sc]

    if piece_color(piece) != player:
        return False

    # Kings can move in either direction.
    if is_king(piece):
        return True

    # Normal pieces only move forward.
    direction = -1 if player == "R" else 1
    return er - sr == direction


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False

    piece = board[sr][sc]

    if piece_color(piece) != player:
        return False

    # Kings can capture in either direction.
    if not is_king(piece):
        direction = -1 if player == "R" else 1
        if er - sr != 2 * direction:
            return False

    mr, mc = (sr + er) // 2, (sc + ec) // 2

    # Compare colour, not the exact string, so RK cannot capture R
    # and BK cannot capture B.
    return piece_color(board[mr][mc]) not in (None, player)


def has_capture(board, player, only_from=None):
    """
    Return True if the player has at least one capture.

    If only_from is supplied, only that particular piece is checked.
    """
    if only_from is not None:
        positions = [only_from]
    else:
        positions = [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if piece_color(board[r][c]) == player
        ]

    for sr, sc in positions:
        if piece_color(board[sr][sc]) != player:
            continue

        for er in range(SIZE):
            for ec in range(SIZE):
                if capture_move(
                    board,
                    player,
                    (sr, sc),
                    (er, ec),
                ):
                    return True

    return False


def has_legal_move(board, player):
    """Return True if the player has at least one legal simple or capture move."""
    for sr in range(SIZE):
        for sc in range(SIZE):
            if piece_color(board[sr][sc]) != player:
                continue

            for er in range(SIZE):
                for ec in range(SIZE):
                    start = (sr, sc)
                    end = (er, ec)

                    if capture_move(board, player, start, end):
                        return True

                    # A simple move is legal only when there is
                    # no capture anywhere for this player.
                    if simple_move(board, player, start, end):
                        if not has_capture(board, player):
                            return True

    return False


def promote(board):
    """Promote pieces and return True if a promotion occurred."""
    promoted = False

    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted = True

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted = True

    return promoted