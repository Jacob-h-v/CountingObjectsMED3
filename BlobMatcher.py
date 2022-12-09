import cv2 as cv
import numpy as np
import math

def FilterBlobs(template_features, blobs):
    templateSize = template_features[1]
    templateBoxCoords = template_features[2]
    templateBoxRatio = (templateBoxCoords[3] - templateBoxCoords[1]) / (templateBoxCoords[2] - templateBoxCoords[0])
    templatePerimeter = template_features[3]
    templateCircularity = templatePerimeter / (2 * math.sqrt(math.pi * templateSize)) # (4 * 3.14 * templateSize) / (templatePerimeter ^ 2)
    print(templateCircularity)

    blobbestOfBlobs = []

    print(f"template box ratio: {templateBoxRatio}")

    for blob in blobs:
        blobSize = blob[1]
        blobBoxCoords = blob[2]
        blobBoxRatio = (blobBoxCoords[3] - blobBoxCoords[1]) / (
                blobBoxCoords[2] - blobBoxCoords[0])
        currentPerimeter = blob[3]
        circularity = currentPerimeter / (2 * math.sqrt(math.pi * blobSize)) # (4 * 3.14 * blob[1]) / (currentPerimeter ^ 2)
        print(circularity)

        # Box Clasifier
        if (templateSize * 0.15) < blobSize < (templateSize * 1.85):
            if (templateBoxRatio * 0.5) < blobBoxRatio < (templateBoxRatio * 1.5):
                if (templateCircularity * 0.75) < circularity < (templateCircularity * 1.25):
                    blobbestOfBlobs.append(blob)

    return blobbestOfBlobs