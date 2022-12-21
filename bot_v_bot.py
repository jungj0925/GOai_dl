from goai import agent
from goai import gotypes
from goai import goboard_fast as goboard
from goai.agent import naive
from goai.utils import print_board, print_move
import time

def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: agent.naive.RandomBot(),
        gotypes.Player.white: agent.naive.RandomBot(),
    }
    while not game.is_over():
        time.sleep(0.1)
        print(chr(27) + "[2J")
        print_board(game.board)
        next_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, next_move)
        game = game.apply_move(next_move)

if __name__ == '__main__':
    main()