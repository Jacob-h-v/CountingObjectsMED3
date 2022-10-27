import cv2 as cv
import numpy as np

#read image
inputPic = cv.imread("Resources/1M-2L-1P-1CL-1C (1).png")

#convert the image
input_gray = cv.cvtColor(inputPic, cv.COLOR_BGR2GRAY)

templateTest = cv.imread("Output/CroppedPicture.jpg", 0)

def TemplateMatching(image, template):
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    w, h = template.shape[::-1]

    res = cv.matchTemplate(image_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.2
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)


    #showing the result
    # cv.imshow("Correlation", res)
    cv.imwrite('Output/TemplateMatched.png', image)
    cv.imshow("Result", image)
    cv.waitKey(0)

TemplateMatching(inputPic, templateTest)