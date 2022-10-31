import cv2 as cv
import numpy as np
from enum import Enum, auto


class OpType(Enum):
    Erosion = auto()
    Dilation = auto()
    Opening = auto()
    Closing = auto()


img = cv.imread('Resources/1M-2L-1P-1CL-1C (1).png')

# Using OpenCV Functions
def inbuiltMorphology(image_binary, kernel_size, operation):
    # image_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # ret, image_binary = cv.threshold(image_gray, 127, 255, cv.THRESH_BINARY)

    kernel_size = 3
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    if operation == OpType.Erosion:
        output = cv.erode(image_binary, kernel, iterations=1)
    if operation == OpType.Dilation:
        output = cv.dilate(image_binary, kernel, iterations=1)
    if operation == OpType.Opening:
        output = cv.morphologyEx(image_binary, cv.MORPH_OPEN, kernel)
    if operation == OpType.Closing:
        output = cv.morphologyEx(image_binary, cv.MORPH_CLOSE, kernel)

    return output

# Using manual nested loops * UNDER CONSTRUCTION *
def morphology(img, kernel_size, operation):
    image_normalized = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
    image_gray = cv.cvtColor(image_normalized, cv.COLOR_BGR2GRAY)
    ret, image_binary = cv.threshold(image_gray, 127, 255, cv.THRESH_BINARY)

    kernel_size = 3
    kernel_radius = kernel_size//2
    true_value = np.max(img)
    kernel = np.ones((kernel_size, kernel_size))*true_value

    # Output billedet bliver mindre end inputtet da den fjerner kernel radius i hver side
    output = np.zeros((image_binary.shape[0]-2*kernel_radius, image_binary.shape[1]-2*kernel_radius))

    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            roi = img[y:y+kernel_size, x:x+kernel_size]
            # Erosion
            if operation == OpType.Erosion and (roi == kernel).all():
                output[y, x] = true_value
            # Dilation
            if operation == OpType.Dilation and (roi == kernel).any():
                output[y, x] = true_value

    return output

#inbuilt_result = inbuiltMorphology(img, 3, OpType.Dilation)
#manual_result = morphology(img, 3, OpType.Dilation)

#cv.imshow("Inbuilt", inbuilt_result)
#cv.imshow("Manual", manual_result)

#cv.waitKey(0)