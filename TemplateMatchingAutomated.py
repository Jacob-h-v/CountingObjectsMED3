import cv2 as cv
import numpy as np
from NonMaximaSupression import non_max_suppression

#read image
inputPic = cv.imread("Resources/input picture.jpg")

#convert the image
input_gray = cv.cvtColor(inputPic, cv.COLOR_BGR2GRAY)

templateTest = cv.imread("Output/CroppedPicture.jpg", 0)

def TemplateMatching(image, processed, template, kernelsize):
    image = np.array(image, dtype=np.uint8)
    processed = np.array(processed, dtype=np.uint8)
    template = np.array(template, dtype=np.uint8)

    template_90 = cv.rotate(template, cv.ROTATE_90_CLOCKWISE)
    template_180 = cv.rotate(template_90, cv.ROTATE_90_CLOCKWISE)
    template_270 = cv.rotate(template_180, cv.ROTATE_90_CLOCKWISE)

    rotations = [template, template_90, template_180, template_270]

    rects = []
    for i in range(len(rotations)):
        temp = rotations[i]

        tH, tW = temp.shape[:2]

        res = cv.matchTemplate(processed, temp, cv.TM_CCOEFF_NORMED)
        threshold = 0.40
        (yCoords, xCoords) = np.where(res >= threshold)

        for (x, y) in zip(xCoords, yCoords):
            rects.append((x, y, x + tW, y + tH))
        # print(f"Iteration: {i}: {xCoords}, {yCoords}")

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