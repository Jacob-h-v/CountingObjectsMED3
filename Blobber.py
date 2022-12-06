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
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0
        self.points = []
        self.maxDistance = 5
        return

    def new_blob(self, y, x, distanceThreshold):
        self.minX = x
        self.minY = y
        self.maxX = x
        self.maxY = y
        self.points.append((y, x))
        self.maxDistance = distanceThreshold
        print(f"New blob added. minX: {self.minX}, minY: {self.minY}, maxX: {self.maxX}, maxY: {self.maxY}")
        return

    def add_point(self, y, x):
        self.points.append((y, x))
        self.minX = min(self.minX, x)
        self.minY = min(self.minY, y)
        self.maxX = max(self.maxX, x)
        self.maxY = max(self.maxY, y)
        print(f"New point added to a blob. minX: {self.minX}, minY: {self.minY}, maxX: {self.maxX}, maxY: {self.maxY}")
        return

    def blob_size(self):
        return (self.maxX-self.minX)*(self.maxY-self.minY)

    def get_blob_coords(self):
        return self.minX, self.minY, self.maxX, self.maxY

    def is_near(self, y, x, maxDistance):
        d = 1000000
        for i in range(0, len(self.points)):
            tempDist = np.sum(np.square(np.subtract((x, y), (self.points[i]))))
            print(tempDist)
            if tempDist < d:
                d = tempDist
        return

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
