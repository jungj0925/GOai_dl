from goai.gotypes import Point

def is_point_an_eye(board, point, color):
    ## Eye is an empty point
    if board.get(point) is not None:
        return False

    ## All adjacent points must contain friendly stones
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False
    
    ## control three out of four cornes if the point is in the middle of the board, on the edge, you must ontrol all four corners
    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]
    for corner in corners:
        if not board.is_on_grid(corner):
            off_board_corners += 1
            continue
        corner_color = board.get(corner)
        if corner_color == color:
            friendly_corners += 1
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    else:
        return friendly_corners >= 3