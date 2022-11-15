import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, crop
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel
from Morphology import inbuiltMorphology, OpType, morphology, Closing

imageInput = cv.imread("Resources/JPEGbilleder/Coins/GreenBackground/IMG_0383.JPEG")
imageInput = np.array(imageInput, dtype=np.uint8)

# Settings
gaussian_radius = 25
closing_kernel = 5
# structuring_element_erosion = 3
# structuring_element_dilation = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

# These can be changed between True / False to include or exclude different types of image processing.
resize = True
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

if resize:
    scale_percent = 50  # percent of original size
    width = int(imageInput.shape[1] * scale_percent / 100)
    height = int(imageInput.shape[0] * scale_percent / 100)
    dim = (width, height)
    imageInput = cv.resize(imageInput, dim, interpolation=cv.INTER_AREA)

imageInput_gray = cv.cvtColor(imageInput, cv.COLOR_BGR2GRAY)
imageInput_arr = np.array(imageInput_gray)

# Grab temmplate coordinates
if tempCoords:
    template_coords = template_cropping(imageInput)

# Run median filter
if medianFilter:
    image_processed = median_filter(imageInput_gray, 3)

# Convolve with gaussian happens here
if convolve_with_gaussian & medianFilter:
    gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 500)
    image_blurred = convolve(image_processed, gaussian_kernel)
    if adjustImgSize:
        image_resize = image_processed[gaussian_radius:image_processed.shape[0]-gaussian_radius, gaussian_radius:image_processed.shape[1]-gaussian_radius]
        if subtractBlurred:
            image_subtracted = cv.subtract(image_resize, image_blurred)
elif convolve_with_gaussian:
    gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 500)
    image_blurred = convolve(imageInput_gray, gaussian_kernel)
    if adjustImgSize:
        image_resize = image_processed[gaussian_radius:image_processed.shape[0]-gaussian_radius, gaussian_radius:image_processed.shape[1]-gaussian_radius]
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
    image_closed = inbuiltMorphology(image_binary, closing_kernel, OpType.Closing)
    # image_closed = Closing(image_binary, structuring_element_erosion, structuring_element_dilation)
elif closing & convolve_with_gaussian:
    image_closed = inbuiltMorphology(image_subtracted, closing_kernel, OpType.Closing)
elif closing & medianFilter:
    image_closed = inbuiltMorphology(image_processed, closing_kernel, OpType.Closing)
elif closing:
    image_closed = inbuiltMorphology(imageInput_gray, closing_kernel, OpType.Closing)

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
    templateMatching_result, templateMatching_count = TemplateMatching(imageInput, image_closed, template, gaussian_radius)
elif matchTemplates & createTemplate & binaryThresh & tempCoords:
    templateMatching_result, templateMatching_count = TemplateMatching(imageInput, image_binary, template, gaussian_radius)
elif matchTemplates & createTemplate & convolve_with_gaussian & tempCoords:
    templateMatching_result, templateMatching_count = TemplateMatching(imageInput, image_subtracted, template, gaussian_radius)
elif matchTemplates & createTemplate & medianFilter & tempCoords:
    templateMatching_result, templateMatching_count = TemplateMatching(imageInput, image_processed, template, gaussian_radius)
elif matchTemplates & createTemplate & tempCoords:
    templateMatching_result, templateMatching_count = TemplateMatching(imageInput, imageInput_gray, template, gaussian_radius)

templateMatching_result = cv.putText(templateMatching_result, F"{templateMatching_count}", (15,65), 1, 4, (0, 0, 255), 5, cv.LINE_AA)

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

if closing:
    cv.imshow("Closed", image_closed)

cv.waitKey(0)
