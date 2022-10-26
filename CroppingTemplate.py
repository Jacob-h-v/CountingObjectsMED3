import cv2
import numpy as np
cropping = False
showCropping = True
x_start, y_start, x_end, y_end = 0, 0, 0, 0
image = cv2.imread('Resources/1M-2L-1P-1CL-1C (1).png')
imageTest = cv2.imread('Resources/1M-2L-1P-1CL-1C (1).png')
oriImage = image.copy()

def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping, showCropping
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)
            cv2.imwrite('Output/CroppedPicture.jpg', roi)
            #showCropping = False

def template_cropping(inputImage):
    global image, oriImage
    image = inputImage
    oriImage = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)

    while showCropping:
        i = image.copy()
        if not cropping:
            cv2.imshow("image", image)
        elif cropping:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
            cv2.imshow("image", i)
        cv2.waitKey(1)
    # close all open windows
    cv2.destroyAllWindows()


template_cropping(imageTest)