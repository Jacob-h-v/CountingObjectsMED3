import cv2 as cv


def DrawBlobBox(image, blobs, kernelradius):
    for blob in blobs:
        startX, startY, endX, endY = blob[2]
        cv.rectangle(image, (startX + kernelradius, startY + kernelradius), (endX + kernelradius, endY + kernelradius),
                     (0, 0, 255), 3)
    return image