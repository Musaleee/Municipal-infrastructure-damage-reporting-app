SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    direction = -1 if player == "R" else 1

    return (
        board[er][ec] == "."
        and abs(er - sr) == 1
        and abs(ec - sc) == 1
        and er - sr == direction
    )


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    direction = -1 if player == "R" else 1
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    opponent = "B" if player == "R" else "R"

    return (
        board[er][ec] == "."
        and abs(er - sr) == 2
        and abs(ec - sc) == 2
        and er - sr == 2 * direction
        and board[mr][mc] != "."
        and board[mr][mc][0] == opponent
    )


def has_legal_move(board, player):
    """Return True if the player has at least one legal simple or capture move."""
    for sr in range(SIZE):
        for sc in range(SIZE):
            if board[sr][sc] not in (player, player + "K"):
                continue

            for er in range(SIZE):
                for ec in range(SIZE):
                    start = (sr, sc)
                    end = (er, ec)

                    if simple_move(board, player, start, end):
                        return True

                    if capture_move(board, player, start, end):
                        return True

    return False


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"