import cv2 as cv
import numpy as np

def RemoveEdgeBlobs(grassfire_image):
    for y in range(grassfire_image.shape[0]):
        for x in range(grassfire_image.shape[1]):
            if grassfire_image[y, x] != 0:
                if y == 0 or x == 0 or y == grassfire_image.shape[0]-1 or x == grassfire_image.shape[1]-1:
                    currentID = grassfire_image[y, x]
                    for z in range(grassfire_image.shape[0]):
                        for i in range(grassfire_image.shape[1]):
                            if grassfire_image[z, i] == currentID:
                                grassfire_image[z, i] = 0

    return grassfire_image

def CategorizeFeatures(input_image):
    blobID = 0
    Blobs = []
    PreviousIDs = []

    for y in range(input_image.shape[0]):
        for x in range(input_image.shape[1]):
            if input_image[y, x] != 0:
                if PreviousIDs.count(input_image[y, x]) == 0:
                    blobID = blobID + 1

                    xMax = x
                    xMin = x
                    yMax = y
                    yMin = y

                    blobSize = 0
                    currentID = input_image[y, x]
                    for z in range(input_image.shape[0]):
                        for i in range(input_image.shape[1]):
                            if input_image[z, i] == currentID:
                                blobSize = blobSize + 1
                                if i > xMax:
                                    xMax = i
                                if i < xMin:
                                    xMin = i
                                if z > yMax:
                                    yMax = z
                                if z < yMin:
                                    yMin = z

                    Boundingbox = [xMin, yMin, xMax, yMax]
                    PreviousIDs.append(currentID)
                    Blob = [currentID, blobSize, Boundingbox]
                    Blobs.append(Blob)

    return Blobs

def DefineTemplateFeatures(input_image, template_coordinates, kernel_size):
    oriImage = input_image.copy()
    refPoint = [(template_coordinates[0] - kernel_size, template_coordinates[1] - kernel_size), (template_coordinates[2] - kernel_size, template_coordinates[3] - kernel_size)]
    if len(refPoint) == 2:  # when two points were found
        roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]

    #cv.imshow("Blob Template", roi)

    Blobs = CategorizeFeatures(roi)

    BlobSizes = []

    for i in range(len(Blobs)):
        BlobSizes.append(Blobs[i][1])

    BiggestBlob = max(BlobSizes)

    for z in range(len(Blobs)):
        if Blobs[z][1] == BiggestBlob:
            template_features = Blobs[z]

    return template_features
