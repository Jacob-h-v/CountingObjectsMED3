# Implementing a median filter to reduce noise. Specifically salt/pepper noise and spiky pixel values..

import cv2 as cv
import numpy as np
import math
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


# Gaussian filter code from lecture 4
def convolve(image, kernel):
    kernel_size = kernel.shape[0]
    output = np.zeros((image.shape[0] - kernel_size + 1, image.shape[1] - kernel_size + 1), dtype=np.uint8)
    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            slice = image[y:y+kernel_size, x:x+kernel_size]
            output[y, x] = np.sum(slice*kernel)/np.sum(kernel)
    return output

def generate_gaussian_kernel(radius, standard_deviation):
    gaussian = [(1/(standard_deviation*math.sqrt(2*math.pi)))*math.exp(-0.5*(x/standard_deviation)**2) for x in range(-radius, radius+1)]
    gaussian_kernel = np.zeros((radius*2+1,radius*2+1))
    for y in range(gaussian_kernel.shape[0]):
        for x in range(gaussian_kernel.shape[1]):
            gaussian_kernel[y, x] = gaussian[y] * gaussian[x]
    gaussian_kernel *= 1/gaussian_kernel[0,0]
    return gaussian_kernel

#img = cv.imread("lion.jpg", cv.IMREAD_GRAYSCALE)

#mean_kernel = np.ones((11,11))
#mean = convolve(img, mean_kernel)

#gaussian_kernel = generate_gaussian_kernel(4, 2.2)
#gaussian = convolve(img, gaussian_kernel)