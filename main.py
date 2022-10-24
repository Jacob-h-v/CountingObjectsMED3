# This is the beginning of the MED3 "counting things" project.

# Let's fix some version control.

from NoiseReduction import *
# from CroppingTemplate import *

imageInput = cv.imread("Resources/input picture.jpg")
imageInput_gray = cv.cvtColor(imageInput, cv.COLOR_BGR2GRAY)
imageInput_arr = np.array(imageInput_gray)

reduceNoise = True
cropPicture = True
matchTemplate = True
erode = True
dilate = True


#def RunCroppingTemplate():

    # Crop to relevant part of photo here and then crop to template later after cleaning up the photo?


def RunNoiseReduction():
    nrInput = cv.imread("Output/CroppedPicture.jpg")
    nrInput_gray = cv.cvtColor(nrInput, cv.COLOR_BGR2GRAY)
    nrInput_arr = np.array(nrInput_gray)
    nrOutput = median_filter(nrInput_arr, 3)
    return nrOutput


#if cropPicture:
    #RunCroppingTemplate()

if reduceNoise:
    RunNoiseReduction()
    noiseGone = RunNoiseReduction()

#if erode:

    # run erosion from morphology script

#if dilate:

    # run dilation from morphology script


cv.imshow("Filtered Image", noiseGone)
cv.imshow("Input Image", imageInput)
cv.waitKey(0)
