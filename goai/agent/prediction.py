import numpy as np

from goai.agent.base import Agent
from goai.agent.helpers import is_point_an_eye
from goai.gotypes import Point
from goai import encoders
from goai import goboard_fast as goboard
from goai import kerasGo

class DeepLearningAgent(Agent):
    def __init__(this, model, encoder):
        Agent.__init__(this)
        this.model = model
        this.encoder = encoder

    def prediction(this, game_state):
        encoded = this.encoder.encode(game_state)
        input = np.array([encoded])
        return this.model.predict(input)[0]

    def select_move(this, game_state):
        moves = this.encoder.board_width * this.encoder.board_height
        move_probs = this.prediction(game_state)

        move_probs = move_probs ** 3
        epsilon = 1e-6
        move_probs = np.clip(move_probs, epsilon, 1 - epsilon)
        move_probs = move_probs / np.sum(move_probs)
        candidates = np.arange(moves)
        ranked = np.random.choice(candidates, moves, replace=False, p=move_probs)
        for point_idx in ranked:
            point = this.encoder.decode_point_index(goboard.Move.play(point_idx))  
            if game_state.is_valid_move(goboard.Move.play(point)) and not is_point_an_eye(game_state.board, point, game_state.next_player):
                return goboard.Move.play(point)
        return goboard.Move.pass_turn()

    def serialize(this, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = this.encoder.name()
        h5file['encoder'].attrs['board_width'] = this.encoder.board_width
        h5file['encoder'].attrs['board_height'] = this.encoder.board_height
        h5file.create_group('model')
        kerasGo.save_model_to_hdf5_group(this.model, h5file['model'])