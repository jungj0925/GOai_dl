import importlib

class Encoder:
    #Lets you support logging or saving the name of the encoder your model is using
    def name(this):
        raise NotImplementedError()

    # Tuns a Go board into numeric data
    def encode(this, game_state):
        raise NotImplementedError()

    # Turns a Go board into an integer index
    def encode_point(this, point):
        raise NotImplementedError()

    # Turns an integer index into a Go board
    def decode_point_index(this, index):
        raise NotImplementedError()

    # Number of points on the board (19x19 = 361) or w*h
    def num_points(this):
        raise NotImplementedError()

    # Shape of the encoded board structure
    def shape(this):
        raise NotImplementedError()

def get_encoder_by_name(name, board_size):
    module = importlib.import_module('goai.encoders.' + name)
    #Get the class from the module
    #The class name is the same as the module name
    #The class name is the