# generates games for MCTS training
# each move in the game is encoded by the OnePlaneEncoder
import argparse
import numpy as np

from goai.encoders import get_encoder_by_name
from goai import mcts
from goai import goboard_fast as goboard
from goai.utils import print_board, print_move


