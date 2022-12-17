import cv2 as cv
import numpy as np
import math

# FilterBlobs() Takes the list of all blobs and their features and the templates features as an input
# Then returns a list of all remaining blobs after being compared to the templates features
def FilterBlobs(template_features, blobs):

    # Defines the template features as values to hold track of them easier
    templateSize = template_features[1]
    templateBoxCoords = template_features[2]
    templateBoxRatio = (templateBoxCoords[3] - templateBoxCoords[1]) / (templateBoxCoords[2] - templateBoxCoords[0])
    templatePerimeter = template_features[3]
    templateCircularity = templatePerimeter / (2 * math.sqrt(math.pi * templateSize)) # (4 * 3.14 * templateSize) / (templatePerimeter ^ 2)

    # Initializes the list where all accepted blobs will be put into
    blobbestOfBlobs = []

    print(f"template size: {templateSize}")
    print(f"template box ratio: {templateBoxRatio}")
    print(f"template size: {templateCircularity}")

    # Iterates over the list of all blobs
    for blob in blobs:

        # Defines the current blobs feature into variables to calculate individual features
        blobSize = blob[1]
        blobBoxCoords = blob[2]
        blobBoxRatio = (blobBoxCoords[3] - blobBoxCoords[1]) / (
                blobBoxCoords[2] - blobBoxCoords[0])
        currentPerimeter = blob[3]
        circularity = currentPerimeter / (2 * math.sqrt(math.pi * blobSize)) # (4 * 3.14 * blob[1]) / (currentPerimeter ^ 2)

        # Checks the blobs using a Box Clasifier where they are compared to the template
        # Within a procent variation and puts similar blobs into a list
        if (templateSize * 0.15) < blobSize < (templateSize * 1.85):
            if (templateBoxRatio * 0.7) < blobBoxRatio < (templateBoxRatio * 1.3):
                #if (templateCircularity * 0.75) < circularity < (templateCircularity * 1.25):
                blobbestOfBlobs.append(blob)

    # Returns list of remaining blobs
    return blobbestOfBlobs