import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, tempimage, crop
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel
from Morphology import inbuiltMorphology, OpType

# Runs the template cropping script which returns cropped coordinates
template_coords = template_cropping(tempimage)

# Taking the image and reducing noise by putting it through a median filter
image_gray = cv.cvtColor(tempimage, cv.COLOR_BGR2GRAY)
image_arr = np.array(image_gray)
image_processed = median_filter(image_gray, 3)

# Creating a Gaussian Kernel and convoluting it to the Image to create a blured image
gaussian_radius = 25
gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 500)
image_blurred = convolve(image_processed, gaussian_kernel)

# Resizing the image, so it matches the size of the blurred image after convolution
image_resize = image_processed[gaussian_radius:image_processed.shape[0]-gaussian_radius, gaussian_radius:image_processed.shape[1]-gaussian_radius]

# Subtracting the blurred image from the image to remove the background and highlight the objects
image_subtracted = cv.subtract(image_resize, image_blurred)

# Binary thresholding
ret, image_binary = cv.threshold(image_subtracted, 25, 255, cv.THRESH_BINARY)

# Morphology
image_morphed = inbuiltMorphology(image_binary, 5, OpType.Dilation)
image_morphed = inbuiltMorphology(image_morphed, 5, OpType.Erosion)

# Creating Template
template = crop(image_morphed, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)

# Manual subtraction
#img_subtracted = image_resize - image_blurred

#for y in range(img_subtracted.shape[0]):
    #for x in range(img_subtracted.shape[1]):
        #if img_subtracted[y, x] <= 0:
            #img_subtracted[y, x] = 0

# Runs the template matching function using the processed images
templateMatching_result = TemplateMatching(tempimage, image_morphed, template, gaussian_radius)

#cv.imshow("manual", img_subtracted)
cv.imshow("blur", image_blurred)
cv.imshow("Subtracted", image_subtracted)
cv.imshow("Binary", image_binary)
cv.imshow("Morphed", image_morphed)
cv.imshow("template", template)
cv.imshow("template matching", templateMatching_result)
cv.waitKey(0)