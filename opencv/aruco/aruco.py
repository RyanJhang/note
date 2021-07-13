import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd



import threading

import cv2

__author__ = "Ryan Jhang"
__version__ = "1.0.0"

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


class GetStreamingByThread:
    def __init__(self, url, api_preference):
        self.frame = None
        self.status = False
        self.isstop = False
        self.__cap, self.width, self.height = self.__init_video_capture(url, api_preference)

    @timeit_wrapper
    def __init_video_capture(self, url, api_preference):

        cap = cv2.VideoCapture(url, apiPreference=api_preference)

        # 設定擷取影像的尺寸大小
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)

        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # fourcc = cv2.VideoWriter_fourcc(*'VGPX')
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        cap.set(cv2.CAP_PROP_FOURCC, fourcc)

        # 取得影像的尺寸大小
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if width != 0 or height != 0:
            print('{url} Cap setting width{width}, height{height}'.format(url=url, width=width, height=height))
            return cap, width, height
        raise Exception(url, api_preference, "Camera can not connect")

    def start(self):
        # 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('cam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        # 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('ipcam stopped!')

    def getframe(self):
        # 當有需要影像時，再回傳最新的影像。
        return self.status, self.frame

    def queryframe(self):
        while (not self.isstop):
            self.status, self.frame = self.__cap.read()

        self.__cap.release()


# VIDEO_URL = "rtsp://root@172.19.1.38:554/live1s1.sdp", cv2.CAP_ANY
VIDEO_URL = 0, cv2.CAP_DSHOW

if __name__ == '__main__':

    # aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    # fig = plt.figure()
    # nx = 4
    # ny = 3
    # for i in range(1, nx*ny+1):
    #     ax = fig.add_subplot(ny, nx, i)
    #     img = aruco.drawMarker(aruco_dict, i, 700)
    #     plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    #     ax.axis("off")

    # plt.savefig("markers.png")
    # plt.show()

    gsbt = GetStreamingByThread(*VIDEO_URL)
    gsbt.start()
    while True:
        status, frame = gsbt.getframe()
        if status is True:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            parameters = aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
            # cv2.circle(frame_markers, (int(corners[0][0][0][0]), int(corners[0][0][0][1])), 3, (255, 255, 0), -1)
            # cv2.circle(frame_markers, (int(corners[0][0][1][0]), int(corners[0][0][1][1])), 3, (255, 255, 0), -1)
            # cv2.circle(frame_markers, (int(corners[0][0][2][0]), int(corners[0][0][2][1])), 3, (255, 255, 0), -1)
            # cv2.circle(frame_markers, (int(corners[0][0][3][0]), int(corners[0][0][3][1])), 3, (255, 255, 0), -1)
            try:
                index_1 = np.where(ids==1)[0][0]
                index_4 = np.where(ids==4)[0][0]


                cv2.line(frame_markers, (int(corners[index_1][0][3][0]), int(corners[index_1][0][3][1])), (int(corners[index_4][0][3][0]), int(corners[index_4][0][3][1])), (0, 0, 255), 1)
            except:
                pass
            cv2.imshow('frame_markers', frame_markers)
            # plt.figure()
            # plt.imshow(frame_markers)
            # for i in range(len(ids)):
            #     c = corners[i][0]
            #     plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label = "id={0}".format(ids[i]))
            # plt.legend()
            # plt.show()
            # image_scale = 0.25
            # frame = cv2.resize(frame, (0, 0), fx=image_scale, fy=image_scale)
            cv2.imshow('Image', frame)
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                gsbt.stop()
                break
