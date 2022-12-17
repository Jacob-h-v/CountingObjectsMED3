import cv2 as cv
import numpy as np

from NonMaximaSupressionTest import non_max_suppression

def NormalisedCrossCorrelation(roi, target):
    print(f"Initiating NCC on roi: {roi}")
    ncc = np.zeros((roi.shape[0], roi.shape[1], roi.shape[2]), dtype=np.uint8)

    for y in range(roi.shape[0]):
        for x in range(roi.shape[1]):
            for z in range(roi.shape[2]):
                corr = (roi[y, x, z] - np.mean(roi)) * (target[y, x, z] - np.average(target))
                norm = ((roi[y, x, z] - np.mean(roi)) * (roi[y, x, z] - np.mean(roi))) * ((target[y, x, z] - np.average(target)) * (target[y, x, z] - np.average(target)))
                ncc = corr/norm
    # print(ncc)
    print(ncc)
    return ncc


def GetMatches(processed, temp):
    template_y = temp.shape[0]
    template_x = temp.shape[1]
    output = np.zeros((processed.shape[0] - template_y + 1, processed.shape[1] - template_x + 1, processed.shape[2]),
                      dtype=np.uint8)
    matchList = np.zeros((processed.shape[0] - template_y + 1, processed.shape[1] - template_x + 1, processed.shape[2]),
                      dtype=np.uint8)

    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            for z in range(output.shape[2]):
                # getting region of interest (slice)
                slice = processed[y:y + template_y, x:x + template_x, z:z + 1]

                # calculate ncc value (normalized cross correlation value)
                output[y, x, z] = NormalisedCrossCorrelation(slice, temp)
                # find the most match area
                if output[y, x, z] > 0.4:
                    matchList[y, x, z] = output[y, x, z]

    return matchList


def ManualTemplateMatching(original, processed, template, kernelsize):
    image = np.array(original, dtype=np.uint8)
    processed = np.array(processed, dtype=np.uint8)
    template = np.array(template, dtype=np.uint8)

    template_90 = cv.rotate(template, cv.ROTATE_90_CLOCKWISE)
    template_180 = cv.rotate(template_90, cv.ROTATE_90_CLOCKWISE)
    template_270 = cv.rotate(template_180, cv.ROTATE_90_CLOCKWISE)

    rotations = [template, template_90, template_180, template_270]

    rects = []
    for i in range(len(rotations)):
        temp = rotations[i]

        tH, tW = temp.shape[:2]

        # ------------------------------------------------------
        # matchResults = Yaaay time to start writing algorithms (-_-)
        # option: Check for difference for each pixel (using normalized results?), then average for template area
        # (normalized cross correlation)
        matchResults = GetMatches(processed, temp)
        print(matchResults)


        #-------------------------------------------------------
        threshold = 0.90
        (yCoords, xCoords, zCoords) = np.where(matchResults >= threshold)

        for (x, y) in zip(xCoords, yCoords):
            rects.append((x, y, x + tW, y + tH))
    print("Initiating non maxima suppression...")
    pick = non_max_suppression(np.array(rects), 0.1)
    resultAmount = len(pick)
    print(resultAmount)

    # loop over the final bounding boxes
    for (startX, startY, endX, endY) in pick:
        # draw the bounding box on the image
        cv.rectangle(image, (startX + kernelsize, startY + kernelsize // 2), (endX + kernelsize, endY + kernelsize // 2), (0, 0, 255), 3)

    return image, resultAmount