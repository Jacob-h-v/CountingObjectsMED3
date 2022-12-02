import cv2 as cv
import numpy as np
import os

from CroppingTemplate import template_cropping, crop, combinedCrop

directory = 'Resources\JPEGbilleder\Coins\GreenBackground'

for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".JPEG"):

        cropping_image = cv.imread(f"{directory}/{filename}")

        scale_percent = 50  # percent of original size
        width = int(cropping_image.shape[1] * scale_percent / 100)
        height = int(cropping_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        cropping_image = cv.resize(cropping_image, dim, interpolation=cv.INTER_AREA)

        tempCoords = template_cropping(cropping_image)
        template = crop(cropping_image, tempCoords[0], tempCoords[1], tempCoords[2], tempCoords[3])
        tempCoords.clear()

        cv.imwrite(f'{directory}/template_{filename}', template)
        cv.imshow("image", template)
        cv.waitKey(0)