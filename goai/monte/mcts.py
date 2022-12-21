import random
import math

from goai import agent
from goai.gotypes import Player
from goai.agent import naive

def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + temperature * exploration

class MCTSNode(object):
    def __init__(this, game_state, parent=None, move=None):
        this.game_state = game_state
        this.parent = parent
        this.move = move
        this.win_counts = {
            Player.black: 0,
            Player.white: 0,
        }
        this.num_rollouts = 0
        this.children = []
        this.unvisited_moves = game_state.legal_moves()

    # adding new child to the tree, updating rollout stats
    def add_random_child(this):
        index = random.randint(0, len(this.unvisited_moves) - 1)
        new_move = this.unvisited_moves.pop(index)
        new_game_state = this.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, this, new_move)
        this.children.append(new_node)
        return new_node
    
    def record_win(this, winner):
        this.win_counts[winner] += 1
        this.num_rollouts += 1

    def can_add_child(this):
        return len(this.unvisited_moves) > 0

    def is_terminal(this):
        return this.game_state.is_over()

    def winning_frac(this, player):
        return float(this.win_counts[player]) / float(this.num_rollouts)

class MonteAgent():
    def __init__(this, num_rounds, temperature):
        this.num_rounds = num_rounds
        this.temperature = temperature

    def select_move(this, game_state):
        root = MCTSNode(game_state)
        for i in range(this.num_rounds):
            node = root
            while (not node.can_add_child() and not node.is_terminal()):
                node = this.select_child(node)

            if node.can_add_child():
                node = node.add_random_child()

            winner = this.simulate_random_game(node.game_state)

            while node is not None:
                node.record_win(winner)
                node = node.parent

        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
            return best_move

    def select_child(this, node):
        total_rollouts = sum(child.num_rollouts for child in node.children)

        best_score = -1
        best_child = None
        for child in node.children:
            score = uct_score(total_rollouts, child.num_rollouts,
                                child.winning_frac(node.game_state.next_player),
                                this.temperature)

            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    @staticmethod
    def simulate_random_game(game):
        bots = {
            Player.black: agent.naive.RandomBot(),
            Player.white: agent.naive.RandomBot(),
        }
        while not game.is_over():
            next_move = bots[game.next_player].select_move(game)
            game = game.apply_move(next_move)
        return game.winner()