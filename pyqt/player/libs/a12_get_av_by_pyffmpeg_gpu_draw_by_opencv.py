
import logging
import re
import subprocess
import sys
import time

import cv2
import ffmpeg
import numpy as np
import pyaudio

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)


class FrameInfo:
    width = None
    height = None
    yuv_height = None
    frame_bytes = None


class StreamingInfo:
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.probe_info = self._get_info_by_ffprobe()
        self.video_info = None
        self.audio_info = None

    def _get_info_by_ffprobe(self):
        """
        獲取視訊基本資訊，大約會花 1.1 - 1.3秒
        """
        try:
            probe = ffmpeg.probe(self.rtsp_url)
            if probe is None:
                print('No stream found', file=sys.stderr)
                sys.exit(1)
            return probe
        except ffmpeg.Error as err:
            print(str(err.stderr, encoding='utf8'))
            sys.exit(1)

    def get_video_info(self):
        if self.video_info is None:
            self.video_info = next((stream for stream in self.probe_info['streams'] if stream['codec_type'] == 'video'), None)
        return self.video_info

    def get_audio_info(self):
        if self.audio_info is None:
            self.audio_info = next((stream for stream in self.probe_info['streams'] if stream['codec_type'] == 'audio'), None)
        return self.audio_info


class YUVDecoder(StreamingInfo):
    def __init__(self, rtsp_url):
        StreamingInfo.__init__(self, rtsp_url)
        self.video_process = None

    def init_video_decoder(self):
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
        self.frame_info.width = self.get_video_info()['width']
        self.frame_info.height = self.get_video_info()['height']
        self.frame_info.yuv_height = self.get_video_info()['height'] * 6 // 4
        self.frame_info.frame_bytes = int(self.frame_info.width * self.frame_info.yuv_height)

    def get_a_frame(self):
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
            self.video_process = None


class RGBDecoder(StreamingInfo):
    def __init__(self, rtsp_url):
        StreamingInfo.__init__(self, rtsp_url)
        self.video_process = None

    def init_video_decoder(self):
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
            .output('pipe:1',
                    format='rawvideo',
                    pix_fmt='bgr24',
                    preset="slow")
            .compile()
        )
        self.video_process = subprocess.Popen(args, stdout=subprocess.PIPE)

        self.frame_info = FrameInfo()
        self.frame_info.width = self.get_video_info()['width']
        self.frame_info.height = self.get_video_info()['height']
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


def get_stdout(list_cmd):
    print(" ".join(list_cmd))
    p = subprocess.Popen(list_cmd, stderr=subprocess.PIPE)
    lines = []
    for line in iter(p.stderr.readline, ''):
        if line == b'':
            break
        lines.append(line)
    p.terminate()
    return lines


class DSVideoOption:
    def __init__(self):
        self.vcodec = []
        self.min_s = []
        self.min_fps = []
        self.max_s = []
        self.max_fps = []

    def get_info(self, index):
        return self.vcodec[index], self.min_s[index], self.min_fps[index], self.max_s[index], self.max_fps[index]

    def get_info_by_max_video_size(self):
        max_index = self._get_max_resolution_index(self.max_s)
        return self.get_info(max_index)

    def _get_max_resolution_index(self, resolution_list):
        temp = 0
        max_index = None

        for index, resolution in enumerate(resolution_list):
            cur = self._get_area(resolution)
            if cur > temp:
                temp = cur
                max_index = index

        return max_index

    def _get_area(self, resolution):
        if not re.fullmatch(r'\d+x\d+', resolution):
            raise Exception(f'resolution is not valid: {resolution}')

        width, length = resolution.split('x')
        return int(width) * int(length)


