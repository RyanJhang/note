import os

import cv2
import numpy as np


def vertical(img):
    img = img > 200
    width, height = img.shape[1], img.shape[0]

    x_pixel_counts = [np.sum(img[:, x]) for x in range(0, width)]

    array = np.zeros([height, width, 3], dtype=np.uint8)
    for x, count in enumerate(x_pixel_counts):
        array[0:count, x] = (255, 255, 255)

    cv2.imshow('vertical', array)


def horizontal(img):
    img = img > 200
    width, height = img.shape[1], img.shape[0]

    y_pixel_counts = [np.sum(img[y, :]) for y in range(0, height)]

    array = np.zeros([height, width, 3], dtype=np.uint8)
    for y, count in enumerate(y_pixel_counts):
        array[y, 0:count] = (255, 255, 255)

    cv2.imshow('horizontal', array)


def kmeans(img):
    cv2.imshow('img', img)

    Z = img.reshape((-1, 3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    K = 7
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    img_k_result = res.reshape((img.shape))

    cv2.imshow(f'img_k[{K}]_result', img_k_result)

    # cv2.waitKey(0) & 0xFF
    # cv2.destroyAllWindows()
    return img_k_result


def show_rgb_hist(image):
    def calcAndDrawHist(image, color):
        hist = cv2.calcHist([image], [0], None, [256], [0.0, 255.0])
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
        histImg = np.zeros([256, 256, 3], np.uint8)
        hpt = int(0.9 * 256)

        for h in range(256):
            intensity = int(hist[h] * hpt / maxVal)
            cv2.line(histImg, (h, 256), (h, 256 - intensity), color)
        return histImg
    b, g, r = cv2.split(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    histImgB = calcAndDrawHist(b, [255, 0, 0])
    histImgG = calcAndDrawHist(g, [0, 255, 0])
    histImgR = calcAndDrawHist(r, [0, 0, 255])
    histImgGray = calcAndDrawHist(gray, [127, 127, 127])

    cv2.imshow("histImgB", histImgB)
    cv2.imshow("histImgG", histImgG)
    cv2.imshow("histImgR", histImgR)
    cv2.imshow("histImgGray", histImgGray)
    # cv2.imshow("Img", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def hsv_debug():
    def nothing(x):
        pass

    # # Load in image
    folder_path = os.path.dirname(os.path.abspath(__file__))
    # img_path = os.path.join(folder_path, "30.0.jpg")
    img_path = os.path.join(folder_path, " 4.0.jpg")
    image = cv2.imread(img_path)

    width, height = image.shape[1], image.shape[0]
    scale = 2
    image = cv2.resize(image, (int(width // scale), int(height // scale)), interpolation=cv2.INTER_AREA)

    # Create a window
    cv2.namedWindow('image', cv2.WINDOW_GUI_EXPANDED)

    # Create trackbars for color change
    cv2.createTrackbar('b_min', 'image', 0, 255, nothing)  # Hue is from 0-179 for Opencv
    cv2.createTrackbar('g_min', 'image', 0, 255, nothing)
    cv2.createTrackbar('r_min', 'image', 0, 255, nothing)
    cv2.createTrackbar('b_max', 'image', 0, 255, nothing)
    cv2.createTrackbar('g_max', 'image', 0, 255, nothing)
    cv2.createTrackbar('r_max', 'image', 0, 255, nothing)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('b_max', 'image', 255)
    cv2.setTrackbarPos('g_max', 'image', 255)
    cv2.setTrackbarPos('r_max', 'image', 40)

    # Initialize to check if HSV min/max value changes
    b_min = g_min = r_min = b_max = g_max = r_max = 0
    pb_min = pg_min = pr_min = pb_max = pg_max = pr_max = 0

    output = image
    wait_time = 100

    while(1):

        # Get current positions of all trackbars
        b_min = cv2.getTrackbarPos('b_min', 'image')
        g_min = cv2.getTrackbarPos('g_min', 'image')
        r_min = cv2.getTrackbarPos('r_min', 'image')

        b_max = cv2.getTrackbarPos('b_max', 'image')
        g_max = cv2.getTrackbarPos('g_max', 'image')
        r_max = cv2.getTrackbarPos('r_max', 'image')

        # Set minimum and max HSV values to display
        lower = np.array([b_min, g_min, r_min])
        upper = np.array([b_max, g_max, r_max])

        # Image and threshold into a range.
        mask = cv2.inRange(image, lower, upper)
        cv2.imshow('mask', mask)
        output = cv2.bitwise_and(image, image, mask=mask)

        # analysis
        vertical(mask)
        horizontal(mask)
        show_rgb_hist(output)

        # Print if there is a change in HSV value
        if((pb_min != b_min) | (pg_min != g_min) | (pr_min != r_min) | (pb_max != b_max) | (pg_max != g_max) | (pr_max != r_max)):
            print("(b_min = %d , g_min = %d, r_min = %d), (b_max = %d , g_max = %d, r_max = %d)" % (b_min, g_min, r_min, b_max, g_max, r_max))
            pb_min = b_min
            pg_min = g_min
            pr_min = r_min
            pb_max = b_max
            pg_max = g_max
            pr_max = r_max

        # Display output image
        cv2.imshow('image', output)

        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    hsv_debug()
