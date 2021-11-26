# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 478)
        self.actionFullscreen = QAction(MainWindow)
        self.actionFullscreen.setObjectName(u"actionFullscreen")
        self.actionFullscreen.setCheckable(True)
        self.actionFullscreen.setChecked(False)
        self.actionPlay = QAction(MainWindow)
        self.actionPlay.setObjectName(u"actionPlay")
        self.actionStop = QAction(MainWindow)
        self.actionStop.setObjectName(u"actionStop")
        self.actionPause = QAction(MainWindow)
        self.actionPause.setObjectName(u"actionPause")
        self.actionSnapshot = QAction(MainWindow)
        self.actionSnapshot.setObjectName(u"actionSnapshot")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.dockPlayer = QDockWidget(self.centralwidget)
        self.dockPlayer.setObjectName(u"dockPlayer")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockPlayer.sizePolicy().hasHeightForWidth())
        self.dockPlayer.setSizePolicy(sizePolicy)
        self.widgetContentsPlayer = QWidget()
        self.widgetContentsPlayer.setObjectName(u"widgetContentsPlayer")
        self.gridLayout_5 = QGridLayout(self.widgetContentsPlayer)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(9, 9, 9, 9)
        self.layoutPlayer = QVBoxLayout()
        self.layoutPlayer.setObjectName(u"layoutPlayer")

        self.gridLayout_5.addLayout(self.layoutPlayer, 0, 1, 1, 1)

        self.dockPlayer.setWidget(self.widgetContentsPlayer)

        self.gridLayout.addWidget(self.dockPlayer, 0, 0, 2, 1)

        self.dockCalculator = QDockWidget(self.centralwidget)
        self.dockCalculator.setObjectName(u"dockCalculator")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dockCalculator.sizePolicy().hasHeightForWidth())
        self.dockCalculator.setSizePolicy(sizePolicy1)
        self.widgetContentsController = QWidget()
        self.widgetContentsController.setObjectName(u"widgetContentsController")
        sizePolicy1.setHeightForWidth(self.widgetContentsController.sizePolicy().hasHeightForWidth())
        self.widgetContentsController.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.widgetContentsController)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.layoutCalculator = QGridLayout()
        self.layoutCalculator.setObjectName(u"layoutCalculator")
        self.label = QLabel(self.widgetContentsController)
        self.label.setObjectName(u"label")

        self.layoutCalculator.addWidget(self.label, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.layoutCalculator)

        self.dockCalculator.setWidget(self.widgetContentsController)

        self.gridLayout.addWidget(self.dockCalculator, 0, 1, 2, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuPlayer = QMenu(self.menubar)
        self.menuPlayer.setObjectName(u"menuPlayer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPlayer.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuView.addAction(self.actionFullscreen)
        self.menuPlayer.addAction(self.actionPlay)
        self.menuPlayer.addAction(self.actionStop)
        self.menuPlayer.addAction(self.actionPause)
        self.menuPlayer.addAction(self.actionSnapshot)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionFullscreen.setText(QCoreApplication.translate("MainWindow", u"Fullscreen", None))
#if QT_CONFIG(shortcut)
        self.actionFullscreen.setShortcut(QCoreApplication.translate("MainWindow", u"F11", None))
#endif // QT_CONFIG(shortcut)
        self.actionPlay.setText(QCoreApplication.translate("MainWindow", u"Play", None))
#if QT_CONFIG(shortcut)
        self.actionPlay.setShortcut(QCoreApplication.translate("MainWindow", u"P", None))
#endif // QT_CONFIG(shortcut)
        self.actionStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
#if QT_CONFIG(shortcut)
        self.actionStop.setShortcut(QCoreApplication.translate("MainWindow", u"S", None))
#endif // QT_CONFIG(shortcut)
        self.actionPause.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
#if QT_CONFIG(shortcut)
        self.actionPause.setShortcut(QCoreApplication.translate("MainWindow", u"Space", None))
#endif // QT_CONFIG(shortcut)
        self.actionSnapshot.setText(QCoreApplication.translate("MainWindow", u"Snapshot", None))
        self.dockPlayer.setWindowTitle(QCoreApplication.translate("MainWindow", u"Player", None))
        self.dockCalculator.setWindowTitle(QCoreApplication.translate("MainWindow", u"Controller", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuPlayer.setTitle(QCoreApplication.translate("MainWindow", u"Player", None))
    # retranslateUi

