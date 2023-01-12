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