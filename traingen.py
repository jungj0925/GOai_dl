from goai.data.parallel_processor import GoDataProcessor
from goai.encoders.oneplane import OnePlaneEncoder

from goai.network import small
from keras.models import Sequential
from keras.layers.core import Dense
from keras.callbacks import ModelCheckpoint  # <1>

def main():

    rows, cols = 19, 19
    classes = rows * cols
    num_games = 100

    encoder = OnePlaneEncoder((rows, cols))  # <1>

    processor = GoDataProcessor(encoder=encoder.name())  # <2>

    generator = processor.load_go_data('train', num_games, use_generator=True)  # <3>
    test_generator = processor.load_go_data('test', num_games, use_generator=True)
    input_shape = (encoder.num_planes, rows, cols)
    network_layers = small.layers(input_shape)
    model = Sequential()
    for layer in network_layers:
        model.add(layer)
    model.add(Dense(classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    epochs = 10
    batch_size = 128
    model.fit(generator.generate(batch_size, classes),  # <1>
                        epochs=epochs,
                        steps_per_epoch=generator.get_num_samples(),
                        validation_data=test_generator.generate(batch_size, classes),
                        validation_steps=test_generator.get_num_samples(),
                        callbacks=[ModelCheckpoint('./checkpoints/small_model_epoch_{epoch}.h5')])

    model.evaluate(test_generator.generate(batch_size, classes), steps=test_generator.get_num_samples())

if __name__ == '__main__':
    main()