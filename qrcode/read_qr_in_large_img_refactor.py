
import math
import os

import cv2
import numpy as np
from pyzbar import pyzbar
from dataclasses import dataclass

import time
from functools import wraps


def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        print('{0:<10}.{1:<30} : {2:.8f}'.format(func.__module__, func.__name__, end - start))
        return func_return_val
    return wrapper


@dataclass
class ImgsData:
    source: object = None
    gray: object = None
    binary: object = None
    binary_th: object = None
    target: object = None


@timeit_wrapper
def detect_roi(imgs: ImgsData, area_lower, area_upper, extent_th=0.3, do_erode_dilat=False):
    thresh = imgs.binary
    target = imgs.target

    if do_erode_dilat:
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)
        thresh = cv2.erode(thresh, kernel, iterations=2)
        cv2.imshow("dilate", thresh)
        cv2.waitKey(1)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bboxes = []
    for index, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        xmin, ymin, width, height = cv2.boundingRect(cnt)
        extent = abs(1 - (width / height))

        # if (area > 5000) and (area < 15000) and extent < 0.3:
        # new_area = area * scale^2
        if (area > area_lower) and (area < area_upper) and (extent < extent_th):
            print(f"extent:{extent}, area:{area}")
            bboxes.append((index, xmin, ymin, xmin + width, ymin + height))

            cv2.rectangle(target, (xmin, ymin), (xmin + width, ymin + height), (0, 255, 255), 2)
            cv2.imshow("target", target)
    # cv2.waitKey(0)

    return bboxes


@timeit_wrapper
def smart_decode(imgs: ImgsData, bboxes):
    gray = imgs.gray
    target = imgs.target

    qrs = []
    info = set()
    for index, box in enumerate(bboxes):
        img_num, xmin, ymin, xmax, ymax = box
        gap = 10
        roi_gray = gray[ymin - gap:ymax + gap, xmin - gap:xmax + gap]
        th = imgs.binary_th
        th, roi = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        detections = pyzbar.decode(roi)
        if len(detections) == 0:
            print("try")
            cv2.imshow(f"roi{index}", roi)
            cv2.waitKey(1)

            th_start = int(th)
            th_range = 50
            for degree in range(th_start - th_range, th_start + th_range, 5):
                th = degree
                _, roi = cv2.threshold(roi_gray, degree, 255, cv2.THRESH_BINARY)
                detections = pyzbar.decode(roi)
                if len(detections) == 0:
                    # cv2.imshow(f"roi_n{img_num}_th{degree}", roi)
                    # cv2.waitKey(1)
                    pass
                else:
                    break

        for barcode in detections:
            info.add(barcode.data)
            # bounding box coordinates
            x, y, w, h = barcode.rect
            qr = (xmin + x, ymin + y, xmin + x + w, ymin + y + h)
            qrs.append(qr)

            (x, y, w, h) = (xmin + x, ymin + y, w, h)
            cv2.rectangle(target, (x, y), (x + w, y + h), (0, 0, 255), -1)

            # 條形碼數據為字節對象，所以如果我們想在輸出圖像上
            # 畫出來，就需要先將它轉換成字符串
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # 繪出圖像上條形碼的數據和條形碼類型
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(target, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 125), 2)
            cv2.putText(target, f"n[{img_num}], th[{th}]", (x, y + 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (125, 0, 0), 2)

            # 向終端打印條形碼數據和條形碼類型
            # print(f"[INFO] num[{img_num}] th[{th}] Found[{barcodeType}] barcode[{barcodeData}]")

        cv2.imshow("target", target)
        # cv2.waitKey(1)


@timeit_wrapper
def main():

    folder_path = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(folder_path, "7.jpg")
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cv2.imshow("thresh", thresh)
    # cv2.waitKey(1)

    scale = 0.5
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    image = cv2.resize(image, (width, height))

    imgs = ImgsData
    imgs.source = image
    imgs.gray = gray
    imgs.binary = thresh
    imgs.binary_th = th
    imgs.target = image.copy()

    bboxes = detect_roi(imgs, area_lower=5000, area_upper=15000, do_erode_dilat=True)
    smart_decode(imgs, bboxes)


@timeit_wrapper
def main_by_scale():

    folder_path = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(folder_path, "8.jpg")
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    imgs = ImgsData()
    imgs.source = image
    imgs.gray = gray
    imgs.binary = thresh
    imgs.binary_th = th
    imgs.target = image.copy()

    scale = 0.25
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    image_scale = cv2.resize(image.copy(), (width, height))
    gray_scale = cv2.cvtColor(image_scale, cv2.COLOR_BGR2GRAY)
    th_scale, thresh_scale = cv2.threshold(gray_scale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    imgs_scale = ImgsData()
    imgs_scale.source = image_scale
    imgs_scale.gray = gray_scale
    imgs_scale.binary = thresh_scale
    imgs_scale.binary_th = th_scale
    imgs_scale.target = image_scale.copy()

    # 偵測用小張
    bboxes = detect_roi(imgs_scale, area_lower=500, area_upper=1500, do_erode_dilat=True)

    scale_r = 4
    n_bboxes = []
    for index, box in enumerate(bboxes):
        img_num, xmin, ymin, xmax, ymax = box
        n_bboxes.append((img_num, xmin * scale_r, ymin * scale_r, xmax * scale_r, ymax * scale_r))

    # 解碼用大張
    smart_decode(imgs, n_bboxes)


if __name__ == '__main__':
    # main()
    main_by_scale()
    cv2.waitKey(0)
