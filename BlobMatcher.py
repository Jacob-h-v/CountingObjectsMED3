import cv2 as cv
import numpy as np

def FilterBlobs(template_features, blobs):
    templateSize = template_features[1]
    templateBoxCoords = template_features[2]
    templateBoxRatio = (templateBoxCoords[3] - templateBoxCoords[1]) / (templateBoxCoords[2] - templateBoxCoords[0])
    blobbestOfBlobs = []

    print(f"template box ratio: {templateBoxRatio}")

    for blob in blobs:
        blobBoxCoords = blob[2]
        blobBoxRatio = (blobBoxCoords[3] - blobBoxCoords[1]) / (
                blobBoxCoords[2] - blobBoxCoords[0])

        # Euclidean Distance
        #distance = np.sqrt((np.float(blob[1]/templateSize) - templateSize/blob[1]) * (np.float(blob[1]/templateSize) - templateSize/blob[1]) + (blobBoxRatio - templateBoxRatio) * (blobBoxRatio - templateBoxRatio))
        #print(distance)

        # Box Clasifier
        if (templateSize * 0.15) < blob[1] < (templateSize * 1.3):
            #print(f"{blobBoxRatio}")
            if (templateBoxRatio * 0.5) < blobBoxRatio < (templateBoxRatio * 1.3):
                blobbestOfBlobs.append(blob)
    return blobbestOfBlobs