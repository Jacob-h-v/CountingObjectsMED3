import cv2 as cv

cropping = False
showCropping = True
x_start, y_start, x_end, y_end = 0, 0, 0, 0
tempimage = cv.imread("Resources/1M-2L-1P-1CL-1C (1).png")

# mouse_crop() is the event called in template_cropping() as a setMouseCallBack
# and handles the actual user inputs
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping, showCropping
    oriImage = tempimage.copy()

    # If the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being cropped
    if event == cv.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving
    elif event == cv.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    # If the left mouse button was released
    elif event == cv.EVENT_LBUTTONUP:
        # Records the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # Cropping is finished
        showCropping = False # Cropping window is closed

# template_cropping() takes an input image and returns a list of coordinates indicating the template area
# Takes originally inspiration from: https://www.life2coding.com/crop-image-using-mouse-click-movement-python/
def template_cropping(image):

    # Opens window with name image with the input picture
    cv.namedWindow("image")
    tempimage = image

    # Runs the mouse_crop as a MouseCallback event to take the users mouse input
    cv.setMouseCallback("image", mouse_crop)

    # Within the while statement is where the red rectangle is being drawn while the user is currently cropping
    while showCropping:
        i = image.copy()
        if not cropping:
            cv.imshow("image", image)
        elif cropping:
            cv.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)
            cv.imshow("image", i)
        cv.waitKey(1)

    # Close all open windows
    cv.destroyAllWindows()

    # Saves all the final coordinates in a list called result then returning it
    result = [x_start, y_start, x_end, y_end]
    return result

# Crop() takes the image and coordinates and crops the image accordingly
def crop(image, x_start, y_start, x_end, y_end):
    oriImage = image.copy()
    refPoint = [(x_start, y_start), (x_end, y_end)]
    if len(refPoint) == 2:  # when two points were found
        roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
        # cv.imwrite('Output/CroppedPicture.jpg', roi)
    return roi

# combinedCrop() takes the two above functions and runs them one after another
def combinedCrop(image):
    tempCoords = template_cropping(image)
    template = crop(image, tempCoords[0], tempCoords[1], tempCoords[2], tempCoords[3])

    return template