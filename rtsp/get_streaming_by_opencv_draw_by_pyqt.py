

# -*- coding: utf-8 -*-
"""
Use GLImageItem to display image data on rectangular planes.

In this example, the image data is sampled from a volume and the image planes 
placed as if they slice through the volume.
"""
## Add path to library (just for examples; you do not need this)
# import initExample

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np

app = pg.mkQApp("GLImageItem Example")
w = gl.GLViewWidget()
w.opts['distance'] = 200
w.show()
w.setWindowTitle('pyqtgraph example: GLImageItem')

## create volume data set to slice three images from
shape = (100,100,70)
data = pg.gaussianFilter(np.random.normal(size=shape), (4,4,4))
data += pg.gaussianFilter(np.random.normal(size=shape), (15,15,15))*15

## slice out three planes, convert to RGBA for OpenGL texture
levels = (-0.08, 0.08)
tex1 = pg.makeRGBA(data[shape[0]//2], levels=levels)[0]       # yz plane
tex2 = pg.makeRGBA(data[:,shape[1]//2], levels=levels)[0]     # xz plane
tex3 = pg.makeRGBA(data[:,:,shape[2]//2], levels=levels)[0]   # xy plane
#tex1[:,:,3] = 128
#tex2[:,:,3] = 128
#tex3[:,:,3] = 128

## Create three image items from textures, add to view
v1 = gl.GLImageItem(tex1)
v1.translate(-shape[1]/2, -shape[2]/2, 0)
v1.rotate(90, 0,0,1)
v1.rotate(-90, 0,1,0)
w.addItem(v1)
v2 = gl.GLImageItem(tex2)
v2.translate(-shape[0]/2, -shape[2]/2, 0)
v2.rotate(-90, 1,0,0)
w.addItem(v2)
v3 = gl.GLImageItem(tex3)
v3.translate(-shape[0]/2, -shape[1]/2, 0)
w.addItem(v3)

ax = gl.GLAxisItem()
w.addItem(ax)

if __name__ == '__main__':
    pg.exec()

# import pyqtgraph.examples
# pyqtgraph.examples.run()
# from pyqtgraph.Qt import QtCore, QtGui
# import pyqtgraph.opengl as gl
# import pyqtgraph as pg
# import numpy as np


# -----------------------------------
# import sys  # for exiting

# # import cv2  # OpenCV
# # import qimage2ndarray  # for a memory leak,see gist
# # from PySide2.QtCore import QTimer
# # from PySide2.QtGui import QPixmap
# # from PySide2.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
# #                                QPushButton, QVBoxLayout, QWidget)


# # def displayFrame():
# #     ret, frame = cap.read()
# #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #     image = qimage2ndarray.array2qimage(frame)
# #     label.setPixmap(QPixmap.fromImage(image))

# # app = QApplication(sys.argv)
# # window = QWidget()

# # # OPENCV

# # cap = cv2.VideoCapture("rtsp://root:@172.19.1.17:554/live1s1.sdp")
# # # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# # # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# # # timer for getting frames

# # timer = QTimer()
# # timer.timeout.connect(displayFrame)
# # timer.start(60)
# # label = QLabel('No Camera Feed')
# # button = QPushButton("Quiter")
# # button.clicked.connect(sys.exit) # quiter button 
# # layout = QVBoxLayout()
# # layout.addWidget(button)
# # layout.addWidget(label)
# # window.setLayout(layout)
# # window.show()
# # app.exec_()

# import cv2
# import sys
# from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
# from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
# from PyQt5.QtGui import QImage, QPixmap


# class Thread(QThread):
#     changePixmap = pyqtSignal(QImage)

#     def run(self):
#         cap = cv2.VideoCapture("rtsp://root:@172.19.1.17:554/live1s1.sdp")
#         while True:
#             ret, frame = cap.read()
#             if ret:
#                 # https://stackoverflow.com/a/55468544/6622587
#                 rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 h, w, ch = rgbImage.shape
#                 bytesPerLine = ch * w
#                 convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
#                 p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
#                 self.changePixmap.emit(p)


# class App(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 Video'
#         self.left = 100
#         self.top = 100
#         self.width = 640
#         self.height = 480
#         self.initUI()

#     @pyqtSlot(QImage)
#     def setImage(self, image):
#         self.label.setPixmap(QPixmap.fromImage(image))

#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.resize(1800, 1200)
#         # create a label
#         self.label = QLabel(self)
#         self.label.move(280, 120)
#         self.label.resize(640, 480)
#         th = Thread(self)
#         th.changePixmap.connect(self.setImage)
#         th.start()
#         self.show()



# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())
