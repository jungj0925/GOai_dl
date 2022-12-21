import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout

# First preprocess the mnist data
# flatten 60000 training samples and 10000 test samples, convert them into float

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

y_train = keras.utils.to_categorical(y_train, 10)

model = Sequential()
model.add(Dense(392, activation='sigmoid', input_shape=(784,)))
model.add(Dense(196, activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.summary()

# next is to compile the model with a loss function and an optimizer
# choose sgd (stochastic gradient descent) as the optimizer
# choose mean squared error as the loss function

model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

# carry out the training step of the network and then evaluate
# it on the test data

model.fit(x_train, y_train, batch_size=128, epochs=1000)
score = model.evaluate(x_test, y_test)
print('Test loss:', score[0])
print('Test accuracy:', score[1])