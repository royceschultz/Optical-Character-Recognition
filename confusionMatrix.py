from generate import Gen

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

G = Gen()
model = keras.models.load_model('Models/MyTrainedModel1562129906.ckpt')
matrix = []

for c in G.letters:
    print(c)
    set,labels = G.generateNumpySet(100,[c], G.fonts)
    predictions = model.predict(set)
    row = np.zeros(predictions[0].shape)
    for prediction in predictions:
        #row[np.argmax(prediction)] += 1
        row += prediction
    matrix.append(row)

matrix = np.array(matrix)

print(matrix.shape)
print(matrix)

labels = G.letters
x = np.r_[:len(labels)]

plt.imshow(matrix)
plt.xticks(x, labels)
plt.yticks(x, labels)
plt.gray()
plt.show()
