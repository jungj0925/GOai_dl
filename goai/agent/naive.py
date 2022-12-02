import random
from goai.agent.base import Agent
from goai.agent.helpers import is_point_an_eye
from goai.gotypes import Point
from goai.goboard_slow import Move

class BadBot(Agent):
    def select_move(this, game_state):
        # select a random valid move that preserves our own eyes
        # and captures at least one eye
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)) and \
                    not is_point_an_eye(game_state.board, candidate, game_state.next_player) and \
                    any(is_point_an_eye(game_state.board, candidate, game_state.next_player.other) for candidate in candidate.neighbors()):
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))