import cv2
import numpy as np

# Load the image
image = cv2.imread('pics/test.png', 0)  

blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Hough Circle Transform
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=100)

# Draw detected circles
if circles is not None:
    circles = np.round(circles[0, :]).astype(int)
    for (x, y, r) in circles:
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)

# output
cv2.imwrite('pics/detected_circles.jpg', image)
