import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

np.random.seed(120)
x = np.load('./generated_games/features-40k.npy')
y = np.load('./generated_games/labels-40k.npy')

samples = x.shape[0]
size = 9
input_shape = (size, size, 1)

x = x.reshape(samples, size, size, 1)
y = y.reshape(samples, size, size, 1)

train_samples = int(0.9 * samples)
x_train = x[:train_samples]
y_train = y[:train_samples]
x_test = x[train_samples:]
y_test = y[train_samples:]

model = Sequential()
model.add(Conv2D(48, kernel_size=(3, 3), activation='relu', padding='same', input_shape=input_shape))
model.add(Dropout(rate=0.5))
model.add(Conv2D(48, (3, 3), padding='same', activation='relu'))
model.add(Flatten())

model.add(Dense(512, activation='sigmoid'))
model.add(Dense(size * size, activation='sigmoid'))
model.summary()

model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=64, epochs=15, verbose=1, validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

test_board = np.array([[
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, -1, 1, -1, 0, 0, 0, 0,
    0, 1, -1, 1, -1, 0, 0, 0, 0,
    0, 0, 1, -1, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
]])

probability = model.predict(test_board)[0]
x = 0
for i in range(9):
    row_formatted = []
    for j in range(9):
        row_formatted.append('{:.4f}'.format(probability[x]))
        x += 1
    print(' '.join(row_formatted))

