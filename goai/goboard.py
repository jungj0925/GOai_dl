import copy
from goai import zobrist
from goai.gotypes import Player


#Any action a player can take on a turn - is_play, is_pass, or is_resign - will be represented by a Move object
class Move():
    def __init__(this, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        this.point = point
        this.is_play = (this.point is not None)
        this.is_pass = is_pass
        this.is_resign = is_resign

    @classmethod
    def play(cls, point): #cls is a reference to the class itself
        return Move(point=point)
        #places a stone on the board
    
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
        #passes the turn

    @classmethod
    def resign(cls):
        return Move(is_resign=True)
        #resigns the game
        #cls is a reference to the class itself

#A Go string is a group of connected stones of the same color
class GoString():
    def __init__(this, color, stones, liberties):
        this.color = color
        this.stones = frozenset(stones)
        this.liberties = frozenset(liberties)

    def without_liberty(this, point):
        new_liberties = this.liberties - set([point])
        return GoString(this.color, this.stones, new_liberties)
    
    def with_liberty(this, point):
        new_liberties = this.liberties | set([point])
        return GoString(this.color, this.stones, new_liberties)

    #This returns a new GoString with the stones and liberties of the two strings combined
    def merged_with(this, go_string):
        assert go_string.color == this.color
        c_stones = this.stones | go_string.stones
        return GoString(
            this.color,
            c_stones,
            (this.liberties | go_string.liberties) - c_stones
        )
    
    @property
    def num_Liberties(this):
        return len(this.liberties)

    def __eq__(this, other):
        return isinstance(other, GoString) and this.color == other.color and this.stones == other.stones and this.liberties == other.liberties

    def __deepcopy__(this, memodict={}):
        return GoString(this.color, this.stones, copy.deepcopy(this.liberties))

#A Go board is represented by a dictionary of points to strings
class Board():
    def __init__(this, num_rows, num_cols):
        this.num_rows = num_rows
        this.num_cols = num_cols
        this._grid = {}
        this._hash = zobrist.EMPTY_BOARD

    #inspect all neighboring stones of a given point of liberties
    def place_stone(this, player, point):
        assert this.is_on_grid(point)
        assert this._grid.get(point) is None
        nextto_same_color = []
        nextto_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not this.is_on_grid(neighbor):
                continue
            neighbor_string = this._grid.get(neighbor)
            ##if the neighbor is empty, add it to the liberties
            if neighbor_string is None:
                liberties.append(neighbor)
            ##if the neighbor is the same color, add it to the list of same color neighbors
            elif neighbor_string.color == player:
                if neighbor_string not in nextto_same_color:
                    nextto_same_color.append(neighbor_string)
            ##if the neighbor is the opposite color, add it to the list of opposite color neighbors
            else:
                if neighbor_string not in nextto_opposite_color:
                    nextto_opposite_color.append(neighbor_string)
        ##create a new string with the new stone and the liberties
        new_string = GoString(player, [point], liberties)
        ##Merge all of the same color strings together
        for same_color_string in nextto_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            this._grid[new_string_point] = new_string

        this._hash ^= zobrist.HASH_CODE[point, player]

        ##Remove the liberties of the opposite color strings
        for other_color_string in nextto_opposite_color:
            replacement = other_color_string.without_liberty(point)
            if replacement.num_Liberties:
                this._replace_string(other_color_string.without_liberty(point))
            else:
                this._remove_string(other_color_string)
        
        ##Remove the opposite color strings if they have no liberties
        for other_color_string in nextto_opposite_color:
            if other_color_string.num_Liberties == 0:
                this.remove_string(other_color_string)

        ##is_on_grid checks if the point is on the board
    def is_on_grid(this, point):
        return 1 <= point.row <= this.num_rows and \
            1 <= point.col <= this.num_cols

    ##get returns the string at a given point
    def get(this, point):
        string = this._grid.get(point)
        if string is None:
            return None
        return string.color

    ##returns the entire string at a given point
    def get_go_string(this, point):
        string = this._grid.get(point)
        if string is None:
            return None
        return string

    def _replace_string(this, new_string):
        for point in new_string.stones:
            this._grid[point] = new_string

    def _remove_string(this, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = this._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    this._replace_string(neighbor_string.with_liberty(point))
            this._grid[point] = None

            this._hash ^= zobrist.HASH_CODE[point, string.color]

    ##Removing the string can add liberity to other strings
    def remove_string(this, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = this._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            this._grid[point] = None
    
    def zobrist_hash(this):
        return this._hash

class GameState():
    def __init__(this, board, next_player, previous, move):
        this.board = board
        this.next_player = next_player
        this.previous_state = previous
        if this.previous_state is None:
            this.previous_states = frozenset()
        else:
            this.previous_states = frozenset(
                previous.previous_states | 
                {(previous.next_player, previous.board.zobrist_hash())}
            )
        this.last_move = move

    def apply_move(this, move):
        if move.is_play:
            next_board = copy.deepcopy(this.board)
            next_board.place_stone(this.next_player, move.point)
        else:
            next_board = this.board

        return GameState(next_board, this.next_player.other, this, move)
    
    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_over(this):
        if this.last_move is None:
            return False
        if this.last_move.is_resign:
            return True
        second_last_move = this.previous_state.last_move
        if second_last_move is None:
            return False
        return this.last_move.is_pass and second_last_move.is_pass

    def is_move_self_capture(this, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(this.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_Liberties == 0

    @property
    def situation(this):
        return (this.next_player, this.board)

    def does_move_violate_ko(this, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(this.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in this.previous_states
        
    def is_valid_move(this, move):
        if this.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        ##check if the move is a self capture
        return (this.board.get(move.point) is None and
                not this.is_move_self_capture(this.next_player, move) and
                not this.does_move_violate_ko(this.next_player, move))


        
