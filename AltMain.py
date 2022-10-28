import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping
from TemplateMatchingAutomated import TemplateMatching

inputImage = cv.imread("Resources/1M-2L-1P-1CL-1C (1).png")
# inputImage_gray = cv.cvtColor(inputImage, cv.COLOR_BGR2GRAY)

template = template_cropping(inputImage)
template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

templateMatching_result = TemplateMatching(inputImage, template_gray)

cv.imshow("template", template)
cv.imshow("template matching", templateMatching_result)
cv.waitKey(0)