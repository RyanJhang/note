

import os

import cv2
from pyzbar import pyzbar
import math

import numpy as np



# 定义旋转rotate函数
def rotate(image, angle, center=None, scale=1.0):
    # 获取图像尺寸
    (h, w) = image.shape[:2]
 
    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)
 
    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    image = 255 - image
    rotated = cv2.warpAffine(image, M, (w, h))
    rotated = 255 - rotated
 
    # 返回旋转后的图像
    return rotated

# 2021.10.15 將樣本編號 做分析

if __name__ == '__main__':

    folder_path = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(folder_path, "4.jpg")
    # img_path = os.path.join(folder_path, "qr3.jpg")

    image = cv2.imread(img_path)
    scale = 1
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    image = cv2.resize(image, (width, height))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cv2.imshow("thresh", thresh)
    cv2.waitKey(1)

    # The bigger the kernel, the more the white region increases.
    # If the resizing step was ignored, then the kernel will have to be bigger
    # than the one given here.
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    thresh = cv2.dilate(thresh, kernel, iterations=4)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("dilate", thresh)
    cv2.waitKey(1)

    bboxes = []
    for index, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        xmin, ymin, width, height = cv2.boundingRect(cnt)
        extent = area / (width * height)

        # filter non-rectangular objects and small objects
        if (area > 7000) and (area < 15000):
            print(f"extent:{extent}, area:{area}")
            bboxes.append((index, xmin, ymin, xmin + width, ymin + height))

            cv2.rectangle(image, (xmin, ymin), (xmin + width, ymin + height), (0, 255, 255), 5)
            cv2.imshow("image", image)
            cv2.waitKey(1)

    cv2.waitKey(1)
    qrs = []
    info = set()
    for index, box in enumerate(bboxes):
        img_num, xmin, ymin, xmax, ymax = box
        roi_gray = gray[ymin - 10:ymax + 10, xmin - 10:xmax + 10]
        th = 0
        _, roi = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        detections = pyzbar.decode(roi)
        if len(detections) == 0:
            cv2.imshow(f"roi{index}", roi)
            cv2.waitKey(1)

            for degree in range(50, 200, 25):
                th = degree
                _, roi = cv2.threshold(roi_gray, degree, 255, cv2.THRESH_BINARY)
                detections = pyzbar.decode(roi)
                if len(detections) == 0:
                    cv2.imshow(f"roi_{img_num}_{degree}", roi)
                    cv2.waitKey(1)
                else:
                    break

            # retry degree
            # for degree in range(0, 15, 5): 
            #     img_rotate = rotate(roi, degree)
            #     detections = pyzbar.decode(roi)

            #     if len(detections) == 0:
            #         cv2.imshow(f"img_rotate{degree}", img_rotate)
            #         cv2.waitKey(1)

        for barcode in detections:
            info.add(barcode.data)
            # bounding box coordinates
            x, y, w, h = barcode.rect
            qr = (xmin + x, ymin + y, xmin + x + w, ymin + y + h)
            qrs.append(qr)

            (x, y, w, h) = (xmin + x, ymin + y, w, h)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), -1)

            # 條形碼數據為字節對象，所以如果我們想在輸出圖像上
            # 畫出來，就需要先將它轉換成字符串
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # 繪出圖像上條形碼的數據和條形碼類型
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 125), 2)

            # 向終端打印條形碼數據和條形碼類型
            print(f"[INFO] num[{img_num}] th[{th}] Found[{barcodeType}] barcode[{barcodeData}]")

            # cv2.imshow(f"decodeDisplay by {barcodeData} Degrees", image)
            cv2.imshow("image", image)
            cv2.waitKey(1)

    cv2.waitKey(0)
