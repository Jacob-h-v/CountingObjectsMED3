import cv2 as cv
import numpy as np


def FilterBlobs(template_features, blobs):
    templateSize = template_features[1]
    blobbestOfBlobs = []
    for blob in blobs:
        if (templateSize * 0.15) < blob[1] < (templateSize * 1.3):
            blobbestOfBlobs.append(blob)
    return blobbestOfBlobs