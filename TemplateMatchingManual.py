import numpy as np
import cv2 as cv
import math

#read image
inputPic = cv.imread("Resources/input picture.jpg")

#Test arrays
# test_img = np.array([[1, 4, 7, 1, 1, 1, 4, 4, 1, 1],
#                     [1, 4, 7, 1, 1, 1, 4, 4, 1, 1]], dtype=np.uint8)

new_test_img = cv.imread("Resources/1M-1L-1P-1CL-3C.png")

# test_kernel = np.array([[1, 1, 1],
#                         [1, 1, 1]], dtype=np.uint8)

new_test_kernel = cv.imread("Resources/coinTemplate.png")

new_test_img = cv.cvtColor(new_test_img, cv.COLOR_BGR2GRAY)
new_test_kernel = cv.cvtColor(new_test_kernel, cv.COLOR_BGR2GRAY)

#template matching with normalized-cross correlation
def matchTemplate(image, template):

    kernel_radius_y = template.shape[0]//2
    kernel_radius_x = template.shape[1]//2

    print(kernel_radius_x)
    print(kernel_radius_y)

    output = np.zeros((image.shape[0] - 2*kernel_radius_x, image.shape[1] - 2*kernel_radius_y), dtype=np.uint8)

    print(output.shape)

    # for y in range(processed.shape[0]):
    #     for x in range(processed.shape[1]):
    #         output = sum(processed[x:x+kernel_radius_x] * template) / sum(template)
    #
    # return output
    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            slice = image[y:y + template.shape[0], x:x + template.shape[1]]
            print(slice.shape)
            output[y, x] = np.sum(slice * template) / np.sum(template)
    return output

match = matchTemplate(new_test_img, new_test_kernel)

#print
cv.imshow("input", new_test_img)

#print(f"output {match}")
cv.imshow("Output", match)