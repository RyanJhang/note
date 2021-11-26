import queue
import time

import cv2

import numpy as np
import ptvsd
from OpenGL import GL as gl
from PySide2.QtCore import QThread, QTimer, Signal
from PySide2.QtWidgets import QOpenGLWidget

from libs.a12_get_av_by_pyffmpeg_gpu_draw_by_opencv import (AudioDecoder, DSAudioDecoder, DSVideoDecoder,
                                                            YUVDecoder)
from libs.loggers.logger_formatter import LoggerFormatter

from read_qr_in_large_img_refactor import img_process


URL_MODE_UVC = 'UVC'
URL_MODE_RTSP = 'RTSP'

ALLOW_URL_MODE = [URL_MODE_RTSP, URL_MODE_UVC]


class PlayerInfo:
    def __init__(self,
                 url,
                 width,
                 height,
                 url_mode='RTSP',
                 fps=30,
                 reconnect_times=3,
                 need_video=True,
                 need_audio=False,
                 need_score=False):
        self.url = url
        self.width = width
        self.height = height
        self.url_mode = url_mode
        self.fps = fps
        self.reconnect_times = reconnect_times
        self.need_video = need_video
        self.need_audio = need_audio
        self.need_score = need_score
        if url_mode not in ALLOW_URL_MODE:
            raise Exception(f"url_mode not allow in [{ALLOW_URL_MODE}]")


class AudioThread(QThread):
    trigger = Signal(str)

    def __init__(self, player_info: PlayerInfo, logger: LoggerFormatter):
        QThread.__init__(self)
        self.player_info = player_info
        self.logger = logger
        self.a_decoder = self.get_audio_decoder()
        self.a_decoder.init_audio_decoder()
        self.a_decoder.get_audio_and_stream()

    def get_audio_decoder(self):
        decoder = None
        if self.player_info.url_mode == URL_MODE_RTSP:
            decoder = AudioDecoder(self.player_info.url)
        elif self.player_info.url_mode == URL_MODE_UVC:
            decoder = DSAudioDecoder(self.player_info.url)
        else:
            raise Exception("no allow url_mode")
        return decoder

    def run(self):
        ptvsd.debug_this_thread()
        self.a_decoder.stream.start_stream()

        while hasattr(self.a_decoder, "stream") and self.a_decoder.stream.is_active():
            time.sleep(0.1)

    def stop(self):
        self.terminate()
        self.a_decoder.release_decoder()


class VideoThread(QThread):
    retry_times_signal = Signal(str)

    def __init__(self, player_info: PlayerInfo, logger: LoggerFormatter, video_q: queue.Queue):
        QThread.__init__(self)
        self.player_info = player_info
        self.logger = logger
        self.video_q = video_q
        self.err = float('inf')

        self.v_decoder = self.get_video_decoder()

    def get_video_decoder(self):
        decoder = None
        if self.player_info.url_mode == URL_MODE_RTSP:
            decoder = YUVDecoder(self.player_info.url)
        elif self.player_info.url_mode == URL_MODE_UVC:
            decoder = DSVideoDecoder(self.player_info.url)
        else:
            raise Exception("no allow url_mode")
        return decoder

    def run(self):
        # ptvsd.debug_this_thread()
        self.retry_times = 0
        while hasattr(self.v_decoder, "video_process"):
            # self.logger.debug((self.video_q.full(), self.err))

            try:
                if self.err > 10:
                    self.err = 0
                    self.retry_times += 1
                    self.retry_times_signal.emit(str(self.retry_times))
                    self.logger.debug(str(self.retry_times))
                    self.v_decoder.init_video_decoder()

                img = self.v_decoder.get_a_frame()
                # rgb_img = cv2.cvtColor(img, cv2.COLOR_YUV2RGB_I420)  # BGR-->RGB
                rgb_img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_I420)  # BGR-->RGB

                if self.video_q.full():
                    self.video_q.get_nowait()

                rgb_img = img_process(rgb_img)
                # cv2.waitKey(1)
                self.video_q.put(rgb_img)

            except Exception as e:
                self.logger.debug(e)
                self.err += 1
            finally:
                pass

    def stop(self):
        self.hint_txet_in_video("No Signal")
        self.terminate()
        self.v_decoder.release_decoder()

    def lost_connection(self):
        self.hint_txet_in_video(f"No Signal, retry {self.retry_times} times.")

    def hint_txet_in_video(self, text: str):
        img = np.zeros((400, 400, 3), np.uint8)
        img.fill(90)
        cv2.putText(img, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 1, cv2.LINE_AA)
        self.video_q.put(img)


