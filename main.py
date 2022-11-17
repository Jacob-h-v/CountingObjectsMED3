import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, crop
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel
from Morphology import inbuiltMorphology, OpType, morphology, Closing

currentImageName = "1M-1L-1P-1CL-3C.jpg"
currentDirectory = "Coins/NormalBackground"
imageInput = cv.imread(F"Resources/JPEGbilleder/{currentDirectory}/{currentImageName}")
imageInput = np.array(imageInput, dtype=np.uint8)
tempImage = imageInput

# Settings
gaussian_radius = 30
newGauss = False
closing_kernel = 5
structuring_element_erosion = 3
structuring_element_dilation = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

# These can be changed between True / False to include or exclude different types of image processing.
resize = True
medianFilter = False
convolve_with_gaussian = True
binaryThresh = False
closing = True
testing = False  # This will write the output image, closed image and template to files in the "Output" folder.
# Don't forget to rename the outputs in the bottom of the script, if testing is enabled.
# -------------------------------
# What to display after the program runs
displayMatchingResult = True
displayClosing = True
displayTemplate = True
displayBinaryThresh = False
displayBlurred = False
displaySubtracted = False
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

# Grab template coordinates
if tempCoords:
    template_coords = template_cropping(tempImage)

# tempImage_gray = cv.cvtColor(tempImage, cv.COLOR_BGR2GRAY)
# tempImage_hsv = cv.cvtColor(tempImage, cv.COLOR_BGR2HSV)
tempImage = np.array(tempImage, dtype=np.uint8)

# Run median filter
if medianFilter:
    tempImage = median_filter(tempImage, 3)
    # median_filtered_img = tempImage

# Convolve with gaussian happens here
if convolve_with_gaussian:
    if newGauss:
        gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 15)
        file = open("savedGauss", "wb")
        np.save(file, gaussian_kernel)
        file.close

    file = open("savedGauss", "rb")
    savedGauss = np.load(file)
    # print(savedGauss)
    image_blurred = convolve(tempImage, savedGauss)
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
    if displayBlurred:
        cv.imshow("blur", image_blurred)
    if displaySubtracted:
        cv.imshow("Subtracted", image_subtracted)

if binaryThresh & displayBinaryThresh:
    cv.imshow("Binary", image_binary)

if createTemplate & tempCoords & displayTemplate:
    cv.imshow("template", template)

if createTemplate & matchTemplates & tempCoords & displayMatchingResult:
    cv.imshow("template matching", tempImage)

if closing & displayClosing:
    cv.imshow("Closed", image_closed)

if testing:
    cv.imwrite(F'Output/{currentDirectory}/Test1-{currentImageName}_result.png', tempImage)
    cv.imwrite(F'Output/{currentDirectory}/Test1-{currentImageName}_final.png', image_closed)
    cv.imwrite(F'Output/{currentDirectory}/Test1-{currentImageName}_template.png', template)

cv.waitKey(0)
