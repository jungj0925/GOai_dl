# generates games for MCTS training
# each move in the game is encoded by the OnePlaneEncoder
import argparse
import numpy as np

from goai.monte import mcts
from goai.encoders.base import get_encoder_by_name
from goai import goboard_fast as goboard
from goai.utils import print_board, print_move

def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []

    # Initializing OnePlaneEncoder by name with given board size
    encoder = get_encoder_by_name('oneplane', board_size)

    # new game is instantiated
    game = goboard.GameState.new_game(board_size)

    # MCTS agent is instantiated
    monteA = mcts.MonteAgent(rounds, temperature)
    
    # game is played until it is over or max_moves is reached
    num_moves = 0
    while not game.is_over():
        print_board(game.board)
        # next move selected by MCTS agent
        move = monteA.select_move(game)
        if move.is_play:
            # encoded board and move are appended to lists
            boards.append(encoder.encode(game))
            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            # one-hot encoding of move is appended to list
            moves.append(move_one_hot)
        
        print_move(game.next_player, move)
        game = game.apply_move(move)
        num_moves += 1
        if num_moves > max_moves:
            break

    return np.array(boards), np.array(moves)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', '-s', type=int, default=9)
    parser.add_argument('--rounds', '-r', type=int, default=1000)
    parser.add_argument('--max-moves', '-m', type=int, default=60, help='Max moves per game')
    parser.add_argument('--temperature', '-t', type=float, default=0.8)
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--board-out')
    parser.add_argument('--move-out')

    # allows customization using command line arguments
    args = parser.parse_args()
    xs, ys = [], []

    for i in range(args.num_games):
        print("Playing game %d/%d..." % (i+1, args.num_games))
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)
        xs.append(x)
        ys.append(y)

    # After all games have been generated, you concatenate the lists of boards and moves into a single array
    x = np.concatenate(xs)
    y = np.concatenate(ys)

    np.save(args.board_out, x)
    np.save(args.move_out, y)

if __name__ == '__main__':
    main()