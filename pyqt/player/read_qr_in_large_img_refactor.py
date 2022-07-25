
import pyaudio
import ffmpeg
import sys
import subprocess
import logging
import argparse
import math
import os

import cv2
import numpy as np
from pyzbar import pyzbar
from dataclasses import dataclass

import time
from functools import wraps
DEBUG = False
import sys
import traceback
import math
import os

import cv2
import numpy as np
from pyzbar import pyzbar
from dataclasses import dataclass

import time
from functools import wraps
import qrcode

def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        print('{0:<10}.{1:<30} : {2:.8f}'.format(func.__module__, func.__name__, end - start))
        return func_return_val
    return wrapper

def get_traceback():
    result = 'Traceback (most recent call last):\n'
    tb = sys.exc_info()[-1]
    stk = traceback.extract_tb(tb, 100)
    for s in stk:
        temp = ''
        for index, t in enumerate(s):
            if index == 0:
                temp = '{0} File:"{1}", '.format(temp, str(t))
            elif index == 1:
                temp = '{0} line:{1}, '.format(temp, str(t))
            elif index == 2:
                temp = '{0} in {1}\n'.format(temp, str(t))
            elif index == 3:
                temp = '{0}     {1}\n'.format(temp, str(t))
        result = result + temp
    return result

@dataclass
class ImgsData:
    source: object = None
    gray: object = None
    binary: object = None
    binary_th: object = None
    target: object = None


# @timeit_wrapper
def detect_roi(imgs: ImgsData, area_lower, area_upper, extent_th=0.4, do_erode_dilat=False):
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
            # print(f"extent:{extent}, area:{area}")
            bboxes.append((index, xmin, ymin, xmin + width, ymin + height))

            cv2.rectangle(target, (xmin, ymin), (xmin + width, ymin + height), (0, 255, 255), 2)
            cv2.imshow("target1", target)
    # cv2.waitKey(0)

    return bboxes


# @timeit_wrapper
def smart_decode(imgs: ImgsData, bboxes):
    gray = imgs.gray
    target = imgs.target

    qrs = []
    info = set()
    for index, box in enumerate(bboxes):
        try:
            img_num, xmin, ymin, xmax, ymax = box
            gap = 5
            roi_gray = gray[ymin - gap:ymax + gap, xmin - gap:xmax + gap]
            th = imgs.binary_th
            th, roi = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            detections = pyzbar.decode(roi)
            if len(detections) == 0:
                # print("try")
                # cv2.imshow(f"roi{index}", roi)
                # cv2.waitKey(1)

                th_start = int(th)
                th_range = 50
                for degree in range(th_start, th_start + th_range, 10):
                    print(f"try{degree}")
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
                # qr = (xmin + x, ymin + y, xmin + x + w, ymin + y + h)
                # qrs.append(qr)

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
        except Exception as err:
            print(err)
            # print(get_traceback())
    cv2.imshow("target", target)
    cv2.waitKey(1)


