import cv2 as cv
import numpy as np
from Morphology import inbuiltMorphology, OpType

# RemoveEdgeBlobs() takes a grassfired image as an input and returns the image
# with all blobs in contact with the edge removed
def RemoveEdgeBlobs(grassfire_image):
    # Iterates over all pixels
    for y in range(grassfire_image.shape[0]):
        for x in range(grassfire_image.shape[1]):
            # Only checks when hitting blobs
            if grassfire_image[y, x] != 0:
                # Checks All Edge Values
                if y == 0 or x == 0 or y == grassfire_image.shape[0]-1 or x == grassfire_image.shape[1]-1:
                    # Saves the hit pixels ID
                    currentID = grassfire_image[y, x]
                    # Iterates again over all pixels to check for similar ID's
                    for z in range(grassfire_image.shape[0]):
                        for i in range(grassfire_image.shape[1]):
                            # Removes all pixels with the currentID in the image
                            if grassfire_image[z, i] == currentID:
                                grassfire_image[z, i] = 0

    return grassfire_image

# FindPerimeter() takes a morphed image as an input and returns a list of all blob's perimeters
def FindPerimeter(blob_image):
    # Creates an image with only the perimeters by eroding the image
    # Then subtracting the eroded image with the original
    eroded_image = inbuiltMorphology(blob_image, 3, OpType.Erosion)
    edge_image = cv.subtract(blob_image, eroded_image)
    # cv.imshow("Edges", edge_image)

    # Creates two lists of all ID's it has already counted and a list for all perimeter values
    PreviousIDs = []
    Perimeters = []

    # Iterates over all pixels in image with only edges
    for y in range(edge_image.shape[0]):
        for x in range(edge_image.shape[1]):
            # Checks if value is a blob and if it is not already been counted
            # This is to not count the blob as a new for each pixel it encounters
            if edge_image[y, x] != 0:
                if PreviousIDs.count(edge_image[y, x]) == 0:

                    # Saves currentID as the pixel value and puts it in PreviousIDs list
                    currentID = edge_image[y, x]
                    PreviousIDs.append(currentID)

                    # Counts the blobsize of the edges and saves them in the list Perimeters
                    blobSize = 0
                    for z in range(edge_image.shape[0]):
                        for i in range(edge_image.shape[1]):
                            if edge_image[z, i] == currentID:
                                blobSize = blobSize + 1

                    Perimeters.append(blobSize)

    return Perimeters

# CategorizeFeatures() takes an image with blobs and returns a list
# containing a list for each blob with each feature represented by a value or set of coordinates
def CategorizeFeatures(input_image):

    # Defines internal blobID value and two lists for all blobs and one to check all previous IDs
    blobID = 0
    Blobs = []
    PreviousIDs = []

    # Gets a list of perimeters from the FindPerimeter function from this script
    Perimeters = FindPerimeter(input_image)

    # Iterates over all pixels
    for y in range(input_image.shape[0]):
        for x in range(input_image.shape[1]):

            # If the pixel have a value and has not been counted yet, it continues
            if input_image[y, x] != 0:
                if PreviousIDs.count(input_image[y, x]) == 0:

                    # Updates blobID variable
                    blobID = blobID + 1

                    # Defines and finds variables for boundingbox
                    xMax = x
                    xMin = x
                    yMax = y
                    yMin = y

                    blobSize = 0
                    currentID = input_image[y, x]

                    # Iterates over all pixels again to find similar IDs
                    for z in range(input_image.shape[0]):
                        for i in range(input_image.shape[1]):
                            if input_image[z, i] == currentID:

                                # Counts blobsize
                                blobSize = blobSize + 1

                                # Updates bounding box variables if value is higher or lower
                                if i > xMax:
                                    xMax = i
                                if i < xMin:
                                    xMin = i
                                if z > yMax:
                                    yMax = z
                                if z < yMin:
                                    yMin = z

                    # Puts all relevant variables in lists
                    Boundingbox = [xMin, yMin, xMax, yMax]
                    PreviousIDs.append(currentID)
                    Blob = [currentID, blobSize, Boundingbox, Perimeters[blobID-1]]
                    Blobs.append(Blob)

    return Blobs

# DefineTemplateFeatures() takes an image, the template coordinates from cropping
# And the kernelsize to compensate for changes pre-processing and returns a list of features describing
# the biggest blob found within the template coordinates area
def DefineTemplateFeatures(input_image, template_coordinates, kernel_size):

    # Takes the input image and crops the template from the input image
    oriImage = input_image.copy()
    refPoint = [(template_coordinates[0] - kernel_size, template_coordinates[1] - kernel_size), (template_coordinates[2] - kernel_size, template_coordinates[3] - kernel_size)]
    if len(refPoint) == 2:  # when two points were found
        roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]

    #cv.imshow("Blob Template", roi)

    # Runs the template image through the CategorizeFeatures() function from this script
    Blobs = CategorizeFeatures(roi)

    # Initializes two list for blobsizes and template_features
    BlobSizes = [0]
    template_features = [0, 0]

    # Puts all blobsizes into a single list
    for i in range(len(Blobs)):
        BlobSizes.append(Blobs[i][1])

    # Finds the biggest value of all the found blobs
    BiggestBlob = max(BlobSizes)

    # if no blob was found it prints a error message
    if BiggestBlob < 1:
        print("BiggestBlob not found")

    # Loops over all blobs and sets the template features to be equal to the biggest blob
    for z in range(len(Blobs)):
        if Blobs[z][1] == BiggestBlob:
            template_features = Blobs[z]

    # Returns a list of all features for the biggest blob as the template blob
    return template_features
