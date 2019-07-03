# Optical Character Recognition using keras

## TensorBoard

![ValidationAccuracy](/Present/ValidationAccuracy.png)

![ValidationLoss](/Present/ValidationLoss.png)

## Model Structure

The most successful model achieved 90% accuracy on the generated validation set. It had the following structure:

### Input: (32,32,3)

### 2D Convolutional Layer: (30,30,64)
### 2D Convolutional Layer: (28,28,64)
### Dense Layer: (128)
### Dense Layer: (128)

### Output Layer: ()
