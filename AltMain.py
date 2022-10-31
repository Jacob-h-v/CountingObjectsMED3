import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, image, crop
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel

# Runs the template cropping script which returns cropped coordinates
template_coords = template_cropping(image)

# Taking the image and reducing noise by putting it through a median filter
image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
image_arr = np.array(image_gray)
image_processed = median_filter(image_gray, 3)

# Creating a Gaussian Kernel and convoluting it to the Image to create a blured image
gaussian_radius = 25
gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 500)
image_blurred = convolve(image_processed, gaussian_kernel)

# Resizing the image, so it matches the size of the blurred image after convolution
new_image_size = (image_processed.shape[1] - gaussian_radius*2, image_processed.shape[0] - gaussian_radius*2)
image_resize = cv.resize(image_processed, new_image_size, interpolation= cv.INTER_LINEAR)

# Subtracting the blurred image from the image to remove the background and highlight the objects
image_subtracted = cv.subtract(image_resize, image_blurred)

# Creating Template
template = crop(image_subtracted, template_coords[0] - gaussian_radius, template_coords[1] - gaussian_radius, template_coords[2] - gaussian_radius, template_coords[3] - gaussian_radius)

# Manual subtraction
#img_subtracted = image_resize - image_blurred

#for y in range(img_subtracted.shape[0]):
    #for x in range(img_subtracted.shape[1]):
        #if img_subtracted[y, x] <= 0:
            #img_subtracted[y, x] = 0

# Runs the template matching function using the processed images
templateMatching_result = TemplateMatching(image, image_subtracted, template, gaussian_radius)

#cv.imshow("manual", img_subtracted)
cv.imshow("blur", image_blurred)
cv.imshow("subtracted", image_subtracted)
cv.imshow("template", template)
cv.imshow("template matching", templateMatching_result)
cv.waitKey(0)