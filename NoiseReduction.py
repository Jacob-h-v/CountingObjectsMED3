# Implementing a median filter to reduce noise. Specifically salt/pepper noise and spiky pixel values..

import cv2 as cv
import numpy as np
from PIL import Image

#inputPic = cv.imread("Resources/hamsta input.jpg")
#inputPic_gray = cv.cvtColor(inputPic, cv.COLOR_BGR2GRAY)
#inputPic_arr = np.array(inputPic_gray)


def median_filter(data, kernel):
    temp = []
    indexer = kernel // 2
    window = [
        (i, j)
        for i in range(-indexer, kernel - indexer)
        for j in range(-indexer, kernel - indexer)
    ]
    index = len(window) // 2
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j] = sorted(
                0 if (
                        min(i + a, j + b) < 0
                        or len(data) <= i + a
                        or len(data[0]) <= j + b
                ) else data[i + a][j + b]
                for a, b in window
            )[index]
            return data
    return data


#filtered_img = median_filter(inputPic_arr, 3)

#cv.imshow("Filtered Image", filtered_img)
#cv.imshow("Input Image", inputPic)
#cv.waitKey(0)

# slice = data[ i - filter_size : i + filter_size]

# slice = slice.flatten
