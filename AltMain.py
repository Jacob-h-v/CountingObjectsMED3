import cv2 as cv
import numpy as np

from CroppingTemplate import template_cropping, image
from TemplateMatchingAutomated import TemplateMatching

template = template_cropping(image)
template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

templateMatching_result = TemplateMatching(image, template_gray)

cv.imshow("template", template)
cv.imshow("template matching", templateMatching_result)
cv.waitKey(0)