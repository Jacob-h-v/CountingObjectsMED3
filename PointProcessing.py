import cv2 as cv
import numpy as np

def IncreaseCotrast(image, contrast_amount):
    output = image.copy()
    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            output[y, x] = contrast_amount * image[y, x]

    return output