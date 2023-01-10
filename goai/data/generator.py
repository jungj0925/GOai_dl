import glob
import numpy as np
from keras.utils import to_categorical

class DataGenerator:
    def __init__(this, data_dir, samples):
        this.data_dir = data_dir
        this.samples = samples
        this.files = set(file_name for file_name, i in samples)
        this.num_samples = None

    def get_num_samples(this, batch_size=128, num_classes=19*19):
        if this.num_samples is not None:
            return this.num_samples
        else:
            this.num_samples = 0
            for x, y in this._generate(batch_size = batch_size, num_classes = num_classes):
                this.num_samples += x.shape[0]
            return this.num_samples

    def _generate(this, batch_size, num_classes):
        for zip_file_name in this.files:
            file_name = zip_file_name.replace('tar.gz', '') + 'train'
            base = this.data_dir + '/' + file_name + '_features_*.npy'
            for feature_file in glob.glob(base):
                label_file = feature_file.replace('features', 'labels')
                x = np.load(feature_file).astype('float32')
                y = np.load(label_file)
                y = to_categorical(y.astype(int), num_classes=num_classes)
                while x.shape[0] >= batch_size:
                    x_batch, x = x[:batch_size], x[batch_size:]
                    y_batch, y = y[:batch_size], y[batch_size:]
                    yield x_batch, y_batch

    def generate(this, batch_size=128, num_classes=19*19):
        while True:
            for i in this._generate(batch_size, num_classes):
                yield i