# Source:
# Daniel Shiffman
# http://codingtra.in
# http://patreon.com/codingtrain
# Code for: https://youtu.be/1scFcY-xMrI

import numpy as np


class Blob:
    minX = 0
    minY = 0
    maxX = 0
    maxY = 0
    points = []
    maxDistance = 5

    def __init__(self):
        Blob.minX = 0
        Blob.minY = 0
        Blob.maxX = 0
        Blob.maxY = 0
        Blob.points = []
        Blob.maxDistance = 5

    def new_blob(self, y, x, distanceThreshold):
        Blob.minX = x
        Blob.minY = y
        Blob.maxX = x
        Blob.maxY = y
        Blob.points.append((y, x))
        Blob.maxDistance = distanceThreshold
        # print(f"New blob added. minX: {self.minX}, minY: {self.minY}, maxX: {self.maxX}, maxY: {self.maxY}")

    def add_point(self, y, x):
        Blob.points.append((y, x))
        Blob.minX = min(Blob.minX, x)
        Blob.minY = min(Blob.minY, y)
        Blob.maxX = max(Blob.maxX, x)
        Blob.maxY = max(Blob.maxY, y)
        # print(f"New point added to a blob. minX: {self.minX}, minY: {self.minY}, maxX: {self.maxX}, maxY: {self.maxY}")

    def blob_size(self):
        return (Blob.maxX-Blob.minX)*(Blob.maxY-Blob.minY)

    def get_blob_coords(self):
        return Blob.minX, Blob.minY, Blob.maxX, Blob.maxY

    def is_near(self, y, x, maxDistance):
        d = 1000000
        for i in range(0, len(Blob.points)):
            tempDist = np.sum(np.square(np.subtract((x, y), (Blob.points[i]))))
            print(tempDist)
            if tempDist < d:
                d = tempDist

        if d < (maxDistance * maxDistance):
            return True
            print("'is_near' returned True")
        else:
            return False
            print("'is_near' returned False")




# def Show():
    # stroke(0)
    # fill(255)
    # strokeWeight(2)
    # rectMode(CORNERS)
    # rect(minX, minY, maxX, maxY)








# Blob.new_blob(Blob, 5, 8)
# Blob.add_point(Blob, 5, 6)
# Blob.is_near(Blob, 5, 6)
