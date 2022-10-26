import cv2 as cv
import numpy as np

#read image
inputPic = cv.imread("Resources/input picture.jpg")

#convert the image
input_gray = cv.cvtColor(inputPic, cv.COLOR_BGR2GRAY)

templateTest = cv.imread("Output/CroppedPicture.jpg", 0)

def TemplateMatching(image, template):
    w, h = template.shape[::-1]

    res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv.rectangle(inputPic, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    #showing the result
    # cv.imshow("Correlation", res)
    cv.imwrite('Output/TemplateMatched.png', inputPic)
    cv.imshow("Result", inputPic)
    cv.waitKey(0)

TemplateMatching(input_gray, templateTest)