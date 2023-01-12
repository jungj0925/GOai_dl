import numpy as np

from goai.encoders.base import Encoder
from goai.gotypes import Point

class OnePlaneEncoder(Encoder):
    def __init__(this, board_size):
        this.board_width, this.board_height = board_size
        this.num_planes = 1

    def name(self):
        return 'oneplane'
        # referencing this OnePlaneEncoder class as oneplane

    #encoding the entire board
    def encode(this, game_state):
        #this is encoding the actual game board
        #we first set the entire 'board' into zeros
        #we set next player as game_state.next_player
        #we then loop through the board and set the board_matrix to 1 or -1
        #we skip the loop if the point is None, as empty spaces are 0
        board_matrix = np.zeros(this.shape())
        next_player = game_state.next_player
        for r in range(this.board_height):
            for i in range(this.board_width):
                p = Point(row=r+1, col=i+1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    continue
                if go_string.color == next_player:
                    board_matrix[0, r, i] = 1
                else:    
                    board_matrix[0, r, i] = -1

        return board_matrix

    #we now encode a single point
    def encode_point(this,point):
        return this.board_width*(point.row - 1)+(point.col - 1) # integer index

    def decode_point_index(this, index):
        row = index // this.board_width
        col = index % this.board_width
        return Point(row=row + 1, col=col + 1)

    def num_points(this):
        return this.board_width * this.board_height

    def shape(this):
        return this.num_planes, this.board_height, this.board_width

def create(board_size):
    return OnePlaneEncoder(board_size)