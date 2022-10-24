# This is the beginning of the MED3 "counting things" project.

# Let's fix some version control.

from NoiseReduction import *

imageInput = cv.imread("Resources/input picture.jpg")
imageInput_gray = cv.cvtColor(imageInput, cv.COLOR_BGR2GRAY)
imageInput_arr = np.array(imageInput_gray)

reduceNoise = True
cropPicture = True

def RunCroppingTemplate():
    cropOutput = True
    # This stuff needs to be coded. Does nothing right now.
    return cropOutput


def RunNoiseReduction():
    nrInput = cv.imread("Output/CroppedPicture.jpg")
    nrInput_gray = cv.cvtColor(nrInput, cv.COLOR_BGR2GRAY)
    nrInput_arr = np.array(imageInput_gray)
    nrOutput = median_filter(imageInput, 3)
    return nrOutput

if reduceNoise:
    RunNoiseReduction()
    noiseGone = RunNoiseReduction()

cv.imshow("Filtered Image", noiseGone)
cv.imshow("Input Image", imageInput)
cv.waitKey(0)
