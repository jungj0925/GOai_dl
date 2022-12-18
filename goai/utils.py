from goai import gotypes
from goai import agent

COLS = 'ABCDEFGHIJKLMNOPQRS'
STONE_TO_CHAR = {
    None: ' . ',
    gotypes.Player.black: ' x ',
    gotypes.Player.white: ' o ',
}

## print each moves on the terminal
def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))

## print the board on the terminal
def print_board(board):
    for row in range (board.num_rows, 0 ,-1):
        bump = ' ' if row <= 9 else ''
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row = row, col = col))
            line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' % (bump, row, ''.join(line)))
    print('   ' + '  '.join(COLS[:board.num_cols]))

def point_from_coords(coords):
    col = COLS.find(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)