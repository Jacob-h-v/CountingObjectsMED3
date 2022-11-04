import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, crop
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel
from Morphology import inbuiltMorphology, OpType

imageInput = cv.imread("Resources/1M-2L-1P-1CL-1C (1).png")
imageInput_gray = cv.cvtColor(imageInput, cv.COLOR_BGR2GRAY)
imageInput_arr = np.array(imageInput_gray)

tempCoords = True
medianFilter = True
convolve_with_gaussian = True
adjustImgSize = True
subtractBlurred = True
binaryThresh = True
closing = True
createTemplate = True
matchTemplates = True

if tempCoords:
    template_coords = template_cropping(imageInput)

if medianFilter:
    image_processed = median_filter(imageInput_gray, 3)

if convolve_with_gaussian:
    gaussian_radius = 25
    gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 500)
    image_blurred = convolve(image_processed, gaussian_kernel)
    if adjustImgSize:
        new_image_size = (
        image_processed.shape[1] - gaussian_radius * 2, image_processed.shape[0] - gaussian_radius * 2)
        image_resize = cv.resize(image_processed, new_image_size, interpolation=cv.INTER_LINEAR)
        if subtractBlurred:
            image_subtracted = cv.subtract(image_resize, image_blurred)

if binaryThresh:
    ret, image_binary = cv.threshold(image_subtracted, 25, 255, cv.THRESH_BINARY)

if closing:
    image_closed = inbuiltMorphology(image_binary, 5, OpType.Closing)

if createTemplate:
    template = crop(image_closed, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)

if matchTemplates:
    templateMatching_result = TemplateMatching(imageInput, image_closed, template, gaussian_radius)
    

cv.imshow("blur", image_blurred)
cv.imshow("Subtracted", image_subtracted)
cv.imshow("Binary", image_binary)
cv.imshow("template", template)
cv.imshow("template matching", templateMatching_result)
cv.waitKey(0)
