import cv2 as cv
import numpy as np

#testImage1 = cv.imread("Resources/JPEGbilleder/Coins/NormalBackground/1M-2L-1P-1CL-1C_(1)(1).jpg")

def IncreaseContrast(image, contrast_amount):
    output = image.copy()
    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            output[y, x] = contrast_amount * image[y, x]
    return output

#result = IncreaseCotrast(testImage1, 2)

#cv.imshow("input", testImage1)
#cv.imshow("result", result)
#cv.waitKey(0)