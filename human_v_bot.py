from goai import agent
from goai import gotypes
from goai import goboard
from goai.agent import naive
from goai.utils import print_board, print_move, point_from_coords

def main():
    board_size = 19
    game = goboard.GameState.new_game(board_size)
    bot = naive.RandomBot()
    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)

        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)

if __name__ == '__main__':
    main()