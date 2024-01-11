import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
import os
batch_size = 32
img_height = 96
img_width = 96

# Define an ImageDataGenerator with data augmentation parameters
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='constant'
)

val_datagen = ImageDataGenerator(rescale=1./255)

# Load your dataset
train_generator = train_datagen.flow_from_directory(
    'containers/train',  # Make sure to have separate train directory
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

training_data_dir = 'pics/training_data'
os.makedirs(training_data_dir, exist_ok=True)

# Save the processed training images
for i, (images, labels) in enumerate(train_generator):
    for j in range(len(images)):
        image_path = os.path.join(training_data_dir, f'image_{i * batch_size + j}.png')
        cv2.imwrite(image_path, images[j] * 255)  # Save the image in the range [0, 255]
    if i == len(train_generator) - 1:
        break

validation_generator = val_datagen.flow_from_directory(
    'containers/validation',  # Make sure to have separate validation directory
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(2, 2),
    BatchNormalization(),   
    Flatten(),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

steps_per_epoch = max(1, train_generator.samples // batch_size)
validation_steps = max(1, validation_generator.samples // batch_size)

# Train 
history = model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=100,  # Increase if needed
    validation_data=validation_generator,
    validation_steps=validation_steps,
    callbacks=[tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)]
)

# def preprocess_image(image_path):
#     image = cv2.imread(image_path)
#     # image = cv2.resize(image, (96, 96))
#     # image = image.astype('float32') / 255.0
#     image = np.expand_dims(image, axis=0)
#     return image

# def predict_container(image_path):
#     image = preprocess_image(image_path)
#     prediction = model.predict(image)
#     if prediction > 0.1:
#         return "Container detected"
#     else:
#         return "No container detected"
    
# image_path = 'pics/test.png'

# result = predict_container(image_path)

# print(result)

