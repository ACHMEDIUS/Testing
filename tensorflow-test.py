import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
import numpy as np
import pandas as pd
import os

# Load the image data
image_data = []
for filename in os.listdir('pics'):
    image = load_img(os.path.join('pics', filename))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = image.reshape((1, 224, 224, 3))
    image_data.append(image)

# Load the bounding box data
bounding_boxes = pd.read_csv('bounding_boxes.csv')

# Create the training and validation sets
train_images, validation_images = [], []
train_labels, validation_labels = [], []

for i, row in bounding_boxes.iterrows():
    image = image_data[i]
    label = row['label']
    if row['is_train']:
        train_images.append(image)
        train_labels.append(label)
    else:
        validation_images.append(image)
        validation_labels.append(label)

# Configure the data generators
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    rescale=1.0 / 255
)

validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_datagen.flow(
    train_images,
    train_labels,
    batch_size=10,
)

validation_generator = validation_datagen.flow(
    validation_images,
    validation_labels,
    batch_size=10,
)

# Define the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(2, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(train_generator, epochs=10, validation_data=validation_generator)

# Evaluate the model
test_images, test_labels = [], []
for filename in os.listdir('test_pics'):
    image = load_img(os.path.join('test_pics', filename))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = image.reshape((1, 224, 224, 3))
    test_images.append(image)
    test_labels.append(bounding_boxes.loc[filename, 'label'])

test_datagen = ImageDataGenerator(rescale=1.0 / 255)

test_generator = test_datagen.flow(
    test_images,
    test_labels,
    batch_size=10,
)

loss, accuracy = model.evaluate(test_generator)
print(f"Loss: {loss}, Accuracy: {accuracy}")