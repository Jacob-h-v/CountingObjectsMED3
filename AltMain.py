import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, image
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter, convolve, generate_gaussian_kernel

template = template_cropping(image)
template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
template_arr = np.array(template_gray)
template_processed = median_filter(template_arr, 3)

image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
image_arr = np.array(image_gray)
image_processed = median_filter(image_gray, 3)

gaussian_radius = 25
gaussian_kernel = generate_gaussian_kernel(gaussian_radius, 200)
image_blurred = convolve(image_processed, gaussian_kernel)
new_size = (image_processed.shape[1] - gaussian_radius*2, image_processed.shape[0] - gaussian_radius*2)
image_resize = cv.resize(image_processed, new_size, interpolation= cv.INTER_LINEAR)
image_subtracted = cv.subtract(image_resize, image_blurred)
img_subtracted = image_resize - image_blurred

templateMatching_result = TemplateMatching(image, image_processed, template_processed)

cv.imshow("resize", image_resize)
cv.imshow("manual", img_subtracted)
cv.imshow("blur", image_blurred)
cv.imshow("subtracted", image_subtracted)
cv.imshow("template", template)
cv.imshow("template matching", templateMatching_result)
cv.waitKey(0)