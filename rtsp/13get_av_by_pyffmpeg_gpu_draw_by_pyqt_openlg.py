

# ----------------------------------------------------------------------------------
# timeit_wrapper

import logging
import os
import subprocess
import sys
import time
from functools import wraps

import cv2
import ffmpeg
import numpy as np
import pyaudio
from OpenGL import GL as gl
from PySide2 import QtCore, QtGui
from PySide2.QtCore import *
from PySide2.QtCore import QFile, QTimer
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget


def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        print('{0:<10}.{1:<30} : {2:.8f}'.format(func.__module__, func.__name__, end - start))
        return func_return_val
    return wrapper


# ----------------------------------------------------------------------------------
# UI


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(947, 581)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(-1, -1, 6, -1)
        self.openGLWidget = QOpenGLWidget(self.centralWidget)
        self.openGLWidget.setObjectName(u"openGLWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openGLWidget.sizePolicy().hasHeightForWidth())
        self.openGLWidget.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.openGLWidget, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.textEdit = QTextEdit(self.centralWidget)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy1)
        self.textEdit.setMaximumSize(QSize(993, 25))
        self.textEdit.setAcceptDrops(True)
        self.textEdit.setInputMethodHints(Qt.ImhNone)
        self.textEdit.setLineWidth(0)
        self.textEdit.setMidLineWidth(0)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setCursorWidth(1)

        self.horizontalLayout.addWidget(self.textEdit)

        self.pushButton = QPushButton(self.centralWidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalLayout.setStretch(0, 10)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 100)
        self.gridLayout.setRowStretch(3, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 947, 21))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName(u"mainToolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.pushButton_click)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                         "p, li { white-space: pre-wrap; }\n"
                                                         "</style></head><body style=\" font-family:'PMingLiU'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">rtsp://root:@172.19.1.122:554/live1s1.sdp</span></p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
    # retranslateUi


# ----------------------------------------------------------------------------------
# Decoder


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FrameInfo:
    width = None
    height = None
    yuv_height = None
    frame_bytes = None


class StreamingInfo:
    def __init__(self, rtsp_url, mode="auto", stream_info=None):
        self.rtsp_url = rtsp_url
        self.stream_info = self._get_streaming_info(mode, stream_info)

        self.video_process = None
        self.audio_process = None

    def _get_streaming_info(self, mode, streaming_info):
        if mode == "auto":
            streaming_info = self.get_info_by_ffprobe()
        else:
            if streaming_info is None:
                raise Exception("The stream_info could not be None.")
        return streaming_info

    @timeit_wrapper
    def get_info_by_ffprobe(self):
        """
        獲取視訊基本資訊，大約會花 1.1 - 1.3秒
        """
        try:
            probe = ffmpeg.probe(self.rtsp_url)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                print('No video stream found', file=sys.stderr)
                sys.exit(1)
            return video_stream
        except ffmpeg.Error as err:
            print(str(err.stderr, encoding='utf8'))
            sys.exit(1)


class YUVDecoder(StreamingInfo):
    def __init__(self, rtsp_url, mode="auto", stream_info=None):
        StreamingInfo.__init__(self, rtsp_url, mode, stream_info)
        self.video_process = None

    def init_yuv_decoder(self):
        """
        https://ffmpeg.org/ffmpeg.html
        -vsync parameter
            Video sync method. For compatibility reasons old values can be specified as numbers. Newly added values will have to be specified as strings always.

            0, passthrough
            Each frame is passed with its timestamp from the demuxer to the muxer.

            1, cfr
            Frames will be duplicated and dropped to achieve exactly the requested constant frame rate.

            2, vfr
            Frames are passed through with their timestamp or dropped so as to prevent 2 frames from having the same timestamp.

            drop
            As passthrough but destroys all timestamps, making the muxer generate fresh timestamps based on frame-rate.

            -1, auto
            Chooses between 1 and 2 depending on muxer capabilities. This is the default method.

            Note that the timestamps may be further modified by the muxer, after this. For example, in the case that the format option avoid_negative_ts is enabled.

            With -map you can select from which stream the timestamps should be taken. You can leave either video or audio unchanged and sync the remaining stream(s) to the unchanged one.
        """
        logger.info('init_yuv_decoder ffmpeg process')
        args = (
            ffmpeg
            .input(self.rtsp_url,
                   hwaccel="dxva2",
                   rtsp_transport="tcp",
                   vsync="1",
                   preset="slow",
                   flags="low_delay",
                   max_delay="500000")
            .output('pipe:',
                    format='rawvideo',
                    pix_fmt='yuv420p',
                    preset="slow")
            .compile()
        )
        self.video_process = subprocess.Popen(args, stdout=subprocess.PIPE)

        self.frame_info = FrameInfo()
        self.frame_info.width = self.stream_info['width']
        self.frame_info.height = self.stream_info['height']
        self.frame_info.yuv_height = self.stream_info['height'] * 6 // 4
        self.frame_info.frame_bytes = int(self.frame_info.width * self.frame_info.yuv_height)

    def get_a_yuv_frame(self):
        raw_frame = self.video_process.stdout.read(self.frame_info.frame_bytes)  # read bytes of single frames

        if raw_frame == b'':
            # Break the loop in case of an error (too few bytes were read).
            raise Exception("Error reading frame!!!")

        yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.frame_info.yuv_height, self.frame_info.width))

        self.video_process.stdout.flush()
        return yuv

    def release_decoder(self):
        if self.video_process:
            self.video_process.kill()