class DSVideoInfo:
    def __init__(self, device_name, device_number):
        self.device_number = device_number
        self.device_name = device_name
        self.device_option = DSVideoOption()
        self._get_video_device_option()

    def _get_video_device_option(self):
        list_cmd = [
            'ffmpeg.exe',
            '-list_options', 'true',
            '-video_device_number', str(self.device_number),
            '-f', 'dshow',
            '-i', self.device_name
        ]
        lines = get_stdout(list_cmd)

        for line in lines:
            re_result = re.search(r'vcodec=(.+)  min s=(\d+x\d+) fps=(\d+) max s=(\d+x\d+) fps=(\d+)', line.decode(encoding='UTF-8'))
            if re_result:
                self.device_option.vcodec.append(re_result.group(1))
                self.device_option.min_s.append(re_result.group(2))
                self.device_option.min_fps.append(re_result.group(3))
                self.device_option.max_s.append(re_result.group(4))
                self.device_option.max_fps.append(re_result.group(5))
            if 'Immediate exit requested'.encode(encoding='UTF-8') in line:
                break


class DSAudioOption:
    def __init__(self):
        self.min_ch = []
        self.min_bits = []
        self.min_rate = []
        self.max_ch = []
        self.max_bits = []
        self.max_rate = []

    def get_info(self, index):
        return self.min_ch[index], self.min_bits[index], self.min_rate[index], self.max_ch[index], self.max_bits[index], self.max_rate[index]


class DSAudioInfo:
    def __init__(self, device_name, device_number):
        self.device_number = device_number
        self.device_name = device_name
        self.device_option = DSAudioOption()
        self._get_video_device_option()

    def _get_video_device_option(self):
        list_cmd = [
            'ffmpeg.exe',
            '-list_options', 'true',
            '-video_device_number', str(self.device_number),
            '-f', 'dshow',
            '-i', self.device_name
        ]
        lines = get_stdout(list_cmd)

        for line in lines:
            re_result = re.search(r'min ch=(\d+)\sbits=(\d+)\srate=\s(\d+)\smax ch=(\d+)\sbits=(\d+)\srate=\s(\d+)', line.decode(encoding='UTF-8'))
            if re_result:
                self.device_option.min_ch.append(re_result.group(1))
                self.device_option.min_bits.append(re_result.group(2))
                self.device_option.min_rate.append(re_result.group(3))
                self.device_option.max_ch.append(re_result.group(4))
                self.device_option.max_bits.append(re_result.group(5))
                self.device_option.max_rate.append(re_result.group(6))
            if 'Immediate exit requested'.encode(encoding='UTF-8') in line:
                break


class DirectShowInfo:
    """
    Other way to get video_info, but not recommand:(-video_size 1280x720 -video_device_number 0 is required args)
        ffprobe -show_format -show_streams -of json -f dshow -i video="IPEVO V4K" -video_size 1280x720 -video_device_number 0
    """
    def __init__(self, device_number=0):
        video_device_list, audioa_devices = self._get_device_list_by_dshow()
        self.video_info = DSVideoInfo(device_name=video_device_list[0], device_number=device_number)
        self.audio_info = DSAudioInfo(device_name=audioa_devices[0], device_number=device_number)

    def _get_device_list_by_dshow(self):
        def parse_av_devices(lines):
            video_devices, audioa_devices = [], []
            video_flag, audio_flag = None, None

            for line in lines:
                if 'Immediate exit requested'.encode(encoding='UTF-8') in line:
                    break

                if 'DirectShow video devices'.encode(encoding='UTF-8') in line:
                    video_flag = True
                    audio_flag = False
                    continue
                elif 'DirectShow audio devices'.encode(encoding='UTF-8') in line:
                    video_flag = False
                    audio_flag = True
                    continue

                if video_flag:
                    cam = re.search('"(.*)"', line.decode(encoding='UTF-8')).group(1)
                    cam = 'video=' + cam if cam else ''
                    video_devices.append(cam)

                elif audio_flag:
                    cam = re.search('"(.*)"', line.decode(encoding='UTF-8')).group(1)
                    cam = 'audio=' + cam if cam else ''
                    audioa_devices.append(cam)

            return video_devices, audioa_devices

        list_cmd = 'ffmpeg -list_devices true -f dshow -i dummy'.split()
        lines = get_stdout(list_cmd)
        return parse_av_devices(lines)


