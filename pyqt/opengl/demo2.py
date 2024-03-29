import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *

from PyQt5.QtWidgets import *
app = QApplication(sys.argv)

# Use a QGLFormat with the swap interval set to 1
qgl_format = QGLFormat()
qgl_format.setSwapInterval(1)

# Construct a QGLWidget using the above format
qgl_widget = QGLWidget(qgl_format)

# Set up a timer to call updateGL() every 0 ms
update_gl_timer = QTimer()
update_gl_timer.setInterval(0)
update_gl_timer.start()
update_gl_timer.timeout.connect(qgl_widget.updateGL)

# Set up a graphics view and a scene
grview = QGraphicsView()
grview.setViewport(qgl_widget)
scene = QGraphicsScene()
scene.addPixmap(QPixmap(r'C:\Users\ryan.jhang\Documents\ryan\note\markers.png'))
grview.setScene(scene)

grview.show()

sys.exit(app.exec_())