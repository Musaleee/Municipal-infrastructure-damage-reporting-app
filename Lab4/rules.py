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

    # Kings can move diagonally in either direction.
    if is_king(piece):
        return True

    # Normal pieces can only move forward.
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

    # Normal pieces can only capture forward.
    # Kings can capture in either direction.
    if not is_king(piece):
        direction = -1 if player == "R" else 1
        if er - sr != 2 * direction:
            return False

    mr, mc = (sr + er) // 2, (sc + ec) // 2

    # Compare colours, not exact strings.
    # RK cannot capture R, and BK cannot capture B.
    return piece_color(board[mr][mc]) not in (None, player)


def has_capture(board, player, only_from=None):
    """
    Return True if the player has at least one legal capture.

    If only_from is supplied, only that piece is checked.
    This function never prints anything.
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
    """
    Return True if the player has at least one legal move.

    Forced-capture rules are respected: if any capture exists,
    a simple move does not count as legal.
    """
    forced_capture = has_capture(board, player)

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

                    if not forced_capture and simple_move(
                        board, player, start, end
                    ):
                        return True

    return False


def promote(board, position=None):
    """
    Promote a piece on the correct back row.

    If position is supplied, only that piece is considered.
    Returns True if a promotion occurred.
    """
    if position is not None:
        r, c = position
        piece = board[r][c]

        if piece == "R" and r == 0:
            board[r][c] = "RK"
            return True

        if piece == "B" and r == SIZE - 1:
            board[r][c] = "BK"
            return True

        return False

    # Kept as a general-purpose version for compatibility.
    promoted = False

    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted = True

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted = True

    return promoted