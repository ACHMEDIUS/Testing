import tensorflow as tf
import keras
import numpy as np
import cv2

# Load the EfficientNet-B0 model
model = tf.keras.applications.mobilenet_v2.MobileNetV2()

# Load the destination map image
image = tf.keras.utils.load_img('destination_map.jpeg')

# Convert the image to a NumPy array
image = tf.keras.utils.img_to_array(image)

# Preprocess the image
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (800, 800))
image = image.astype('float32')
image /= 255

# Predict the class of the image
predictions = model.predict(image)

# Find the indices of the letter W and M in the predictions array
w_index = np.argwhere(predictions == 23)[0][0]
m_index = np.argwhere(predictions == 13)[0][0]

# Get the predicted bounding boxes for the letters W and M
w_bounding_box = cv2.boundingRect(predictions[0][:, w_index])
m_bounding_box = cv2.boundingRect(predictions[0][:, m_index])

# Draw the bounding boxes on the image
cv2.rectangle(image, (w_bounding_box[0], w_bounding_box[1]), (w_bounding_box[2], w_bounding_box[3]), (0, 0, 255), 2)
cv2.rectangle(image, (m_bounding_box[0], m_bounding_box[1]), (m_bounding_box[2], m_bounding_box[3]), (0, 255, 0), 2)

# Display the image
cv2.imshow('Image', image)
cv2.waitKey(0)
