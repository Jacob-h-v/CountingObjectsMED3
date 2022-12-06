import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, crop
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel
from Morphology import inbuiltMorphology, OpType, morphology, Closing
from testie import ManualTemplateMatching
from PointProcessing import IncreaseContrast
from BinaryThreshold import BinaryThreshold, BitsuThreshold
from grassfire import grassfire

currentImageName = "1M-2L-1P-1CL-1C_(1)(1).jpg"
currentDirectory = "Coins/NormalBackground"
imageInput = cv.imread(F"Resources/JPEGbilleder/{currentDirectory}/{currentImageName}")
imageInput = np.array(imageInput, dtype=np.uint8)
tempImage = imageInput

# Settings
gaussian_radius = 20
newGauss = True
closing_kernel = 5
structuring_element_erosion = 3
structuring_element_dilation = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
contrast_multiplier = 2

# These can be changed between True / False to include or exclude different types of image processing.
resize = True
medianFilter = False
convolve_with_gaussian = True
applyContrast = True
binaryThresh = True
closing = True
grassfired = True
testing = False  # This will write the output image, closed image and template to files in the "Output" folder.
# Don't forget to rename the outputs in the bottom of the script, if testing is enabled.
# -------------------------------
# What to display after the program runs
displayMatchingResult = True
displayClosing = True
displayTemplate = True
displayBinaryThresh = True
displayBlurred = False
displaySubtracted = True
displayContrast = False
displayGrassfire = True
# -------------------------------
# Warning: Modifying these can crash the program
tempCoords = True
adjustImgSize = True
subtractBlurred = True
createTemplate = True
matchTemplates = True
# -------------------------------

if resize:
    print("Resizing image...")
    scale_percent = 50  # percent of original size
    width = int(tempImage.shape[1] * scale_percent / 100)
    height = int(tempImage.shape[0] * scale_percent / 100)
    dim = (width, height)
    tempImage = cv.resize(tempImage, dim, interpolation=cv.INTER_AREA)
    imageInput = tempImage

# Grab template coordinates
if tempCoords:
    print("Generating template coordinates...")
    template_coords = template_cropping(tempImage)

# tempImage_gray = cv.cvtColor(tempImage, cv.COLOR_BGR2GRAY)
# tempImage_hsv = cv.cvtColor(tempImage, cv.COLOR_BGR2HSV)
tempImage = np.array(tempImage, dtype=np.uint8)

# Run median filter

if medianFilter:
    print("Applying median filter...")
    tempImage = median_filter(tempImage, 3)
    # median_filtered_img = tempImage

# Convolve with gaussian happens here
if convolve_with_gaussian:
    if newGauss:
        print("Generating new gaussian kernel...")
        gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 15)
        file = open("savedGauss", "wb")
        np.save(file, gaussian_kernel)
        file.close
    print("Applying gaussian filter...")
    file = open("savedGauss", "rb")
    savedGauss = np.load(file)
    # print(savedGauss)
    image_blurred = convolve(tempImage, savedGauss)
    if adjustImgSize:
        image_resize = tempImage[gaussian_radius:tempImage.shape[0]-gaussian_radius, gaussian_radius:tempImage.shape[1]-gaussian_radius]
        print("Subtracting blurred image from original...")
        if subtractBlurred:
            tempImage = cv.subtract(image_resize, image_blurred)
            image_subtracted = tempImage

if applyContrast:
    tempImage = IncreaseContrast(tempImage, contrast_multiplier)
    contrasted = tempImage

# Binary thresholding happens here
if binaryThresh:
    print("Applying binary thresholding...")
    tempImage = cv.cvtColor(tempImage, cv.COLOR_BGR2GRAY)
    cv.imshow("grey", tempImage)
    #tempImage = cv.adaptiveThreshold(tempImage, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 251, 2)
    #ret, tempImage = cv.threshold(tempImage, 25, 255, cv.THRESH_BINARY)
    biThresh = BitsuThreshold(tempImage)
    print(f"Bitsu Threshold: {biThresh}")
    tempImage = BinaryThreshold(tempImage, biThresh)
    image_binary = tempImage


# Run closing operation
if closing:
    print("Running morphology operation...")
    # tempImage = morphology(tempImage, 5, OpType.Erosion)

    #tempImage = inbuiltMorphology(tempImage, 3, OpType.Erosion)

    # Closing
    tempImage = inbuiltMorphology(tempImage, 7, OpType.Dilation)
    tempImage = inbuiltMorphology(tempImage, 7, OpType.Erosion)

    # Opening
    tempImage = inbuiltMorphology(tempImage, 7, OpType.Erosion)
    tempImage = inbuiltMorphology(tempImage, 7, OpType.Dilation)

    # tempImage = Closing(image_binary, structuring_element_erosion, structuring_element_dilation)
    image_closed = tempImage

if grassfired:
    grassfire(tempImage)
    np.array(tempImage).dtype=np.uint8
    image_grassfire = tempImage

# Crop out the selected template using coordinates
if createTemplate & tempCoords:
    print("Cropping template...")
    template = crop(tempImage, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)


# Match template against processed image
if matchTemplates & createTemplate & tempCoords:
    print("Running template matching...")
    tempImage, templateMatching_count = TemplateMatching(imageInput, tempImage, template, gaussian_radius)
    # tempImage, templateMatching_count = ManualTemplateMatching(imageInput, tempImage, template, gaussian_radius)
    # templateMatching_result = tempImage
    print("Generating image text...")
    tempImage = cv.putText(tempImage, F"{templateMatching_count}", (15, 65), 1, 4, (0, 0, 255), 5, cv.LINE_AA)

# Display images generated along the way
if convolve_with_gaussian:
    if displayBlurred:
        cv.imshow("blur", image_blurred)
    if displaySubtracted:
        cv.imshow("Subtracted", image_subtracted)

if applyContrast & displayContrast:
    cv.imshow("Contrast", contrasted)

if binaryThresh & displayBinaryThresh:
    cv.imshow("Binary", image_binary)

if createTemplate & tempCoords & displayTemplate:
    cv.imshow("template", template)

if createTemplate & matchTemplates & tempCoords & displayMatchingResult:
    cv.imshow("template matching", tempImage)

if closing & displayClosing:
    cv.imshow("Morphology", image_closed)

if grassfired & displayGrassfire:
    cv.imshow("Grassfire", image_grassfire)

if testing:
    cv.imwrite(F'Output/Test2/{currentDirectory}/{currentImageName}_result.png', tempImage)
    cv.imwrite(F'Output/Test2/{currentDirectory}/{currentImageName}_final.png', contrasted)
    cv.imwrite(F'Output/Test2/{currentDirectory}/{currentImageName}_template.png', template)

cv.waitKey(0)
