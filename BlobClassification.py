import cv2 as cv
import numpy as np

def RemoveEdgeBlobs(grassfire_image):
    for y in range(grassfire_image.shape[0]):
        for x in range(grassfire_image.shape[1]):
            if grassfire_image[y, x] != 0:
                if y == 0 or x == 0 or y == grassfire_image.shape[0]-1 or x == grassfire_image.shape[1]-1:
                    currentID = grassfire_image[y, x]
                    for z in range(grassfire_image.shape[0]):
                        for i in range(grassfire_image.shape[1]):
                            if grassfire_image[z, i] == currentID:
                                grassfire_image[z, i] = 0

    return grassfire_image