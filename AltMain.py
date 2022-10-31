import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, image
from TemplateMatchingAutomated import TemplateMatching
from NoiseReduction import median_filter

template = template_cropping(image)
template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
template_arr = np.array(template_gray)
template_processed = median_filter(template_arr, 3)

image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
image_arr = np.array(image_gray)
image_processed = median_filter(image_gray, 3)

templateMatching_result = TemplateMatching(image, image_processed, template_processed)

cv.imshow("template", template)
cv.imshow("template matching", templateMatching_result)
cv.waitKey(0)