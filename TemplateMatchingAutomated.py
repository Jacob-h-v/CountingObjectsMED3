import cv2 as cv
import numpy as np
from NonMaximaSupression import non_max_suppression

#read image
inputPic = cv.imread("Resources/input picture.jpg")

#convert the image
input_gray = cv.cvtColor(inputPic, cv.COLOR_BGR2GRAY)

templateTest = cv.imread("Output/CroppedPicture.jpg", 0)

def TemplateMatching(image, processed, template, kernelsize):
    #image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = np.array(image, dtype=np.uint8)
    processed = np.array(processed, dtype=np.uint8)
    template = np.array(template, dtype=np.uint8)
    tH, tW = template.shape[:2]

    res = cv.matchTemplate(processed, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.3
    (yCoords, xCoords) = np.where(res >= threshold)

    rects = []
    for (x, y) in zip(xCoords, yCoords):
        rects.append((x, y, x + tW, y + tH))

    pick = non_max_suppression(np.array(rects), 0.1)
    resultAmount = len(pick)
    print(resultAmount)

    # loop over the final bounding boxes
    for (startX, startY, endX, endY) in pick:
        # draw the bounding box on the image
        cv.rectangle(image, (startX + kernelsize, startY + kernelsize//2), (endX + kernelsize, endY + kernelsize//2),
                      (0, 0, 255), 3)
    # show the output image
    return image, resultAmount
    #cv.imshow("Result", image)
    #cv.waitKey(0)

# TemplateMatching(inputPic, templateTest)