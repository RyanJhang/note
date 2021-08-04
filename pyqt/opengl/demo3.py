import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys

#window dimensions

# 载入背景图像
fullname = r"C:\Users\ryan.jhang\Documents\ryan\note\opencv\blemish\blob.jpg"
image = cv2.imread(fullname)
img_rgb  = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

width, height = image.shape[1], image.shape[0]
# width = 1920
# height = 1080
nRange = 1.0

global capture
capture = None


def cv2array(im):
    h, w, c = im.shape
    a = np.fromstring(
        im.tostring(),
        dtype=im.dtype,
        count=w*h*c)
    a.shape = (h, w, c)
    return a


def init():
    #glclearcolor (r, g, b, alpha)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)


def idle():
    #capture next frame

    # global capture
    # _, image = capture.read()

    # cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #you must convert the image to array for glTexImage2D to work
    #maybe there is a faster way that I don't know about yet...

    #print image_arr

    # Create Texture
    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGB,
                 1080, 1920,
                 0,
                 GL_RGB,
                 GL_UNSIGNED_BYTE,
                 img_rgb)
    cv2.imshow('frame', image)
    cv2.waitKey(0)

    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    #this one is necessary with texture2d for some reason
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # Set Projection Matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

    # Switch to Model View Matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Draw textured Quads
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(0.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(width, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(width, height)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(0.0, height)
    glEnd()

    glFlush()
    glutSwapBuffers()


def reshape(w, h):
    if h == 0:
      h = 1

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    # allows for reshaping the window without distoring shape

    if w <= h:
      glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
    else:
      glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard(key, x, y):
    global anim
    if key == chr(27):
      sys.exit()


def main():
    global capture
    # start openCV capturefromCAM
    # capture = cv2.VideoCapture("rtsp://root:@172.19.1.122:554/live1s1.sdp")
    # print(capture)
    # capture.set(3, 1920)
    # capture.set(4, 1080)
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("OpenGL + OpenCV")

    init()
    glutMainLoop()


main()
