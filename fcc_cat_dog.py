# -*- coding: utf-8 -*-
"""fcc_cat_dog.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/freeCodeCamp/boilerplate-cat-and-dog-image-classifier/blob/master/fcc_cat_dog.ipynb
"""

# Commented out IPython magic to ensure Python compatibility.
try:
  # This command only in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt

# Get project files
!wget https://cdn.freecodecamp.org/project-data/cats-and-dogs/cats_and_dogs.zip

!unzip cats_and_dogs.zip

PATH = 'cats_and_dogs'

train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

# Get number of files in each directory. The train and validation directories
# each have the subdirecories "dogs" and "cats".
total_train = sum([len(files) for r, d, files in os.walk(train_dir)])
total_val = sum([len(files) for r, d, files in os.walk(validation_dir)])
total_test = len(os.listdir(test_dir))

# Variables for pre-processing and training.
batch_size = 128
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

#3
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Constants for image size and batch size
IMG_HEIGHT = 150
IMG_WIDTH = 150
BATCH_SIZE = 32

# Create ImageDataGenerators for each dataset
train_image_generator = ImageDataGenerator(rescale=1./255)  # Generator for training data
validation_image_generator = ImageDataGenerator(rescale=1./255)  # Generator for validation data
test_image_generator = ImageDataGenerator(rescale=1./255)  # Generator for test data

# Flow from directory for training, validation, and test datasets
train_data_gen = train_image_generator.flow_from_directory(
    train_dir,  # Use the actual path to training directory
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary'  # Adjust based on your problem (binary classification)
)

val_data_gen = validation_image_generator.flow_from_directory(
    validation_dir,  # Use the actual path to validation directory
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

test_data_gen = test_image_generator.flow_from_directory(
    test_dir,  # Use the actual path to test directory
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode=None,  # No labels for test data
    shuffle=False  # Ensure test data order is preserved
)

# 4
def plotImages(images_arr, probabilities = False):
    fig, axes = plt.subplots(len(images_arr), 1, figsize=(5,len(images_arr) * 3))
    if probabilities is False:
      for img, ax in zip( images_arr, axes):
          ax.imshow(img)
          ax.axis('off')
    else:
      for img, probability, ax in zip( images_arr, probabilities, axes):
          ax.imshow(img)
          ax.axis('off')
          if probability > 0.5:
              ax.set_title("%.2f" % (probability*100) + "% dog")
          else:
              ax.set_title("%.2f" % ((1-probability)*100) + "% cat")
    plt.show()

sample_training_images, _ = next(train_data_gen)
plotImages(sample_training_images[:5])

# 5
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_HEIGHT = 150
IMG_WIDTH = 150
BATCH_SIZE = 32

#create imageDataGenerator for training data with augumentation

train_image_generator = ImageDataGenerator(
    rescale = 1./255,#rescale pixel values to [0,1]
    rotation_range = 40, #randomly rotate images by 40 degrees
    width_shift_range = 0.2, # randomly shift images horizontally
    height_shift_range = 0.2, #randomly shift images vertically
    shear_range = 0.2, #randomly shear images
    zoom_range = 0.2, # randomly zoom into images
    horizontal_flip = True, # randomly flip images horizontally
    fill_mode = 'nearest' # fill in new pixels after transformation
)

train_data_get = train_image_generator.flow_from_directory(
    train_dir,
    target_size = (IMG_HEIGHT, IMG_WIDTH),
    batch_size = BATCH_SIZE,
    class_mode = 'binary'
)

# 6
train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                     directory=train_dir,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     class_mode='binary')

augmented_images = [train_data_gen[0][0][0] for i in range(5)]

plotImages(augmented_images)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Create the model
model = Sequential()

# Add convolutional layers with ReLU activation
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flatten the feature maps to feed into a dense layer
model.add(Flatten())

# Add a fully connected layer with ReLU activation
model.add(Dense(128, activation='relu'))

# Optionally, add dropout to prevent overfitting
model.add(Dropout(0.5))

# Output layer with softmax activation for class probabilities
model.add(Dense(1, activation='sigmoid'))  # Use 'softmax' for multi-class classification

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',  # Use 'categorical_crossentropy' for multi-class
              metrics=['accuracy'])

# Print the model summary
model.summary()

# 8
#number of steps per epoch
steps_per_epoch = total_train // BATCH_SIZE
validation_steps = total_val // BATCH_SIZE

#train the model
history = model.fit(
    train_data_gen,
    steps_per_epoch = steps_per_epoch,
    epochs = epochs,
    validation_data = val_data_gen,
    validation_steps = validation_steps
)

# 9
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

# Ensure test_data_gen is correctly configured
test_data_gen = test_image_generator.flow_from_directory(
    train_dir,  # Path to your test directory
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode=None,  # No labels for test data
    shuffle=False  # Ensure test data order is preserved
)

# Check if any images were found
if test_data_gen.samples == 0:
    print("Error: No images found in the test directory.")
else:
    # Retrieve test images
    test_images = next(test_data_gen)  # Get the first batch of test images
    print(f"Shape of test images batch: {test_images.shape}")

    # Further processing of test_images...



# 11
answers =  [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
            1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1,
            0, 0, 0, 0, 0, 0]

correct = 0

# Ensure the generator is reset before predicting
test_data_gen.reset()

# Check if the generator is empty
if test_data_gen.samples == 0:
    print("Error: No images found in the test directory.")
else:
    probabilities = model.predict(test_data_gen)

    # Assuming 'probabilities' is a list of predicted probabilities
    # (e.g., output from a machine learning model)
    for probability, answer in zip(probabilities, answers):
      if round(probability[0]) == answer: # Access the first element of the probability array
        correct += 1

    percentage_identified = (correct / len(answers)) * 100

    # Print the result (optional)
    print(f"Percentage of correctly identified images: {percentage_identified:.2f}%")

    # Check if the percentage meets a certain threshold (optional)
    if percentage_identified >= 80:  # Example threshold
      print("Passed")
    else:
      print("Failed")