import numpy as np

from goai.encoders.base import Encoder
from goai.goboard import Move
from goai.gotypes import Point

class SevenPlaneEncoder(Encoder):
    def __init__ (this, board_size):
        this.board_width, this.board_height = board_size
        this.num_planes = 7

    def name(this):
        return 'sevenplane'

    def encode(this, game_state):
        board_tensor = np.zeros(this.shape())
        base_plane = {game_state.next_player: 0, game_state.next_player.other: 3}
        for i in range(this.board_height):
            for j in range(this.board_width):
                point = Point(row = i + 1, col = j + 1)
                go_string = game_state.board.get_go_string(point)
                if go_string is None:
                    if game_state.does_move_violate_ko(game_state.next_player, Move.play(point)):
                        board_tensor[6][i][j] = 1
                else:
                    liberty_plane = min(3, go_string.num_liberties) - 1
                    color_plane = base_plane[go_string.color]
                    board_tensor[color_plane + liberty_plane][i][j] = 1
        return board_tensor

    def encode_point(this, point):
        return this.board_width * (point.row - 1) + (point.col - 1)

    def decode_point_index(this, index):
        row = index // this.board_width + 1
        col = index % this.board_width + 1
        return Point(row = row + 1, col = col + 1)

    def num_points(this):
        return this.board_width * this.board_height

    def shape(this):
        return this.num_planes, this.board_height, this.board_width

def create(board_size):
    return SevenPlaneEncoder(board_size)