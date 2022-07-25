import queue
import time

import cv2

import numpy as np
import ptvsd
from OpenGL import GL as gl
from PySide2.QtCore import QThread, QTimer, Signal
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PySide2.QtGui import QPixmap

from libs.a12_get_av_by_pyffmpeg_gpu_draw_by_opencv import (AudioDecoder, DSAudioDecoder, DSVideoDecoder,
                                                            YUVDecoder)
from libs.loggers.logger_formatter import LoggerFormatter
from player_widget import PlayerInfo


class ScoreWidget(QWidget):

    def __init__(self, parent, tag):
        super(ScoreWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        self.img_label = QLabel(tag)
        self.layout.addWidget(self.img_label)

        self.score_label = QLabel("score")
        self.layout.addWidget(self.score_label)

        self.setLayout(self.layout)


class CalculatorWidget(QWidget):

    def __init__(self, parent, player_info: PlayerInfo, logger: LoggerFormatter, *args):
        super(CalculatorWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        zones = ['lt', 't', 'rt', 'l', 'c', 'r', 'lb', 'b', 'rb']
        self.score_widgets_dict = {}
        for row in range(3):
            for column in range(3):
                tag = zones[row * 3 + column]
                self.score_widgets_dict[tag] = ScoreWidget(parent, tag)
                self.layout.addWidget(self.score_widgets_dict[tag], row, column)

        self.setLayout(self.layout)
