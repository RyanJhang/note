import cv2
import os
import numpy as np


def calcAndDrawHist(image, color):
    hist = cv2.calcHist([image], [0], None, [256], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256, 256, 3], np.uint8)
    hpt = int(0.9 * 256)

    for h in range(256):
        intensity = int(hist[h]*hpt/maxVal)
        cv2.line(histImg, (h, 256), (h, 256-intensity), color)
    return histImg


def show_rgb_hist(image):
    b, g, r = cv2.split(image)

    histImgB = calcAndDrawHist(b, [255, 0, 0])
    histImgG = calcAndDrawHist(g, [0, 255, 0])
    histImgR = calcAndDrawHist(r, [0, 0, 255])

    cv2.imshow("histImgB", histImgB)
    cv2.imshow("histImgG", histImgG)
    cv2.imshow("histImgR", histImgR)
    cv2.imshow("Img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':

    folder_path = os.path.dirname(os.path.abspath(__file__))
    # img_path = os.path.join(folder_path, "30.0.jpg")
    img_path = os.path.join(folder_path, "..", r"toolbar\2.5_.jpg")
    img = cv2.imread(img_path)
    show_rgb_hist(img)
