from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D, ZeroPadding2D

def layers(input_shape):
    return [
        #Using zero padding layers to enlarge input images
        ZeroPadding2D(padding=3, input_shape=input_shape, data_format='channels_last'),
        Conv2D(48, (7, 7), data_format='channels_last'), 
        Activation('relu'),
        
        ZeroPadding2D(padding=2, data_format='channels_last'),
        Conv2D(32, (5, 5), data_format='channels_last'), 
        Activation('relu'),

        ZeroPadding2D(padding=2, data_format='channels_last'),
        Conv2D(32, (5, 5), data_format='channels_last'), 
        Activation('relu'),

        ZeroPadding2D(padding=2, data_format='channels_last'),
        Conv2D(32, (5, 5), data_format='channels_last'), 
        Activation('relu'),

        Flatten(), Dense(512), Activation('relu')
    ]

# layers returns a list of Keras layers that we can use to add to    the Sequential model
