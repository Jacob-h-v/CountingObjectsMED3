# Implementing a median filter to reduce noise. Specifically salt/pepper noise and spiky pixel values..

import cv2 as cv
import numpy as np
from PIL import Image

inputPic = cv.imread("Resources/hamsta input.jpg")
inputPic_gray = cv.cvtColor(inputPic, cv.COLOR_BGR2GRAY)
inputPic_arr = np.array(inputPic_gray)

def median_filter(data, filter_size):
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = np.zeros(((len(data), len(data[0]))), dtype=np.uint8)
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    return data_final

filtered_img = median_filter(inputPic_arr, 3)


cv.imshow("Filtered Image", filtered_img)
cv.imshow("Input Image", inputPic)
cv.waitKey(0)
