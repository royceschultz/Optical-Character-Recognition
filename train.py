import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt
import copy
import generate

G = generate.Gen()
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
fonts = ['/Library/Fonts/Arial.ttf']

set,label = G.generateNumpySet(5000,G.letters, G.fonts)
set = set/255.0
print(set.shape, label.shape)



plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(set[i], cmap=plt.cm.binary)
    plt.xlabel(G.letters[label[i]])
#plt.show()



model = keras.Sequential([
    keras.layers.Conv2D(64, kernel_size=3, activation='relu', input_shape=(G.size[0], G.size[1], 3)),
    keras.layers.Flatten(),
    keras.layers.Dense(256, activation=tf.nn.relu),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(len(G.letters), activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

set = set/255.0
test_loss, test_acc = model.evaluate(set, label)
setSize = 5000
while test_acc < .8:
    model.fit(set, label, epochs=3)
    del set
    del label
    set,label = G.generateNumpySet(setSize,G.letters, G.fonts) #Create new, smaller set to validate on
    set = set/255.0
    test_loss, test_acc = model.evaluate(set, label)

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


set,label = G.generateNumpySet(1000,G.letters, G.fonts) #Create new, smaller set to validate on
set = set/255.0

test_loss, test_acc = model.evaluate(set, label)
print('Test accuracy:', test_acc)

predictions = model.predict(set)

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, label, set)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, label)
plt.show()
