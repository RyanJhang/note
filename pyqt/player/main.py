
import json
import os
import sys
import time

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QTimer
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QDockWidget, QMainWindow

from libs.loggers.logger_creater import create_json_logger, create_std_logger
from libs.loggers.logger_formatter import LoggerFormatter
from libs.timeit_wrapper import timeit_wrapper
from player_widget import PlayerInfo, PlayerWidget
from calculator_widget import CalculatorWidget
from ui.ui_mainwindow import Ui_MainWindow

# logger
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "log"))
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

std_logger = create_std_logger(folder_path)
json_logger = create_json_logger(folder_path)


class MainWindow(QMainWindow):
    def __init__(self):
        self.logger = LoggerFormatter(json_logger, std_logger)
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_ui()
        self.logger.debug("complete init ui")

    def init_ui(self):
        # Player
        self.player_info = PlayerInfo("rtsp://root:12345678z@172.19.1.137:554/live1s1.sdp", 1920, 1080, need_video=True,
                                      need_audio=True,
                                      need_score=True)
        self.player_info = PlayerInfo("0", 1920, 1080, url_mode='UVC', need_video=True,
                                      need_audio=True,
                                      need_score=True)
        self.player_weiget = PlayerWidget(player_info=self.player_info, logger=self.logger)
        self.ui.layoutPlayer.addWidget(self.player_weiget)

        # Calculator
        self.calculator_widget = CalculatorWidget(self, player_info=self.player_info, logger=self.logger)
        self.ui.layoutCalculator.addWidget(self.calculator_widget)

        for action in self.findChildren(QAction):
            shortcuts = [x.toString() for x in action.shortcuts()]
            print(type(action), action.toolTip(), shortcuts)

            def_name = f"{action.objectName()}_trigger"
            if shortcuts and hasattr(self, def_name):
                action.triggered.connect(getattr(self, def_name))

    def keyPressEvent(self, event=None):
        if event is None or not hasattr(self, "getShortcutByName"):
            return

        key_value = event.key()
        modifiers = int(event.modifiers())
        key = QKeySequence(modifiers + key_value)
        print(event)

        if key.matches(self.getShortcutByName("actionFullscreen")) == QKeySequence.ExactMatch:
            self.actionFullscreen.trigger()
        elif key.matches(self.getShortcutByName("actionPlay")) == QKeySequence.ExactMatch:
            self.actionPlay.trigger()
        elif key.matches(self.getShortcutByName("actionStop")) == QKeySequence.ExactMatch:
            self.actionStop.trigger()
        elif key.matches(self.getShortcutByName("actionPause")) == QKeySequence.ExactMatch:
            self.actionPause.trigger()
        elif key.matches(self.getShortcutByName("actionFullscreen")) == QKeySequence.ExactMatch:
            self.actionFullscreen.trigger()

    def actionFullscreen_trigger(self):
        # Toggle fullscreen state (current state mask XOR WindowFullScreen)
        self.setWindowState(self.windowState() ^ QtCore.Qt.WindowFullScreen)

    def actionPlay_trigger(self):
        self.player_weiget.play()

    def actionStop_trigger(self):
        self.player_weiget.stop()

    def actionPause_trigger(self):
        print(json.dumps(self.player_weiget.v_decoder._get_info_by_ffprobe(), indent=4))
        self.player_weiget

    def getDocks(self):
        """ Get a list of all dockable widgets """
        return self.findChildren(QDockWidget)

    def removeDocks(self):
        """ Remove all dockable widgets on main screen """
        for dock in self.getDocks():
            if self.dockWidgetArea(dock) != QtCore.Qt.NoDockWidgetArea:
                self.removeDockWidget(dock)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    res = app.exec_()
    # window.glWidget.free_resources()
    sys.exit(res)
