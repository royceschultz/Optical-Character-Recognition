import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import TensorBoard

import numpy as np
import matplotlib.pyplot as plt
import copy
import generate
import time

t = str(int(time.time()))
RUN_NAME = 'Training Set' + t
MODEL_NAME = 'MyTrainedModel'+t+'.ckpt'

G = generate.Gen()
ValidationSet,ValidationLabel = G.generateNumpySet(1000,G.letters, G.fonts)
ValidationSet = ValidationSet/255.0

# Plot labeled Images
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(ValidationSet[i], cmap=plt.cm.binary)
    plt.xlabel(G.letters[ValidationLabel[i]])
plt.show() #(But not right now)

model = keras.Sequential()
model.add(keras.layers.Conv2D(64, kernel_size=3, activation='relu', input_shape=(G.size[0], G.size[1], 3)))
model.add(keras.layers.Conv2D(64, kernel_size=3, activation='relu'))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(128, activation=tf.nn.relu))
model.add(keras.layers.Dropout(0.1))
model.add(keras.layers.Dense(128, activation=tf.nn.relu))
model.add(keras.layers.Dropout(0.1))
model.add(keras.layers.Dense(len(G.letters), activation=tf.nn.softmax))
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
#Keras Logger
logger = keras.callbacks.TensorBoard(
    log_dir = 'logs/' + RUN_NAME,
    write_graph = True
)
earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)
model.summary()

set,label = G.generateNumpySet(5000,G.letters, G.fonts)
#Pre-training
test_acc = 0.0
while test_acc < 0.1:
    model.fit(set, label,
        epochs=10,
        callbacks=[logger],
        validation_data=(ValidationSet,ValidationLabel)
    )
    test_loss, test_acc = model.evaluate(set, label)
setSize = 10000
train_acc = 1
best = 0
while test_acc < .9:
    del set
    del label
    set,label = G.generateNumpySet(setSize,G.letters, G.fonts) #Create new, smaller set to validate on
    set = set/255.0
    #G.shuffle(set,label)
    model.fit(set, label,
        epochs=100,
        callbacks=[logger, earlyStop],
        validation_data=(ValidationSet,ValidationLabel)
    )
    test_loss, test_acc = model.evaluate(ValidationSet, ValidationLabel, callbacks=[logger])
    if test_acc > best:
        print('Saved model to disc')
        model.save('Models/'+MODEL_NAME)
        best = test_acc


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


predictions = model.predict(ValidationSet)

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, ValidationLabel, ValidationSet)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, ValidationLabel)
plt.show()
