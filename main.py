# This is the beginning of the MED3 "counting things" project.

# Let's fix some version control.

from NoiseReduction import *
from CroppingTemplate import template_cropping
from TemplateMatchingAutomated import TemplateMatching

imageInput = cv.imread("Resources/input picture.jpg")
imageInput_gray = cv.cvtColor(imageInput, cv.COLOR_BGR2GRAY)
imageInput_arr = np.array(imageInput_gray)

reduceNoise = True
cropPicture = True
matchTemplate = True
erode = True
dilate = True

# Manual user cropping for finding initial template
def RunTemplateCropping(imageInput):
    CroppedPic = template_cropping(imageInput)
    return CroppedPic

def RunNoiseReduction():
    nrInput = cv.imread("Output/CroppedPicture.jpg")
    nrInput_gray = cv.cvtColor(nrInput, cv.COLOR_BGR2GRAY)
    nrInput_arr = np.array(nrInput_gray)
    nrOutput = median_filter(nrInput_arr, 3)
    return nrOutput

def RunTemplateMatching():
    TemplateMatching(inputPic_gray, noiseGone)
    result = cv.imread("Output/TemplateMatched.png")
    return result


if cropPicture:
    template = RunTemplateCropping(imageInput)

if reduceNoise:
    RunNoiseReduction()
    noiseGone = RunNoiseReduction()

#if erode:

    # run erosion from morphology script

#if dilate:

    # run dilation from morphology script

if matchTemplate:
    RunTemplateMatching()
    templateMatchingResult = RunTemplateMatching()

cv.imshow("Filtered Image", noiseGone)
cv.imshow("Input Image", imageInput)
cv.imshow("TemplateMatched", templateMatchingResult)
cv.waitKey(0)
