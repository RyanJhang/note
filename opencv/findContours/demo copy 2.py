
import os
import random as rng
from ast import Global
from re import X

import cv2 as cv
import numpy as np

rng.seed(12345)


def nothing(x):
    print("img_hold, th_area:{}, th_shift:{}".format(th_area, th_shift))
    print("IRLEDQuantity, AreaThreshold:{}, ShiftThreshold:{}".format(th_area, th_shift))


if __name__ == "__main__":
    filename = r"[IBL416V00968][0002D1B0C858]source.jpg"
    image_path = os.path.join(os.path.dirname(__file__), filename)

    img_size = cv.imread(cv.samples.findFile(image_path))

    img_gray = cv.cvtColor(img_size, cv.COLOR_BGR2GRAY)
    img_blur = cv.medianBlur(img_gray, 5)

    source_window = 'Source'
    cv.namedWindow(source_window)
    
    img_scale = 0.2
    img_size2 = cv.resize(img_size, (0, 0), fx=img_scale, fy=img_scale)
    cv.imshow(source_window, img_size2)

    max_area = 250
    max_shift = 100
    
    global th_area
    global th_shift

    th_area = 50  # initial threshold
    th_shift = 50

    cv.createTrackbar('th_area', source_window, th_area, max_area, nothing)
    cv.createTrackbar('th_shift', source_window, th_shift, max_shift, nothing)
    nothing(1)

    while(1):

        th_area = cv.getTrackbarPos('th_area', source_window)
        th_shift = cv.getTrackbarPos('th_shift', source_window)

        th_area = th_area + 1 if th_area % 2 == 0 else th_area
        th_shift = th_shift - 50
        

        img_hold = cv.adaptiveThreshold(img_blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, th_area, th_shift)
        
        img_scale = 0.25
        img_hold = cv.resize(img_hold, (0, 0), fx=img_scale, fy=img_scale)
        cv.imshow('Contours', img_hold)

        #waitfor the user to press escape and break the while loop
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break

    #destroys all window
    cv.destroyAllWindows()
