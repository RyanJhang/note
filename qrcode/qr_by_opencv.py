import os
import time

import cv2
import numpy as np

folder_path = os.path.dirname(os.path.abspath(__file__))
# img_path = os.path.join(folder_path, "qr.png")
img_path = os.path.join(folder_path, "qr2.jpg")
inputImage = cv2.imread(img_path)
inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

# Display barcode and QR code location


def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(im, tuple(bbox[j][0]), tuple(bbox[(j+1) % n][0]), (255, 0, 0), 3)

    # Display results
    cv2.imshow("Results", im)


# Create a qrCodeDetector Object
qrDecoder = cv2.QRCodeDetector()

# Detect and decode the qrcode
t = time.time()
data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
print("Time Taken for Detect and Decode : {:.3f} seconds".format(time.time() - t))
if len(data) > 0:
    print("Decoded Data : {}".format(data))
    display(inputImage, bbox)
    rectifiedImage = np.uint8(rectifiedImage)
    cv2.imshow("Rectified QRCode", rectifiedImage)
else:
    print("QR Code not detected")
    cv2.imshow("Results", inputImage)
cv2.imwrite("output.jpg", inputImage)
cv2.waitKey(0)
cv2.destroyAllWindows()
