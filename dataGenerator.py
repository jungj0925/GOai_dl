from goai.data.parallel_processor import GoDataProcessor
from goai.encoders.oneplane import OnePlaneEncoder

from goai.network import small
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.callbacks import ModelCheckpoint

if __name__ == '__main__':
    rows = 19
    cols = 19
    classes = rows * cols
    games = 100

    encoder = OnePlaneEncoder((rows, cols))

    processor = GoDataProcessor(encoder=encoder.name())
    generator = processor.load_go_data('train', games, use_generator=True)
    test_generator = processor.load_go_data('test', games, use_generator=True)

    ## Defining a neural network with Keras by using the layers function

    shape = (encoder.num_planes, rows, cols)
    layers = small.layers(shape)
    model = Sequential()
    for i in layers:
        model.add(i)
    model.add(Dense(classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

    batch_size = 128
    model.fit(
        generator.generate(batch_size, classes),
        epochs=5, steps_per_epoch = generator.get_num_samples() / batch_size,
        validation_data = test_generator.generate(batch_size, classes),
        validation_steps = test_generator.get_num_samples() / batch_size,
        callbacks = [ModelCheckpoint('../epoch_{epoch}.h5')]
    )
    model.evaluate(
        test_generator.generate(batch_size, classes),
        steps=test_generator.get_num_samples() / batch_size
    )