class DSVideoDecoder(DirectShowInfo):
    def __init__(self, device_number):
        DirectShowInfo.__init__(self, device_number)
        self.video_process = None

    def init_video_decoder(self):
        _, video_size, fps, _, _ = self.video_info.device_option.get_info_by_max_video_size()
        logger.info('init_dshow_decoder ffmpeg process')

        command = [
            'ffmpeg.exe',
            '-hwaccel', 'auto',
            '-video_size', video_size,
            '-video_device_number', str(self.video_info.device_number),
            # '-rtbufsize', '100M',
            '-f', 'dshow',
            '-i', self.video_info.device_name,

            '-y',
            '-r', str(fps),
            '-pix_fmt', 'yuv420p',
            '-f', 'rawvideo',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency ',
            '-'
        ]

        self.video_process = subprocess.Popen(command, stdout=subprocess.PIPE)
        print(' '.join(command))
        width, height = [int(s) for s in video_size.split('x')]

        self.frame_info = FrameInfo()
        self.frame_info.width = width
        self.frame_info.height = height
        self.frame_info.yuv_height = height * 6 // 4
        self.frame_info.frame_bytes = int(self.frame_info.width * self.frame_info.yuv_height)

    def get_a_frame(self):
        raw_frame = self.video_process.stdout.read(self.frame_info.frame_bytes)  # read bytes of single frames
        # print("self.video_process.returncode", self.video_process.returncode, self.video_process.stderr.readline())
        if raw_frame == b'':
            # Break the loop in case of an error (too few bytes were read).
            raise Exception("Error reading frame!!!")

        yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.frame_info.yuv_height, self.frame_info.width))

        self.video_process.stdout.flush()
        # self.video_process.stderr.flush()
        return yuv

    def release_decoder(self):
        if self.video_process:
            self.video_process.kill()
            self.video_process = None


class DSAudioDecoder(DirectShowInfo):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5

    def __init__(self, device_number):
        DirectShowInfo.__init__(self, device_number)
        self.audio_process = None
        self.stream = None

    def init_audio_decoder(self):
        min_ch, min_bits, min_rate, max_ch, max_bits, max_rate = self.audio_info.device_option.get_info(0)

        command = [
            'ffmpeg.exe',
            '-video_device_number', str(self.audio_info.device_number),
            '-f', 'dshow',
            '-i', self.audio_info.device_name,

            '-f', 's16le',
            # '-volume', '1',
            '-acodec', 'pcm_s16le',
            '-ac', '1',
            '-ar', '16000',
            '-'
        ]

        self.audio_process = subprocess.Popen(command, stdout=subprocess.PIPE)
        logger.info('init_ds_audio_decoder ffmpeg process')
        print(' '.join(command))

    def get_audio_and_stream(self):
        def callback(in_data, frame_count, time_info, status):
            if self.audio_process.poll() is None:
                data = self.audio_process.stdout.read(2 * frame_count)
                return (data, pyaudio.paContinue)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  output=True,
                                  stream_callback=callback)

    def release_decoder(self):
        if hasattr(self, "pyaudio_player"):
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if hasattr(self, "p"):
            self.p.terminate()

        if hasattr(self, "audio_process"):
            self.audio_process.terminate()


