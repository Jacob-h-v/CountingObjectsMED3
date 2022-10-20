import cv2 as cv
import numpy as np

image = cv.imread('Resources/input picture.jpg')

# Using OpenCV Functions
image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
ret, image_binary = cv.threshold(image_gray, 127, 255, cv.THRESH_BINARY)

kernel = np.ones((5, 5), np.uint8)

erosion = cv.erode(image_binary, kernel, iterations=1)
dilation = cv.dilate(image_binary, kernel, iterations=1)
opening = cv.morphologyEx(image_binary, cv.MORPH_OPEN, kernel)
closing = cv.morphologyEx(image_binary, cv.MORPH_CLOSE, kernel)

# Using manual nested loops * UNDER CONSTRUCTION *
structuring_element = np.array([[1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1]])

# cv.imshow("image", image)
# cv.imshow("image gray", image_gray)
# cv.imshow('image binary', image_binary)

cv.imshow('erosion', erosion)
cv.imshow('dilation', dilation)
cv.imshow('opening', opening)
cv.imshow('closing', closing)

cv.waitKey(0)