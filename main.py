import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, crop
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel
from Morphology import inbuiltMorphology, OpType

imageInput = cv.imread("Resources/1M-2L-1P-1CL-1C (1).png")
imageInput_gray = cv.cvtColor(imageInput, cv.COLOR_BGR2GRAY)
imageInput_arr = np.array(imageInput_gray)
gaussian_radius = 0

# These can be changed between True / False to include or exclude different types of image processing.
medianFilter = True
convolve_with_gaussian = True
binaryThresh = True
closing = True
# -------------------------------
# Warning: Modifying these can crash the program
tempCoords = True
adjustImgSize = True
subtractBlurred = True
createTemplate = True
matchTemplates = True
# -------------------------------

# Grab temmplate coordinates
if tempCoords:
    template_coords = template_cropping(imageInput)

# Run median filter
if medianFilter:
    image_processed = median_filter(imageInput_gray, 3)

# Convolve with gaussian happens here
if convolve_with_gaussian & medianFilter:
    gaussian_radius = 25
    gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 500)
    image_blurred = convolve(image_processed, gaussian_kernel)
    if adjustImgSize:
        new_image_size = (
        image_processed.shape[1] - gaussian_radius * 2, image_processed.shape[0] - gaussian_radius * 2)
        image_resize = cv.resize(image_processed, new_image_size, interpolation=cv.INTER_LINEAR)
        if subtractBlurred:
            image_subtracted = cv.subtract(image_resize, image_blurred)
elif convolve_with_gaussian:
    gaussian_radius = 25
    gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 500)
    image_blurred = convolve(imageInput_gray, gaussian_kernel)
    if adjustImgSize:
        new_image_size = (
        imageInput_gray.shape[1] - gaussian_radius * 2, imageInput_gray.shape[0] - gaussian_radius * 2)
        image_resize = cv.resize(imageInput_gray, new_image_size, interpolation=cv.INTER_LINEAR)
        if subtractBlurred:
            image_subtracted = cv.subtract(image_resize, image_blurred)

# Binary thresholding happens here
if binaryThresh & convolve_with_gaussian:
    ret, image_binary = cv.threshold(image_subtracted, 25, 255, cv.THRESH_BINARY)
elif binaryThresh & medianFilter:
    ret, image_binary = cv.threshold(image_processed, 25, 255, cv.THRESH_BINARY)
elif binaryThresh:
    ret, image_binary = cv.threshold(imageInput_gray, 25, 255, cv.THRESH_BINARY)

# Run closing operation
if closing & binaryThresh:
    image_closed = inbuiltMorphology(image_binary, 5, OpType.Closing)
elif closing & convolve_with_gaussian:
    image_closed = inbuiltMorphology(image_subtracted, 5, OpType.Closing)
elif closing & medianFilter:
    image_closed = inbuiltMorphology(image_processed, 5, OpType.Closing)
elif closing:
    image_closed = inbuiltMorphology(imageInput_gray, 5, OpType.Closing)

# Crop out the selected template using coordinates
if createTemplate & closing & tempCoords:
    template = crop(image_closed, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)
elif createTemplate & binaryThresh & tempCoords:
    template = crop(image_binary, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)
elif createTemplate & convolve_with_gaussian & tempCoords:
    template = crop(image_subtracted, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)
elif createTemplate & tempCoords & medianFilter:
    template = crop(image_processed, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)
elif createTemplate & tempCoords:
    template = crop(imageInput_gray, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)

# Match template against processed image
if matchTemplates & createTemplate & closing & tempCoords:
    templateMatching_result = TemplateMatching(imageInput, image_closed, template, gaussian_radius)
elif matchTemplates & createTemplate & binaryThresh & tempCoords:
    templateMatching_result = TemplateMatching(imageInput, image_binary, template, gaussian_radius)
elif matchTemplates & createTemplate & convolve_with_gaussian & tempCoords:
    templateMatching_result = TemplateMatching(imageInput, image_subtracted, template, gaussian_radius)
elif matchTemplates & createTemplate & medianFilter & tempCoords:
    templateMatching_result = TemplateMatching(imageInput, image_processed, template, gaussian_radius)
elif matchTemplates & createTemplate & tempCoords:
    templateMatching_result = TemplateMatching(imageInput, imageInput_gray, template, gaussian_radius)

# Display images generated along the way
if convolve_with_gaussian:
    cv.imshow("blur", image_blurred)
    cv.imshow("Subtracted", image_subtracted)

if binaryThresh:
    cv.imshow("Binary", image_binary)

if createTemplate & tempCoords:
    cv.imshow("template", template)

if createTemplate & matchTemplates & tempCoords:
    cv.imshow("template matching", templateMatching_result)

cv.waitKey(0)
