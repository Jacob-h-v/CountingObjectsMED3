# Source:
# Daniel Shiffman
# http://codingtra.in
# http://patreon.com/codingtrain
# Code for: https://youtu.be/1scFcY-xMrI
# https://github.com/CodingTrain/website-archive/blob/main/Tutorials/Processing/11_video/sketch_11_8_BlobTracking_improved/sketch_11_8_BlobTracking_improved.pde

import Blobber
import cv2 as cv
import numpy as np

imageInput = cv.imread("Output/Test2/Lego/GreenBackground/3L-2L-1P-1CL-2C-16A (3).JPEG_final.png")
trackColor = (0, 0, 255)
threshold = 100
distanceThreshold = 50

Blobbies = []

def setup(image, color):
    global trackColor
    size = image.shape[:, :, :]
    input = image
    trackColor = color

def find_blobs(image, trackColor, minSize):
   global Blobbies
   Blobbies.clear()
   blueTrack = trackColor[0]
   greenTrack = trackColor[1]
   redTrack = trackColor[2]
   for y in range(image.shape[0]):
       for x in range (image.shape[1]):
           tempLocation = (y, x)
           blue = image[y, x, 0]
           green = image[y, x, 1]
           red = image[y, x, 2]
           tempDist = np.sum(np.square(np.subtract((blue, green, red), (blueTrack, greenTrack, redTrack))))

           if(tempDist < threshold & threshold):
               found = False
               for Blob in Blobbies:
                   if(Blobber.Blob.is_near(Blobber.Blob, y, x, 25)):
                       Blobber.Blob.add_point(Blobber.Blob, y, x)
                       found = True
                       break

               if not found:
                   Blob = Blobber.Blob.new_blob(Blobber.Blob, y, x, 25)
                   Blobbies.append(Blob)

   for blob in Blobbies:
       if Blobber.Blob.blob_size(blob) > minSize:
           blobSize = Blobber.Blob.blob_size(Blobber.Blob)
           xmin, ymin, xmax, ymax = Blobber.Blob.get_blob_coords(Blobber.Blob)
           return blobSize, xmin, ymin, xmax, ymax





testSize, xmin, ymin, xmax, ymax = find_blobs(imageInput, (50, 20, 20), 50)
print(testSize, xmin, ymin, xmax, ymax)
