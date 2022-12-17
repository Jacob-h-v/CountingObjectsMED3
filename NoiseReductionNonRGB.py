# Implementing a median filter to reduce noise. Specifically salt/pepper noise and spiky pixel values..

import cv2 as cv
import numpy as np
import math
from PIL import Image


def median_filter2D(data, kernel):
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

# slice = data[ i - filter_size : i + filter_size]

# slice = slice.flatten


# Gaussian filter code from lecture 4
def convolve2D(image, kernel):
    kernel_size = kernel.shape[0]
    output = np.zeros((image.shape[0] - kernel_size + 1, image.shape[1] - kernel_size + 1, image.shape[2]), dtype=np.uint8)

    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            for z in range(output.shape[2]):
                slice = image[y:y + kernel_size, x:x + kernel_size, z:z + 1]
                output[y, x, z] = np.sum(slice * kernel) / np.sum(kernel)
    return output

def generate_gaussian_kernel2D(radius, standard_deviation):
    gaussian = [(1/(standard_deviation*math.sqrt(2*math.pi)))*math.exp(-0.5*(x/standard_deviation)**2) for x in range(-radius, radius+1)]
    gaussian_kernel = np.zeros((radius*2+1,radius*2+1))
    for y in range(gaussian_kernel.shape[0]):
        for x in range(gaussian_kernel.shape[1]):
            gaussian_kernel[y, x] = gaussian[y] * gaussian[x]
    gaussian_kernel *= 1/gaussian_kernel[0, 0]
    return gaussian_kernel