class PlayerWidget(QOpenGLWidget):

    def __init__(self, player_info: PlayerInfo, logger: LoggerFormatter, *args):
        QOpenGLWidget.__init__(self, *args)
        self.player_info = player_info
        self.logger = logger
        self.video_q = queue.Queue(30)

        self.video_update_timer = QTimer(self)
        self.video_update_timer.timeout.connect(self.opengl_update)

    def opengl_update(self):
        # self.logger.debug("opengl_update")
        # self.logger.info("opengl_update")
        self.update()

    def play(self):
        if self.player_info.need_audio:
            self.audio_thread = AudioThread(self.player_info, self.logger)
            self.audio_thread.start()

        if self.player_info.need_video:
            self.video_thread = VideoThread(self.player_info, self.logger, self.video_q)
            self.video_thread.start()
            self.video_update_timer.start(10)

            self.video_thread.retry_times_signal.connect(self.lost_connection)

        if self.player_info.need_score:
            self.video_thread = VideoThread(self.player_info, self.logger, self.video_q)
            self.video_thread.start()
            self.video_update_timer.start(10)

            self.video_thread.retry_times_signal.connect(self.lost_connection)

    def lost_connection(self, retry_times):
        if retry_times != '' and int(retry_times) >= 3:
            self.stop()
            if hasattr(self, "video_thread"):
                self.video_thread.lost_connection()

    def stop(self):
        if hasattr(self, "audio_thread"):
            self.audio_thread.stop()
            self.audio_thread.quit()
            self.audio_thread.wait()
        if hasattr(self, "video_thread"):
            self.video_thread.stop()
            self.video_thread.quit()
            self.video_thread.wait()
        if hasattr(self, "video_update_timer"):
            self.video_update_timer.start(1000)

        self.update()

    def initializeGL(self):
        gl.glClearColor(0.5, 0.8, 0.7, 1.0)

        # Enable texture map
        gl.glEnable(gl.GL_TEXTURE_2D)

    def resizeGL(self, w, h):
        # self.logger.debug((w, h))
        gl.glViewport(0, 0, w, h)
        gl.glLoadIdentity()

        if isinstance(self.width, int):
            widowWidth = self.width
            windowHeight = self.height
            # Make the display area proportional to the size of the view
            gl.glOrtho(int(-w / widowWidth), int(w / widowWidth), int(-h / windowHeight), int(h / windowHeight), -1.0, 1.0)

    def paintGL(self):
        # self.logger.debug(f"{self.video_q.qsize()}")
        # self.logger.debug("self.frame_q.empty()")

        # painting strategy
        if self.video_q.empty():
            return

        frame = self.video_q.get()
        if self.video_q.empty():
            self.video_q.put(frame)

        self._draw_frame_into_opengl(frame)

    def _draw_frame_into_opengl(self, frame):
        h, w = frame.shape[:2]
        # Paste into texture to draw at high speed
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, w, h, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, frame)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

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

    def special_painting(self):
        pass
        # cv2.imshow('Image', rgb_img)
        # if cv2.waitKey(1) == 27:
        #     cv2.destroyAllWindows()
        # temp = rgb_img[0:self.player_info.height // 5, 0:self.player_info.width // 5]
        # x = cv2.Sobel(temp, cv2.CV_16S, 1, 0)
        # y = cv2.Sobel(temp, cv2.CV_16S, 0, 1)
        # absX = np.absolute(x)
        # absY = np.absolute(y)
        # cv2.rectangle(frame, (crop_y_x[0], crop_y_x[2]), (crop_y_x[1], crop_y_x[3]), (0, 255, 0), -1)
        # cv2.imwrite('output{}.jpg'.format(i), frame)
        # val = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

        # res = cv2.sumElems(val)[0]
        # cv2.putText(rgb_img, str(res), (100, 400), cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
        #             10, (0, 255, 255), 1, cv2.LINE_AA)
