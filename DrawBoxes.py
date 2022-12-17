import cv2 as cv

# DrawBlobBox() takes the original image, list of blobs and kernel radius as input
# and returns an image where all bounding boxes have been visualized with a red rectangle upon
def DrawBlobBox(image, blobs, kernelradius):

    # Iterates over all blobs
    for blob in blobs:

        # Defines coordinates based upon the third index in the feature list
        startX, startY, endX, endY = blob[2]

        # Then it draws the bounding box on the original image and
        cv.rectangle(image, (startX + kernelradius, startY + kernelradius), (endX + kernelradius, endY + kernelradius),
                     (0, 0, 255), 3)
    return image