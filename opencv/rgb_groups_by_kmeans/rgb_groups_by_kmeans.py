
import cv2
import numpy as np
import os

folder_path = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(folder_path, "k-mean-example.jpg")

img = cv2.imread(img_path, 1)

cv2.imshow('img', img)

Z = img.reshape((-1, 3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

for K in range(1, 5):
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    img_k_result = res.reshape((img.shape))

    cv2.imshow(f'img_k[{K}]_result', img_k_result)
    cv2.imwrite(os.path.join(folder_path, f'img_k[{K}]_result.jpg'), img_k_result)

cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
