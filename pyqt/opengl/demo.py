import os
import sys
import time

import cv2
import pygame
import pygame.image
import PySide2.QtOpenGL
from OpenGL import GL as gl
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *
from PySide2 import QtCore, QtGui
from PySide2.QtCore import QFile, QTimer
from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget

from ui_mainwindow import Ui_MainWindow


# cap = cv2.VideoCapture("rtsp://root:12345678z@172.19.1.137:554/live1s1.sdp")
# if cap.isOpened() is False:
#     raise("IO Error")



import numpy as np
import cv2
import subprocess
import json


class YUVInfo:
    width = None
    height = None
    yuv_height = None
    frame_bytes = None


class GetStreamingByFFmpegDrawByOpencv:
    def __init__(self, rtsp_url, mode="auto", stream_info=None):
        self.rtsp_url = rtsp_url
        self.stream_info = self._get_streaming_info(mode, stream_info)

        self.yuv_info = YUVInfo()
        self.ffmpeg_process = None

    def _get_streaming_info(self, mode, stream_info):
        if mode == "auto":
            stream_info = self.get_info_by_ffprobe()
        else:
            if stream_info is None:
                raise Exception("The stream_info could not be None.")
        return stream_info

    def get_info_by_ffprobe(self):
        probe_command = ['ffprobe.exe',
                         '-loglevel', 'error',
                         '-rtsp_transport', 'tcp',  # Force TCP (for testing)]
                         '-select_streams', 'v:0',  # Select only video stream 0.
                         '-show_entries', 'stream=width,height',  # Select only width and height entries
                         '-of', 'json',  # Get output in JSON format
                         self.rtsp_url]

        # Read video width, height using FFprobe:
        probe_process = subprocess.Popen(probe_command, stdout=subprocess.PIPE)

        # Reading content of p0.stdout (output of FFprobe) as string
        probe_str = probe_process.communicate()[0]  
        probe_process.wait()

        # Convert string from JSON format to dictonary.
        probe_dct = json.loads(probe_str)  

        # Get width and height from the dictonary
        # width = probe_dct['streams'][0]['width']
        # height = probe_dct['streams'][0]['height']
        return probe_dct['streams'][0]

    def init_yuv_decoder(self):
        ffmpeg_command = ["ffmpeg.exe", "-y",
                          "-hwaccel", "dxva2",
                          # "-c:v",  "h264_qsv",
                          "-vsync", "1",
                          "-max_delay", "500000",
                          # "-reorder_queue_size", "10000",
                          "-i", self.rtsp_url,
                          "-f", "rawvideo",
                          "-pix_fmt", "yuv420p",
                          "-preset", "slow",
                          "-an", "-sn",
                          # "-vf", "fps=15",
                          "-"]

        self.ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, bufsize=10)

        self.yuv_info.width = self.stream_info['width']
        self.yuv_info.height = self.stream_info['height']
        self.yuv_info.yuv_height = self.stream_info['height'] * 6 // 4
        self.yuv_info.frame_bytes = int(self.yuv_info.width * self.yuv_info.yuv_height)

    def get_a_yuv_frame(self):

        raw_frame = self.ffmpeg_process.stdout.read(self.yuv_info.frame_bytes)  # read bytes of single frames

        if raw_frame == b'':
            # Break the loop in case of an error (too few bytes were read).
            raise Exception("Error reading frame!!!")

        yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.yuv_info.yuv_height, self.yuv_info.width))

        self.ffmpeg_process.stdout.flush()
        return yuv

    def release_decoder(self):
        if self.ffmpeg_process:
            self.ffmpeg_process.kill()


widowWidth = 720
windowHeight = 480


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.openGLWidget.initializeGL = self.initializeGL
        self.ui.openGLWidget.resizeGL = self.resizeGL
        self.ui.openGLWidget.paintGL = self.paintGL

        rtsp_url = "rtsp://root:@172.19.1.122:554/live1s1.sdp"
        self.player = GetStreamingByFFmpegDrawByOpencv(rtsp_url)
        self.player.init_yuv_decoder()

        timer = QTimer(self)
        timer.timeout.connect(self.advanceGears)
        timer.start(20)

    def advanceGears(self):
        self.ui.pushButton.setText(str(time.time()))
        self.curr_yuv_frame = self.player.get_a_yuv_frame()
        self.ui.openGLWidget.update()

    def pushButton_click(self):
        pass

    def initializeGL(self):
        gl.glClearColor(0.5, 0.8, 0.7, 1.0)

        # Enable texture map
        gl.glEnable(gl.GL_TEXTURE_2D)

    def resizeGL(self, w, h):
        print(w,h)
        gl.glViewport(0, 0, w, h)
        gl.glLoadIdentity()
        # Make the display area proportional to the size of the view
        gl.glOrtho(-w / widowWidth, w / widowWidth, -h / windowHeight, h / windowHeight, -1.0, 1.0)

    def paintGL(self):
        img = cv2.cvtColor(self.curr_yuv_frame, cv2.COLOR_YUV2RGB_I420)  # BGR-->RGB
        h, w = img.shape[:2]
        # Paste into texture to draw at high speed
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, w, h, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # gl.glClearColor(0, 0, 0, 1)

        gl.glColor3f(1.0, 1.0, 1.0)

        # Set texture map method
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        # draw square
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2d(0.0, 1.0)
        gl.glVertex3d(-1.0, -1.0, 0.0)
        gl.glTexCoord2d(1.0, 1.0)
        gl.glVertex3d(1.0, -1.0, 0.0)
        gl.glTexCoord2d(1.0, 0.0)
        gl.glVertex3d(1.0, 1.0, 0.0)
        gl.glTexCoord2d(0.0, 0.0)
        gl.glVertex3d(-1.0, 1.0, 0.0)
        gl.glEnd()
        gl.glFlush()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    res = app.exec_()
    window.glWidget.free_resources()
    sys.exit(res)
