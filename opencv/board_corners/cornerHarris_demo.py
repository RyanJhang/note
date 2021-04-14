from __future__ import print_function

import os

import cv2
import numpy as np

source_window = 'Source image'
corners_window = 'Corners detected'
max_thresh = 255


def cornerHarris_demo(val):
    thresh = val
    # Detector parameters
    blockSize = 2
    apertureSize = 3
    k = 0.04
    # Detecting corners
    dst = cv2.cornerHarris(src_gray, blockSize, apertureSize, k)
    # Normalizing
    dst_norm = np.empty(dst.shape, dtype=np.float32)
    cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    dst_norm_scaled = cv2.convertScaleAbs(dst_norm)
    # Drawing a circle around corners
    for i in range(dst_norm.shape[0]):
        for j in range(dst_norm.shape[1]):
            if int(dst_norm[i, j]) > thresh:
                cv2.circle(dst_norm_scaled, (j, i), 5, (0), 2)
    # Showing the result
    cv2.namedWindow(corners_window)
    cv2.imshow(corners_window, dst_norm_scaled)


# Load source image and convert it to gray

folder_path = os.path.dirname(os.path.abspath(__file__))
# img_path = os.path.join(folder_path, "board.jpg")
# img_path = os.path.join(folder_path, "calib_result.jpg")
img_path = os.path.join(folder_path, "variant_board.jpg")
src = cv2.imread(img_path)

src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
# Create a window and a trackbar
cv2.namedWindow(source_window)
thresh = 200  # initial threshold
cv2.createTrackbar('Threshold: ', source_window, thresh, max_thresh, cornerHarris_demo)
cv2.imshow(source_window, src)
cornerHarris_demo(thresh)
cv2.waitKey()
