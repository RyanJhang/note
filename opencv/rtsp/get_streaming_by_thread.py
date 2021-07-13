
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

        # cap.set(3, 640) #set width
        # cap.set(4, 480) #set height
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

# a = "rtspsrc location=\"rtsp://root:12345678z@192.168.1.119:554/live1s1.sdp\" ! rtph264depay ! h264parse ! omxh264dec ! nvvidconv ! video/x-raw, format=(string)BGRx! videoconvert ! appsink"
# VIDEO_URL = a, cv2.CAP_ANY
VIDEO_URL = "rtsp://root:12345678z@192.168.1.119:554/live1s1.sdp", cv2.CAP_GSTREAMER
# VIDEO_URL = 0, cv2.CAP_DSHOW

if __name__ == '__main__':
    gsbt = GetStreamingByThread(*VIDEO_URL)
    gsbt.start()
    while True:
        status, frame = gsbt.getframe()
        if status is True:
            image_scale = 0.25
            frame = cv2.resize(frame, (0, 0), fx=image_scale, fy=image_scale)
            cv2.imshow('Image', frame)
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                gsbt.stop()
                break
