

from functools import wraps
import logging
import subprocess
import sys
import time

import cv2
import ffmpeg
import numpy as np
import pyaudio

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        print('{0:<10}.{1:<30} : {2:.8f}'.format(func.__module__, func.__name__, end - start))
        return func_return_val
    return wrapper


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


def run_yuv(rtsp_url):
    decoder = YUVDecoder(rtsp_url)
    decoder.init_yuv_decoder()
    while 1:
        yuv = decoder.get_a_yuv_frame()

        image_scale = 0.25
        yuv = cv2.resize(yuv, (0, 0), fx=image_scale, fy=image_scale)
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
        cv2.imshow('image', bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    decoder.release_decoder()
    cv2.destroyAllWindows()


def run_rgb(rtsp_url):
    decoder = RGBDecoder(rtsp_url)
    decoder.init_rgb24_decoder()
    while 1:
        frame = decoder.get_a_rgb24_frame()
        image_scale = 0.25
        frame = cv2.resize(frame, (0, 0), fx=image_scale, fy=image_scale)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    decoder.release_decoder()
    cv2.destroyAllWindows()


def run_audio(rtsp_url):
    decoder = AudioDecoder(rtsp_url)
    decoder.init_audio_decoder()
    pyaudio_player = decoder.get_pyaudio_player()
    pyaudio_player.start_stream()

    # wait for stream to finish (5)
    while pyaudio_player.is_active():
        time.sleep(0.1)

    # stop stream (6)
    pyaudio_player.stop_stream()
    pyaudio_player.close()

    # close PyAudio (7)
    decoder.audio_process.terminate()


def run_audio_vedio(rtsp_url):
    a_decoder = AudioDecoder(rtsp_url)
    a_decoder.init_audio_decoder()
    a_player = a_decoder.get_pyaudio_player()
    a_player.start_stream()

    v_decoder = YUVDecoder(rtsp_url)
    v_decoder.init_yuv_decoder()
    while 1:
        yuv = v_decoder.get_a_yuv_frame()

        image_scale = 0.25
        yuv = cv2.resize(yuv, (0, 0), fx=image_scale, fy=image_scale)
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
        cv2.imshow('image', bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    v_decoder.release_decoder()
    cv2.destroyAllWindows()

    a_player.stop_stream()
    a_player.close()
    a_decoder.audio_process.terminate()


if __name__ == '__main__':
    # Use public RTSP Stream for testing
    # rtsp_url_2k = "rtsp://root:@172.19.1.122:554/live1s1.sdp"
    rtsp_url = "rtsp://root:@192.168.200.99:554/live1s1.sdp"
    run_yuv(rtsp_url)
    # run_rgb(rtsp_url)
    # run_audio(rtsp_url_av)
    # run_audio_vedio(rtsp_url_av)
