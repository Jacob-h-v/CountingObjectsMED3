# This file outlines the basics of how to code template matching
# Source: Image Processing and Acquisition using Python - Second Edition, P240-241.

# in order to work, this script requires the OpenCV and napari-skimage-regionprops libraries to be enabled in the environment.

import cv2 as cv
import numpy as np
from PIL import Image
from skimage.morphology import label
from skimage.measure import regionprops
from skimage.feature import match_template
from CroppingTemplate import *


# Here we import an image and convert it to grayscale
inputImage = Image.open("Resources/1M-2L-1P-1CL-1C (1).png")
inputImage = inputImage.convert("L")
# Here we convert the image to a ndarray.
inputImage = np.asarray(inputImage)

# Here we import the desired template image and convert it to grayscale
templateImage = 'Output/CroppedPicture'
templateImage = templateImage.convert("L")
# Converting the template image to a ndarray:
templateImage = np.asarray(templateImage)

# Using built in functionality to perform template matching:
comparison = match_template(inputImage, templateImage)
thresh = 0.7

# Thresholding the result from template matching considering pixel values where the normalized cross-correlation  is > 0.7.
result = comparison > thresh

# Labeling the thresholded image:
c = label(result, background=0)

# Performing regionprops to count the number of label:
regprop = regionprops(c)
print("Number of matches:", len(regprop))

# Convert binary image to 8bit for storage:
result = result*255

# Convert ndarray back to Image:
output = cv.imwrite("Output/OutputImageName.jpg", result)

cv.imshow("Input Pic", inputImage)
cv.imshow("Template", templateImage)
cv.imshow("Output pic", output)

cv.waitKey(0)

