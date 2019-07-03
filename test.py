from generate import Gen

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

G = Gen()
set, labels = G.generateFromFolder('LabeledResizedImages')
#set, labels = G.generateNumpySet(100, G.letters, G.fonts)
model = keras.models.load_model('Models/MyTrainedModel1562129906.ckpt')

print(set.shape, labels.shape)
print(labels)

model.evaluate(set,labels)

def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(G.letters[predicted_label],
                                100*np.max(predictions_array),
                                G.letters[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(len(G.letters)), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


predictions = model.predict(set)

num_rows = 5
num_cols = 6
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, labels, set)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, labels)
plt.show()
