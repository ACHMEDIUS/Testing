# import os
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
# from tensorflow import keras
# from tensorflow.keras.preprocessing.image import ImageDataGenerator

# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from tensorflow.keras.models import Sequential

# global variables
img_height = 28
img_width = 28
batch_size = 2

# keras model
# model = keras.Sequential([
#     layers.Input((28, 28, 1)),
#     layers.Conv2D(16, 3, padding='same'),
#     layers.Conv2D(32, 3, padding='same'),
#     layers.MaxPooling2D(),
#     layers.Flatten(),
#     layers.Dense(10),
# ])

image_test = print("select image (.png): ")

building_height = print("building_height: ")
gutter_height = print("Gutter height: ")