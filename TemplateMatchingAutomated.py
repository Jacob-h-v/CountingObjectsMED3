import cv2 as cv
import numpy as np
from NonMaximaSupression import non_max_suppression

#read image
inputPic = cv.imread("Resources/input picture.jpg")

#convert the image
input_gray = cv.cvtColor(inputPic, cv.COLOR_BGR2GRAY)

templateTest = cv.imread("Output/CroppedPicture.jpg", 0)

def TemplateMatching(image, template):
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    tH, tW = template.shape[:2]

    res = cv.matchTemplate(image_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    (yCoords, xCoords) = np.where(res >= threshold)

    rects = []
    for (x, y) in zip(xCoords, yCoords):
        rects.append((x, y, x + tW, y + tH))

    pick = non_max_suppression(np.array(rects), 0.1)
    print(len(pick))

    # loop over the final bounding boxes
    for (startX, startY, endX, endY) in pick:
        # draw the bounding box on the image
        cv.rectangle(image, (startX, startY), (endX, endY),
                      (0, 0, 255), 3)
    # show the output image
    return image
    #cv.imshow("Result", image)
    #cv.waitKey(0)

# TemplateMatching(inputPic, templateTest)