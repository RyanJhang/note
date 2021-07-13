import sys

# sys.path.append(r"C:\Anaconda3\Lib\site-packages\cv2")
# sys.path.append(__file__)

import ctypes

try:
    temp=ctypes.windll.LoadLibrary('opencv_videoio_ffmpeg452_64.dll' )
    temp=ctypes.windll.LoadLibrary('opencv_img_hash452.dll' )
    temp=ctypes.windll.LoadLibrary('opencv_world452.dll' )

except:
    pass

import cv2

print(cv2.__file__)

print(cv2.__version__)

def show_in_cuda(url):
    # load .mp4 video
    vod = cv2.VideoCapture(url)

    # read the 1st frame (ret == bool)
    ret, frame = vod.read()

    # as long as frames are read successfully
    while ret:

        # create GPU picture frame
        gpu_frame = cv2.cuda_GpuMat()

        # fit picture to frame
        gpu_frame.upload(frame)

        # resize frame
        frame = cv2.cuda.resize(gpu_frame, (640, 360))

        # download resized frame from GPU to CPU
        frame = frame.download()

        # display output
        cv2.imshow('resized frame', frame)
        cv2.waitKey(1)

        # load next frame
        ret, frame = vod.read()

    vod.release()


if __name__ == '__main__':
    print("example: rtsp://root:12345678z@192.168.1.119:554/live1s1.sdp")
    # show_in_cuda(sys.argv[1])
    show_in_cuda("rtsp://root:12345678z@192.168.1.119:554/live1s1.sdp")