class AudioDecoder:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5

    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.audio_process = None
        self.stream = None

    def init_audio_decoder(self):
        try:
            args = (ffmpeg
                    .input(self.rtsp_url,
                           rtsp_transport="tcp",
                           vsync="1",
                           preset="slow",
                           flags="low_delay")
                    .filter('volume', 1)
                    .output('pipe:1',
                            format='s16le',
                            acodec='pcm_s16le',
                            ac=1,
                            ar="16k")
                    .overwrite_output()
                    .compile()
                    )
        except ffmpeg.Error as e:
            # print("*"*50)
            print(e.stderr, file=sys.stderr)
            # sys.exit(1)
        self.audio_process = subprocess.Popen(args, stdout=subprocess.PIPE)

    def get_a_audio_chunk(self):
        audio_chunk = self.audio_process.stdout.read(self.CHUNK)
        if audio_chunk == b'':
            raise Exception("Error audio_chunk !!!")

        self.audio_process.stdout.flush()
        return audio_chunk

    def release_decoder(self):
        if hasattr(self, "pyaudio_player"):
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if hasattr(self, "p"):
            self.p.terminate()

        if hasattr(self, "audio_process"):
            self.audio_process.terminate()

    def get_audio_and_stream(self):
        def callback(in_data, frame_count, time_info, status):
            if self.audio_process.poll() is None:
                data = self.audio_process.stdout.read(2 * frame_count)
                return (data, pyaudio.paContinue)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  output=True,
                                  stream_callback=callback)


def run_yuv(rtsp_url):
    decoder = YUVDecoder(rtsp_url)
    decoder.init_video_decoder()
    while 1:
        yuv = decoder.get_a_frame()

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
    decoder.init_video_decoder()
    while 1:
        frame = decoder.get_a_rgb24_frame()
        image_scale = 0.25
        frame = cv2.resize(frame, (0, 0), fx=image_scale, fy=image_scale)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    decoder.release_decoder()
    cv2.destroyAllWindows()


def run_ds_video(device_number):
    decoder = DSVideoDecoder(device_number)
    decoder.init_video_decoder()
    while 1:
        yuv = decoder.get_a_frame()

        image_scale = 0.25
        yuv = cv2.resize(yuv, (0, 0), fx=image_scale, fy=image_scale)
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
        cv2.imshow('image', bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    decoder.release_decoder()
    cv2.destroyAllWindows()


def run_ds_audio(device_number):
    decoder = DSAudioDecoder(device_number)
    decoder.init_audio_decoder()
    decoder.get_audio_and_stream()
    decoder.stream.start_stream()

    # wait for stream to finish (5)
    while decoder.stream.is_active():
        time.sleep(0.1)

    # stop stream (6)
    decoder.stream.stop_stream()
    decoder.stream.close()

    # close PyAudio (7)
    decoder.audio_process.terminate()


def run_audio(rtsp_url):
    decoder = AudioDecoder(rtsp_url)
    decoder.init_audio_decoder()
    pyaudio_player = decoder.get_audio_and_stream()
    pyaudio_player.start_stream()

    # wait for stream to finish (5)
    while pyaudio_player.is_active():
        time.sleep(0.1)

    # stop stream (6)
    pyaudio_player.stop_stream()
    pyaudio_player.close()

    # close PyAudio (7)
    decoder.audio_process.terminate()


def run_audio_sync(rtsp_url):
    decoder = AudioDecoder(rtsp_url)
    decoder.init_audio_decoder()

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,         # use ffprobe to get this from the file beforehand
                    rate=16000,         # use ffprobe to get this from the file beforehand
                    output=True)

    while 1:
        data = decoder.get_a_audio_chunk()
        stream.write(data)

    stream.stop_stream()
    stream.close()

    p.terminate()
    decoder.release_decoder()


def run_audio_vedio(rtsp_url):
    a_decoder = AudioDecoder(rtsp_url)
    a_decoder.init_audio_decoder()
    a_player = a_decoder.get_pyaudio_and_stream()
    a_player.start_stream()

    v_decoder = YUVDecoder(rtsp_url)
    v_decoder.init_video_decoder()
    while 1:
        yuv = v_decoder.get_a_frame()

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
    rtsp_url_2k = "rtsp://root:@172.19.1.122:554/live1s1.sdp"
    rtsp_url_av = "rtsp://root:12345678z@172.19.1.137:554/live1s1.sdp"

    # run_yuv(rtsp_url)
    # run_rgb(rtsp_url)
    # run_ds_AV(0)
    run_ds_audio(0)
    # run_audio(rtsp_url_av)
    # run_audio_sync(rtsp_url_av)
    # run_audio_vedio(rtsp_url_av)
