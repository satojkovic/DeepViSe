from keras.utils import Sequence
from keras.preprocessing import image
import numpy as np

class ImageGenerator(Sequence):
    def __init__(self, path, fnames, wvecs, vec_size, batch_size, image_size=(224, 224), shuffle=True):
        self.path = path
        self.fnames = fnames
        self.wvecs = wvecs
        self.vec_size = vec_size
        self.batch_size = batch_size
        self.image_size = image_size
        self.shuffle = shuffle
        self.indexes = np.arange(len(self.fnames))
        self.on_epoch_end()

    def _load_items(self, indexes):
        X = np.zeros((self.batch_size, self.image_size[0], self.image_size[1], 3), dtype=np.float32)
        y = np.zeros((self.batch_size, self.vec_size), dtype=np.float32)
        image_paths = [self.path/self.fnames[i] for i in indexes]
        wvecs = [self.wvecs[i] for i in indexes]
        for index, image_path in enumerate(image_paths):
            img = image.load_img(image_path, target_size=self.image_size)
            img = image.img_to_array(img)
            wvec = wvecs[index]
            X[index, :] = img
            y[index, :] = wvec
        return X, y

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size : (index + 1) * self.batch_size]
        X, y = self._load_items(indexes)
        return X, y

    def __len__(self):
        # Denotes the number of batches per epoch
        return int(np.floor(len(self.fnames) / self.batch_size))

    def on_epoch_end(self):
        # Udpates indexes after each epoch
        self.indexes = np.arange(len(self.fnames))
        if self.shuffle:
            np.random.shuffle(self.indexes)