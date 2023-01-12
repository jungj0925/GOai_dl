from goai.data.parallel_processor import GoDataProcessor
from goai.encoders.oneplane import OnePlaneEncoder

from goai.network import small
from keras.models import Sequential
from keras.layers.core import Dense
from keras.callbacks import ModelCheckpoint

if __name__ == '__main__':
    rows, cols = 19, 19
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

    epochs = 5
    batch_size = 128
    print("THIS IS WORKING______________________________________")
    model.fit(
        generator.generate(batch_size, classes),
        epochs=epochs,
        steps_per_epoch = generator.get_num_samples() / batch_size,
        validation_data = test_generator.generate(batch_size, classes),
        validation_steps = test_generator.get_num_samples() / batch_size,
        callbacks=[ModelCheckpoint('../checkpoints/small_model_epoch_{epoch}.h5')]
    )
    print("THIS IS WORKING 222222222222222222_____________________________________")
    model.evaluate(
        test_generator.generate(batch_size, classes),
        steps=test_generator.get_num_samples() / batch_size
    )