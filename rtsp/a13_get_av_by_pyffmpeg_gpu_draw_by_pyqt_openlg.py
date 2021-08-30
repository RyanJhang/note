

# ----------------------------------------------------------------------------------
# timeit_wrapper

from a12_get_av_by_pyffmpeg_gpu_draw_by_opencv import YUVDecoder, AudioDecoder
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
                                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">rtsp://root:12345678z@172.19.1.137:554/live1s1.sdp</span></p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
    # retranslateUi


# ----------------------------------------------------------------------------------
# Decoder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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
        self.timer_opengl.timeout.connect(self.ui.openGLWidget.update)

        self.timer_frame = QTimer(self)
        self.timer_frame.timeout.connect(self.frame_update)
        self.err = 0

    def frame_update(self):
        if self.err > 10:
            self.pushButton_click()

        try:
            self.curr_yuv_frame = self.player.get_a_yuv_frame()
        except Exception:
            self.err += 1

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
