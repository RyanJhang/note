
import os

import cv2
from pyzbar import pyzbar
import math

def decodeDisplay(image):
    barcodes = decode(image)
    return barcodes


def draw_qrcode(image, barcodes, degree):
    def get_retate_xy(x, y):
        x1 = x * math.cos(degree * math.pi / 180) + y * math.sin(degree * math.pi / 180)
        y1 = -x * math.sin(degree * math.pi / 180) + y * math.cos(degree * math.pi / 180)
        return int(x1), int(y1)

    for barcode in barcodes:
        # 提取條形碼的邊界框的位置
        # 畫出圖像中條形碼的邊界框
        (x, y, w, h) = barcode.rect
        p1 = (get_retate_xy(x, y))
        p2 = (get_retate_xy(x + w, y + h))
        cv2.rectangle(image, p1, p2, (0, 0, 255), -1)

        # 條形碼數據為字節對象，所以如果我們想在輸出圖像上
        # 畫出來，就需要先將它轉換成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # 繪出圖像上條形碼的數據和條形碼類型
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, p1, cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (0, 0, 125), 2)

        # 向終端打印條形碼數據和條形碼類型
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))


# 定义旋转rotate函数
def rotate(image, angle, center=None, scale=1.0):
    # 获取图像尺寸
    (h, w) = image.shape[:2]
 
    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)
 
    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
 
    # 返回旋转后的图像
    return rotated


if __name__ == '__main__':

    folder_path = os.path.dirname(os.path.abspath(__file__))
    # img_path = os.path.join(folder_path, "qr1.png")
    img_path = os.path.join(folder_path, "qr2.jpg")
    img = cv2.imread(img_path, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # image_scale = 0.25
    # yuv_frame = cv2.resize(im, (0, 0), fx=image_scale, fy=image_scale)
    # cv2.imshow("camera", yuv_frame)
    # cv2.imshow("gray", cv2.resize(gray, (0, 0), fx=image_scale, fy=image_scale))

    before_degree = 0
    # 原始的計算
    height, width = gray.shape[:2]
    barcodes = pyzbar.decode((gray.tobytes(), width, height))
    # 旋轉
    img_rotate = rotate(gray.copy(), before_degree)
    # 繪圖結果
    draw_qrcode(img_rotate, barcodes, before_degree)

    for degree in range(0, 15, 5):
        # img = gray.copy()

        # 拿旋轉結果計算
        barcodes = pyzbar.decode(img_rotate)
        if len(barcodes) > 0:
            print(f"decodeDisplay by {degree} Degrees")

        img_rotate = rotate(img_rotate.copy(), degree)

        draw_qrcode(img_rotate, barcodes, degree)

        scale = 0.25
        img_show = cv2.resize(img_rotate, (0, 0), fx=scale, fy=scale)
        cv2.imshow(f"decodeDisplay by {degree} Degrees", img_show)
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
