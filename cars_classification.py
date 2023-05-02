# -*- coding: utf-8 -*-
"""cars classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aZGDKC0IL1bx2Eb5Ez9b5hGAdYunJZaX

In this article, we will implement car brand classification using images of the car of 3 brands: Mercedes, Audi, and Lamborghini.

VGG-16 is a 16 layer deep Convolution Neural Network that can classify images into 1000 object categories.
"""

from google.colab import drive
drive.mount('/content/drive')

"""# let import the various libraries

Here, we are using Keras because it enables fast experimentation with deep neural networks. We will build our model with the help of Resnet 50 as it can train deep neural networks with many layers.
"""

# import the required libraries
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50
#import VGG16
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

"""# import the dataset

Resize all the images to the size [224, 224] and make a directory with two separate folders named as train and test. These folders will contain the images of cars required for classification.
"""

# re-size all the images to this
IMAGE_SIZE = [224, 224]
train_path = '/content/drive/MyDrive/dataset/Train'
valid_path = '/content/drive/MyDrive/dataset/Test'

"""We are using imagenet weights as there is no need to train the neural network from scratch ."""

# Use imagenet weights
resnet = ResNet50(input_shape=IMAGE_SIZE + [3], weights='imagenet',include_top=False)

"""Here we are using Resnet because The fundamental breakthrough with ResNet was ,it allowed us to train extremely deep neural networks with 150+ layers successfully."""

# don't train existing weights
for layer in resnet.layers:
    layer.trainable = False
# This helps to get number of output classes
folders = glob('/content/drive/MyDrive/dataset/Train/*')
# Our Layers
x = Flatten()(resnet.output)
prediction = Dense(len(folders), activation='softmax')(x)
# creating object model
model = Model(inputs=resnet.input, outputs=prediction)
model.summary()

"""Here we are using categorical_crossentropy is a loss function that is used in multi-class classification tasks."""

# compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
# Using the Image Data Generator
from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale = 1./255, shear_range =
                      0.2, zoom_range = 0.2, horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)
training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/dataset/Train',target_size = (224, 224),batch_size = 32,class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/dataset/Test',target_size = (224, 224),batch_size = 32,class_mode = 'categorical')

# fit the model
r = model.fit(training_set, validation_data=test_set,epochs=30, steps_per_epoch=len(training_set),validation_steps=len(test_set))

"""Now, plotting the loss"""

# ploting the loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')
# ploting the accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')

"""From the above plot, we can infer that validation loss is higher than train loss and train accuracy is more than validation accuracy.

Now we need to save our model in h5 file format for further testing of the model.
"""

# save it as a h5 file
from tensorflow.keras.models import load_model
model.save('model_resnet50.h5')

"""After loading the model, let’s perform predictions on the test set."""

y_pred = model.predict(test_set)
y_pred

"""Np.argmax() is used here to get the indices of the maximum element from an array ."""

y_pred = np.argmax(y_pred, axis=1)
y_pred

from tensorflow.keras.models import load_model
#Load the h5 file in the model
model=load_model('model_resnet50.h5')

img=image.load_img('/content/drive/MyDrive/dataset/Test/lamborghini/11.jpg',target_size=
                    (224,224))
x=image.img_to_array(img)
x

#Shape of the image
x.shape
#output:
(224, 224, 3)
#Normalizing the image pixels values
x=x/255
#Expand the Dimensions of the image
x=np.expand_dims(x,axis=0)
img_data=preprocess_input(x)
img_data.shape
#output:
(1, 224, 224, 3)

model.predict(img_data)

a=np.argmax(model.predict(img_data), axis=1)
a==1

"""So that is how we perform Image classification on a dataset."""

