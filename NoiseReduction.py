# Implementing a median filter to reduce noise. Specifically salt/pepper noise and spiky pixel values.

import cv2 as cv

inputPic = cv.imread("Resources/input picture.jpg")




cv.imshow("Input Image", inputPic)
cv.waitKey(0)