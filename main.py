import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, crop
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel
from Morphology import inbuiltMorphology, OpType, morphology, Closing

imageInput = cv.imread("Resources/JPEGbilleder/Coins/GreenBackground/IMG_0383.JPEG")
imageInput = np.array(imageInput, dtype=np.uint8)
tempImage = imageInput

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
testing = True
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
    width = int(tempImage.shape[1] * scale_percent / 100)
    height = int(tempImage.shape[0] * scale_percent / 100)
    dim = (width, height)
    tempImage = cv.resize(tempImage, dim, interpolation=cv.INTER_AREA)
    imageInput = tempImage

# Grab temmplate coordinates
if tempCoords:
    template_coords = template_cropping(tempImage)

tempImage_gray = cv.cvtColor(tempImage, cv.COLOR_BGR2GRAY)
tempImage = np.array(tempImage_gray, dtype=np.uint8)

# Run median filter
if medianFilter:
    tempImage = median_filter(tempImage, 3)
    # median_filtered_img = tempImage

# Convolve with gaussian happens here
if convolve_with_gaussian:
    gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 500)
    image_blurred = convolve(tempImage, gaussian_kernel)
    if adjustImgSize:
        image_resize = tempImage[gaussian_radius:tempImage.shape[0]-gaussian_radius, gaussian_radius:tempImage.shape[1]-gaussian_radius]
        if subtractBlurred:
            tempImage = cv.subtract(image_resize, image_blurred)
            image_subtracted = tempImage


# Binary thresholding happens here
if binaryThresh:
    ret, tempImage = cv.threshold(tempImage, 25, 255, cv.THRESH_BINARY)
    image_binary = tempImage


# Run closing operation
if closing:
    tempImage = inbuiltMorphology(tempImage, closing_kernel, OpType.Closing)
    # tempImage = Closing(image_binary, structuring_element_erosion, structuring_element_dilation)
    image_closed = tempImage


# Crop out the selected template using coordinates
if createTemplate & tempCoords:
    template = crop(tempImage, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)


# Match template against processed image
if matchTemplates & createTemplate & tempCoords:
    tempImage, templateMatching_count = TemplateMatching(imageInput, tempImage, template, gaussian_radius)
    # templateMatching_result = tempImage


tempImage = cv.putText(tempImage, F"{templateMatching_count}", (15, 65), 1, 4, (0, 0, 255), 5, cv.LINE_AA)

# Display images generated along the way
if convolve_with_gaussian:
    cv.imshow("blur", image_blurred)
    cv.imshow("Subtracted", image_subtracted)

if binaryThresh:
    cv.imshow("Binary", image_binary)

if createTemplate & tempCoords:
    cv.imshow("template", template)

if createTemplate & matchTemplates & tempCoords:
    cv.imshow("template matching", tempImage)

if closing:
    cv.imshow("Closed", image_closed)

if testing:
    cv.imwrite('Output/Coins/NormalBackground/CoinNBtest1_result.png', tempImage)
    cv.imwrite('Output/Coins/NormalBackground/CoinNBtest1_final.png', image_closed)
    cv.imwrite('Output/Coins/NormalBackground/CoinNBtest1_template.png', template)

cv.waitKey(0)
