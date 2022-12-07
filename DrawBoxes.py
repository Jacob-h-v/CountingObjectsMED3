import cv2 as cv


def DrawBlobBox(image, blobs, kernelradius):
    for blob in blobs:
        # startX = blob[2]
        # startY = blob[2]
        # endX = blob[2]
        # endY = blob[2]
        # blobbies = blobs[2]
        startX, startY, endX, endY = blob[2]
        print(startX, startY, endX, endY)
        cv.rectangle(image, (startX + kernelradius, startY + kernelradius), (endX + kernelradius, endY + kernelradius),
                     (0, 0, 255), 3)
    # show the output image
    return image