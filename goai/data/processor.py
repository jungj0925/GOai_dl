import os.path
import tarfile
import gzip
import glob
import shutil
import numpy as np
from keras.utils import to_categorical
from goai.gosgf import Sgf_game
from goai.goboard_fast import Board, GameState, Move
from goai.gotypes import Player, Point
from goai.encoders.base import get_encoder_by_name
from goai.data.index_processor import KGSIndex
from goai.data.sampler import Sampler

class GoDataProcessor:
    def __init__(this, encoder='oneplane', data_directory='data'):
        this.encoder = get_encoder_by_name(encoder, 19)
        this.data_dir = data_directory

    def load_go_data(this, data_type='train', num_samples=1000):
        index = KGSIndex(data_directory = this.data_dir)
        index.download_files()
        sampler = Sampler(data_dir = this.data_dir)
        data = sampler.draw_data(data_type, num_samples)

        zip_names = set()
        indices_by_zip_name = {}
        for filename, index in data:
            zip_names.add(filename)
            if filename not in indices_by_zip_name:
                indices_by_zip_name[filename] = []
            indices_by_zip_name[filename].append(index)
        for i in zip_names:
            base = i.replace('.tar.gz', '')
            data_name = base + data_type
            if not os.path.isfile(this.data_dir + '/' + data_name):
                this.process_zip(i, data_name, indices_by_zip_name[i])
        featuresAndLabels = this.consolidate_games(data_type, data)
        return featuresAndLabels

    def unzip_data(self, zip_file_name):
        this_gz = gzip.open(self.data_dir + '/' + zip_file_name)  # <1>

        tar_file = zip_file_name[0:-3]  # <2>
        this_tar = open(self.data_dir + '/' + tar_file, 'wb')

        shutil.copyfileobj(this_gz, this_tar)  # <3>
        this_tar.close()
        return tar_file

    def process_zip(this, zip_name, data_name, game_list):
        tar_file = this.unzip_data(zip_name)
        zip_file = tarfile.open(this.data_dir + '/' + tar_file)
        name_list = zip_file.getnames()
        total_examples = this.num_total_examples(zip_file, game_list, name_list)

        shape = this.encoder.shape()
        feature_shape = np.insert(shape, 0, np.asarray([total_examples]))
        features = np.zeros(feature_shape)
        labels = np.zeros((total_examples,))

        counter = 0
        for i in game_list:
            name = name_list[i + 1]
            if not name.endswith('.sgf'):
                raise ValueError(name + ' is not an sgf file')
            sgf_content = zip_file.extractfile(name).read()
            sgf = Sgf_game.from_string(sgf_content)
            game_state, first_move_done = this.get_handicap(sgf)

            for j in sgf.main_sequence_iter():
                color, move_tuple = j.get_move()
                point = None
                if color is not None:
                    if move_tuple is not None:
                        row, col = move_tuple
                        point = Point(row + 1, col + 1)
                        move = Move.play(point)
                    else:
                        move = Move.pass_turn()
                    if first_move_done and point is not None:
                        features[counter] = this.encoder.encode(game_state)
                        labels[counter] = this.encoder.encode_point(point)
                        counter += 1
                    game_state = game_state.apply_move(move)
                    first_move_done = True
        feature_file_base = this.data_dir + '/' + data_name + '_features_%d'
        label_file_base = this.data_dir + '/' + data_name + '_labels_%d'
        chunk = 0
        chunksize = 1024
        while features.shape[0] >= chunksize:
            feature_file = feature_file_base % chunk
            label_file = label_file_base % chunk
            chunk += 1
            current_features, features = features[:chunksize]
            current_labels, labels = labels[:chunksize]
            np.save(feature_file, current_features)
            np.save(label_file, current_labels)
    
    def num_total_examples(this, zip_file, game_list, name_list):
        total_examples = 0
        for i in game_list:
            name = name_list[i + 1]
            if name.endswith('.sgf'):
                sgf_content = zip_file.extractfile(name).read()
                sgf = Sgf_game.from_string(sgf_content)
                game_state, first_move_done = this.get_handicap(sgf)
                num_moves = 0
                for j in sgf.main_sequence_iter():
                    color, move_tuple = j.get_move()
                    if color is not None:
                        if first_move_done:
                            num_moves += 1
                        first_move_done = True
                total_examples += num_moves
            else:
                raise ValueError(name + ' is not an sgf file')
        return total_examples

    @staticmethod
    def get_handicap(sgf):
        go_board = Board(19, 19)
        first_move_done = False
        move = None
        game_state = GameState.new_game(19)
        if sgf.get_handicap() is not None and sgf.get_handicap() != 0:
            for i in sgf.get_root().get_setup_stones():
                for move in i:
                    row, col = move
                    point = Point(row + 1, col + 1)
                    go_board.place_stone(Player.black, point)
            first_move_done = True
            game_state = GameState(go_board, Player.white, None, move)
        return game_state, first_move_done

    def consolidate_games(this, data_type, samples):
        files_needed = set(file_name for file_name, index in samples)
        file_names = []
        for zip_file_name in files_needed:
            file_name = zip_file_name.replace('.tar.gz', '') + data_type
            file_names.append(file_name)

        features = []
        labels = []
        for file_name in file_names:
            file_prefix = file_name.replace('.tar.gz', '')
            base = this.data_dir + '/' + file_prefix + '_features_*.npy'
            for feature_file in glob.glob(base):
                label_file = feature_file.replace('features', 'labels')
                x = np.load(feature_file)
                y = np.load(label_file)
                x = x.astype('float32')
                y = to_categorical(y.astype(int), num_classes=361)
                features.append(x)
                labels.append(y)
        features = np.concatenate(features, axis=0)
        labels = np.concatenate(labels, axis=0)
        np.save('{}/features_{}.npy'.format(this.data_dir, data_type), features)
        np.save('{}/labels_{}.npy'.format(this.data_dir, data_type), labels)
        return features, labels