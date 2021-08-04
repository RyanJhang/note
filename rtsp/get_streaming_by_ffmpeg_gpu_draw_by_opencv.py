
import numpy as np
import cv2
import subprocess
import json


class YUVInfo:
    width = None
    height = None
    yuv_height = None
    frame_bytes = None


class GetStreamingByFFmpegDrawByOpencv:
    def __init__(self, rtsp_url, mode="auto", stream_info=None):
        self.rtsp_url = rtsp_url
        self.stream_info = self._get_streaming_info(mode, stream_info)

        self.yuv_info = YUVInfo()
        self.ffmpeg_process = None

    def _get_streaming_info(self, mode, stream_info):
        if mode == "auto":
            stream_info = self.get_info_by_ffprobe()
        else:
            if stream_info is None:
                raise Exception("The stream_info could not be None.")
        return stream_info

    def get_info_by_ffprobe(self):
        probe_command = ['ffprobe.exe',
                         '-loglevel', 'error',
                         '-rtsp_transport', 'tcp',  # Force TCP (for testing)]
                         '-select_streams', 'v:0',  # Select only video stream 0.
                         '-show_entries', 'stream=width,height',  # Select only width and height entries
                         '-of', 'json',  # Get output in JSON format
                         self.rtsp_url]

        # Read video width, height using FFprobe:
        probe_process = subprocess.Popen(probe_command, stdout=subprocess.PIPE)

        # Reading content of p0.stdout (output of FFprobe) as string
        probe_str = probe_process.communicate()[0]  
        probe_process.wait()

        # Convert string from JSON format to dictonary.
        probe_dct = json.loads(probe_str)  

        # Get width and height from the dictonary
        # width = probe_dct['streams'][0]['width']
        # height = probe_dct['streams'][0]['height']
        return probe_dct['streams'][0]

    def init_decoder(self):
        ffmpeg_command = ["ffmpeg.exe", "-y",
                          "-hwaccel", "dxva2",
                          # "-c:v",  "h264_qsv",
                          "-vsync", "1",
                          "-max_delay", "500000",
                          # "-reorder_queue_size", "10000",
                          "-i", self.rtsp_url,
                          "-f", "rawvideo",
                          "-pix_fmt", "yuv420p",
                          "-preset", "slow",
                          "-an", "-sn",
                          # "-vf", "fps=15",
                          "-"]

        self.ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, bufsize=10)

        self.yuv_info.width = self.stream_info['width']
        self.yuv_info.height = self.stream_info['height']
        self.yuv_info.yuv_height = self.stream_info['height'] * 6 // 4
        self.yuv_info.frame_bytes = int(self.yuv_info.width * self.yuv_info.yuv_height)

    def get_a_yuv_frame(self):

        raw_frame = self.ffmpeg_process.stdout.read(self.yuv_info.frame_bytes)  # read bytes of single frames

        if raw_frame == b'':
            # Break the loop in case of an error (too few bytes were read).
            raise Exception("Error reading frame!!!")

        yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.yuv_info.yuv_height, self.yuv_info.width))

        self.ffmpeg_process.stdout.flush()
        return yuv

    def release_decoder(self):
        if self.ffmpeg_process:
            self.ffmpeg_process.kill()


if __name__ == '__main__':
    # Use public RTSP Stream for testing
    rtsp_url = "rtsp://root:@172.19.1.122:554/live1s1.sdp"

    player = GetStreamingByFFmpegDrawByOpencv(rtsp_url)
    player.init_decoder()
    while 1:
        yuv = player.get_a_yuv_frame()

        image_scale = 0.25
        yuv = cv2.resize(yuv, (0, 0), fx=image_scale, fy=image_scale)
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
        cv2.imshow('image', bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    player.release_decoder()
    cv2.destroyAllWindows()