class RGBDecoder(StreamingInfo):
    def __init__(self, rtsp_url, mode="auto", stream_info=None):
        StreamingInfo.__init__(self, rtsp_url, mode, stream_info)
        self.video_process = None

    def init_rgb24_decoder(self):
        logger.info('init_rgb24_decoder ffmpeg process')
        args = (
            ffmpeg
            .input(self.rtsp_url,
                   hwaccel="dxva2",
                   rtsp_transport="tcp",
                   vsync="1",
                   preset="slow",
                   flags="low_delay",
                   max_delay="500000")
            .output('pipe:',
                    format='rawvideo',
                    pix_fmt='bgr24',
                    preset="slow")
            .compile()
        )
        self.video_process = subprocess.Popen(args, stdout=subprocess.PIPE)

        self.frame_info = FrameInfo()
        self.frame_info.width = self.stream_info['width']
        self.frame_info.height = self.stream_info['height']
        self.frame_info.frame_bytes = self.frame_info.width * self.frame_info.height * 3

    def get_a_rgb24_frame(self):
        raw_frame = self.video_process.stdout.read(self.frame_info.frame_bytes)  # read bytes of single frames

        if raw_frame == b'':
            # Break the loop in case of an error (too few bytes were read).
            raise Exception("Error reading frame!!!")

        yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.frame_info.height, self.frame_info.width, 3))

        self.video_process.stdout.flush()
        return yuv

    def release_decoder(self):
        if self.video_process:
            self.video_process.kill()


class AudioDecoder:
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.audio_process = None

    def init_audio_decoder(self):
        try:
            args = (ffmpeg
                    .input(self.rtsp_url,
                           rtsp_transport="tcp",
                           vsync="1",
                           preset="slow",
                           flags="low_delay",)['a']
                    .filter('volume', 1)
                    .output('pipe:',
                            format='s16le',
                            acodec='pcm_s16le',
                            ac=1,
                            ar="16k")
                    .overwrite_output()
                    .compile()
                    )
        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)
            sys.exit(1)
        self.audio_process = subprocess.Popen(args, stdout=subprocess.PIPE)

    def get_pyaudio_player(self):
        def callback(in_data, frame_count, time_info, status):
            if self.audio_process.poll() is None:
                data = self.audio_process.stdout.read(2 * frame_count)
                return (data, pyaudio.paContinue)

        audio = pyaudio.PyAudio()
        pyaudio_player = audio.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=16000,
                                    output=True,
                                    stream_callback=callback)
        return pyaudio_player


# ----------------------------------------------------------------------------------
# QT


# from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # link openGL event

        self.curr_yuv_frame = None
        self.ui.openGLWidget.initializeGL = self.initializeGL
        self.ui.openGLWidget.resizeGL = self.resizeGL
        self.ui.openGLWidget.paintGL = self.paintGL

        self.timer_opengl = QTimer(self)
        self.timer_opengl.timeout.connect(self.opengl_update)

        self.timer_frame = QTimer(self)
        self.timer_frame.timeout.connect(self.frame_update)

    def frame_update(self):
        self.curr_yuv_frame = self.player.get_a_yuv_frame()

    def opengl_update(self):
        self.ui.pushButton.setText(str(time.time()))
        self.ui.openGLWidget.update()

    def pushButton_click(self):
        rtsp_url = self.ui.textEdit.toPlainText()
        self.player = YUVDecoder(rtsp_url)
        self.player.init_yuv_decoder()

        a_decoder = AudioDecoder(rtsp_url)
        a_decoder.init_audio_decoder()
        a_player = a_decoder.get_pyaudio_player()
        a_player.start_stream()

        time.sleep(5)
        self.timer_opengl.start(10)
        self.timer_frame.start(1)

    def initializeGL(self):
        gl.glClearColor(0.5, 0.8, 0.7, 1.0)

        # Enable texture map
        gl.glEnable(gl.GL_TEXTURE_2D)

    def resizeGL(self, w, h):
        print(w, h)
        gl.glViewport(0, 0, w, h)
        gl.glLoadIdentity()

        if isinstance(self.ui.openGLWidget.width, int):
            widowWidth = self.ui.openGLWidget.width
            windowHeight = self.ui.openGLWidget.height
            # Make the display area proportional to the size of the view
            gl.glOrtho(int(-w / widowWidth), int(w / widowWidth), int(-h / windowHeight), int(h / windowHeight), -1.0, 1.0)

    def paintGL(self):
        if self.curr_yuv_frame is None:
            return

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
