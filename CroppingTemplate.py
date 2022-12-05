import cv2 as cv
import numpy as np
import math

cropping = False
showCropping = True
x_start, y_start, x_end, y_end = 0, 0, 0, 0
tempimage = cv.imread("Resources/1M-2L-1P-1CL-1C (1).png")

def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping, showCropping
    oriImage = tempimage.copy()

    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving
    elif event == cv.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    # if the left mouse button was released
    elif event == cv.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished
        showCropping = False
        #refPoint = [(x_start, y_start), (x_end, y_end)]
        #if len(refPoint) == 2: #when two points were found
            #roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            #cv.imshow("Cropped", roi)
            #cv.imwrite('Output/CroppedPicture.jpg', roi)
            #showCropping = False

def template_cropping(image):
    cv.namedWindow("image")
    tempimage = image
    cv.setMouseCallback("image", mouse_crop)

    while showCropping:
        i = image.copy()
        if not cropping:
            cv.imshow("image", image)
        elif cropping:
            cv.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
            cv.imshow("image", i)
        cv.waitKey(1)
    # close all open windows
    cv.destroyAllWindows()
    result = [x_start, y_start, x_end, y_end]
    return result

def crop(image, x_start, y_start, x_end, y_end):
    oriImage = image.copy()
    refPoint = [(x_start, y_start), (x_end, y_end)]
    if len(refPoint) == 2:  # when two points were found
        roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
        # cv.imwrite('Output/CroppedPicture.jpg', roi)
    return roi

def combinedCrop(image):
    tempCoords = template_cropping(image)
    template = crop(image, tempCoords[0], tempCoords[1], tempCoords[2], tempCoords[3])

    return template

#croppedPic = template_cropping(image)
#print(croppedPic)

#cropped = crop(image, croppedPic[0], croppedPic[1], croppedPic[2], croppedPic[3])

#cv.imshow("crop", cropped)
#cv.waitKey(0)

# cv.imshow("result", croppedPic)