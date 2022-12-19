# generates games for MCTS training
# each move in the game is encoded by the OnePlaneEncoder
import argparse
import numpy as np

from goai.encoders import get_encoder_by_name
from goai import mcts
from goai import goboard_fast as goboard
from goai.utils import print_board, print_move

def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []

    # Initializing OnePlaneEncoder by name with given board size
    encoder = get_encoder_by_name('oneplane', board_size)

    # new game is instantiated
    game = goboard.GameState.new_game(board_size)

    # MCTS agent is instantiated
    monte = mcts.MCTSAgent(rounds, temperature)