# @timeit_wrapper
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
def main_by_scale(image):

    # folder_path = os.path.dirname(os.path.abspath(__file__))
    # img_path = os.path.join(folder_path, "8.jpg")
    # image = cv2.imread(img_path)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = image
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
    # gray_scale = cv2.cvtColor(image_scale, cv2.COLOR_BGR2GRAY)
    gray_scale = image_scale
    th_scale, thresh_scale = cv2.threshold(gray_scale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    imgs_scale = ImgsData()
    imgs_scale.source = image_scale
    imgs_scale.gray = gray_scale
    imgs_scale.binary = thresh_scale
    imgs_scale.binary_th = th_scale
    imgs_scale.target = image_scale.copy()

    # 偵測用小張
    # bboxes = detect_roi(imgs_scale, area_lower=3000, area_upper=5500, do_erode_dilat=True)
    bboxes = detect_roi(imgs_scale, area_lower=1000, area_upper=3000, do_erode_dilat=True)

    scale_r = 4
    n_bboxes = []
    for index, box in enumerate(bboxes):
        img_num, xmin, ymin, xmax, ymax = box
        n_bboxes.append((img_num, xmin * scale_r, ymin * scale_r, xmax * scale_r, ymax * scale_r))

    # 解碼用大張
    smart_decode(imgs, n_bboxes)
    return imgs.target


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def read_frame_as_jpeg(in_file, frame_num):
    """
    指定幀數讀取任意幀
    """
    out, err = (
        ffmpeg
        .input(in_file)
        .filter('select', 'gte(n,{})'.format(frame_num))
        .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
        .run(capture_stdout=True)
    )
    return out


def get_video_info(in_file):
    """
    獲取視訊基本資訊
    """
    try:
        probe = ffmpeg.probe(in_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print('No video stream found', file=sys.stderr)
            sys.exit(1)
        return video_stream
    except ffmpeg.Error as err:
        print(str(err.stderr, encoding='utf8'))
        sys.exit(1)


def ffmpeg_video_process(in_filename):
    logger.info('Starting ffmpeg process1')
    args = (
        ffmpeg
        .input(in_filename,
               hwaccel="dxva2",
               rtsp_transport="tcp",
               vsync="1",
               preset="slow",
               max_delay="500000")
        .output('pipe:',
                format='rawvideo',
                pix_fmt='yuv420p',
                preset="slow")
        .compile()
    )
    return subprocess.Popen(args, stdout=subprocess.PIPE)


def read_frame(video_process, width, height):
    """
    RGB24 size ＝ width * heigth * 3 Bit
    RGB32 size ＝ width * heigth * 4 Bit
    yuv420 size ＝ width * heigth * 1.5 Bit (yuv yuv yuv)
    yuv420p size ＝ width * heigth * 6 // 14 Bit (yyyyyyyy uuuuuuuu vvvvv)
    """
    logger.debug('Reading frame')

    yuv_height = height * 6 // 4
    frame_size = int(width * yuv_height)

    # read bytes of single frames
    in_bytes = video_process.stdout.read(frame_size)
    if len(in_bytes) == 0:
        yuv_frame = None
    else:
        assert len(in_bytes) == frame_size
        yuv_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([yuv_height, width])
        )

    return yuv_frame


def ffmpeg_audio_process(in_filename):
    try:
        args = (ffmpeg
                .input(in_filename, vsync="1")['a']
                .filter('volume', 1)
                .output('pipe:', format='s16le', acodec='pcm_s16le', ac=1, ar="16k")
                .overwrite_output()
                .compile()
                )
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    return subprocess.Popen(args, stdout=subprocess.PIPE)


def pyaudio_process(audio_process):
    # instantiate PyAudio (1)
    audio = pyaudio.PyAudio()

    # define callback (2)
    def callback(in_data, frame_count, time_info, status):
        if audio_process.poll() is None:
            data = audio_process.stdout.read(2 * frame_count)
            return (data, pyaudio.paContinue)
        # data = audio_process.stdout.read(2 * frame_count)
        # data = numpy.frombuffer(data, dtype="int32")
        # data = data.reshape((len(data)//2, 2))
        # # # data = pipe.readbuffer(frame_count)
        # return (data, pyaudio.paContinue)

    # open stream using callback (3)
    # pyaudio_player = audio.open(format=pyaudio.paInt32,
    #                             channels=2,
    #                             rate=44100,
    #                             output=True,
    #                             stream_callback=callback)
    pyaudio_player = audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=16000,
                                output=True,
                                stream_callback=callback)
    return pyaudio_player

# if __name__ == '__main__':
#     folder_path = os.path.dirname(os.path.abspath(__file__))
#     img_path = os.path.join(folder_path, "4.jpg")
#     image = cv2.imread(img_path)
#     target = img_process(image)
#     cv2.imshow("target", target)
#     cv2.waitKey(0)


def roi(img, top_b=0.3, bottom_b=0.7, left_b=0.3, right_b=0.7):
    """Region of Interest

    Arguments:
        img {cv2.image} -- It's any img and read by cv2.imread

    Keyword Arguments:
        left_b {float} -- It's left bounding of result img (default: {0.3}) (value:[0:1])
        right_b {float} -- It's right bounding of result img (default: {0.7}) (value:[0:1])
        top_b {float} -- It's top bounding of result img (default: {0.3}) (value:[0:1])
        bottom_b {float} -- It's bottom bounding of result img (default: {0.7}) (value:[0:1])

    Returns:
        roi_img {cv2.image} -- It's a captured img
    """
    top = int(img.shape[0] * top_b)
    bottom = int(img.shape[0] * bottom_b)
    left = int(img.shape[1] * left_b)
    right = int(img.shape[1] * right_b)
    roi_img = img[top:bottom, left:right]
    return roi_img


if __name__ == '__main__':
    file_path = "rtsp://root:@172.19.1.159:554/live1s1.sdp"
    # audio init
    # audio_process = ffmpeg_audio_process(file_path)
    # pyaudio_player = pyaudio_process(audio_process)
    # pyaudio_player.start_stream()

    # video init
    video_info = get_video_info(file_path)
    video_process = ffmpeg_video_process(file_path)

    start_time = time.time()

    count = 1
    while True:
        yuv_frame = read_frame(video_process, video_info['width'], video_info['height'])

        # image_scale = 1
        # yuv_frame = cv2.resize(yuv_frame, (0, 0), fx=image_scale, fy=image_scale)
        # bgr_frame = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2BGR_I420)
        bgr_frame = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2GRAY_I420)
        # bgr_frame = roi(bgr_frame)

        duration_time = time.time() - start_time
        fps = count / duration_time
        if fps < 5 and duration_time > 3:
            count += 1
            # print(int(duration_time % 0.3), duration_time)
            print(f"fps:{fps}, count:{count}, duration_time:{duration_time}")
            try:
                bgr_frame = main_by_scale(bgr_frame)
            except Exception as err:
                print(err)
                # print(get_traceback())
                pass
        cv2.imshow('bgr_frame', bgr_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        video_process.stdout.flush()
    cv2.destroyAllWindows()
