# Optical Character Recognition using Keras

## Abstract

This project explores low cost methods for pre-training AI models for more complex problems. Generating training data with human work is very slow and costly, but if the problem can be simulated using other tools, then limitless, cheap and unique training data can be generated. This implementation generates images of letters to train a Keras model. After training exclusively on generated images, it is able to achieve 46% accuracy on a hand labeled set of images from building and road signs.

## Training data

Python Imaging Library (PIL) is used to generate training images of text. In attempt to gain some generality, randomized fonts, size, foreground and background colors, position, rotation and noise is added.

![TrainingData](/Present/TrainingDataDisplay.png)

## Evaluating the Model

### TensorBoard

TensorBoard is used to compare the relative progress of different model structures.

![ValidationAccuracy](/Present/ValidationAccuracy.png)

![ValidationLoss](/Present/ValidationLoss.png)

### Confusion matrix

A confusion matrix visualizes the mistakes the AI model is making. Often these mistakes are understandable as the letters have similar features.

![Confusion Matrix](/Present/ConfusionMatrix.png)

## Model Structure

The most successful model achieved 90% accuracy on a unique, generated validation set that it has never trained on. It has the following structure:

### Input: (32,32,3)

### 2x 2D Convolutional Layer
### 2x Dense Layer with 10% dropout rate (64)

### Output Layer: ()

## Validation Set

![ModelPrediction](/Present/PredictDisplay.png)

## Generalizing to larger problems

After training exclusively on generated images, the model was able to correctly identify 46% of letters in a curated set of license plates, building names, and road signs. This method provides a low cost method of pre training a model for a larger problem.

![ModelPrediction](/Present/GeneralizeDisplay.png)
