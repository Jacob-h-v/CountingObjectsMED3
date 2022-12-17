import cv2 as cv
import numpy as np

#input_image = cv.imread("Resources/JPEGbilleder/Coins/GreenBackground/1M-2L-1P-1CL-1C-16A (1).JPEG", cv.IMREAD_GRAYSCALE)

def BinaryThreshold(input_image, threshold):
    output_image = np.zeros(input_image.shape, dtype=input_image.dtype)

    for y, row in enumerate(input_image):
        for x, pixel in enumerate(row):
            if pixel > threshold:
                output_image[y, x] = 255

    return output_image

def OtsuThreshold(image_input):
    # find normalized_histogram, and its cumulative distribution function
    hist = cv.calcHist([image_input], [0], None, [256], [0, 256])
    hist_norm = hist.ravel() / hist.sum()
    Q = hist_norm.cumsum()
    bins = np.arange(256)
    fn_min = np.inf
    thresh = -1
    for i in range(1, 256):
        p1, p2 = np.hsplit(hist_norm, [i])  # probabilities
        q1, q2 = Q[i], Q[255] - Q[i]  # cum sum of classes
        if q1 < 1.e-6 or q2 < 1.e-6:
            continue
        b1, b2 = np.hsplit(bins, [i])  # weights

        # finding means and variances
        m1, m2 = np.sum(p1 * b1) / q1, np.sum(p2 * b2) / q2
        v1, v2 = np.sum(((b1 - m1) ** 2) * p1) / q1, np.sum(((b2 - m2) ** 2) * p2) / q2

        # calculates the minimization function
        fn = v1 * q1 + v2 * q2
        if fn < fn_min:
            fn_min = fn
            thresh = i

    return thresh

#result = BinaryThreshold(input_image)
#cv.imshow("result", result)
#cv.waitKey(0)