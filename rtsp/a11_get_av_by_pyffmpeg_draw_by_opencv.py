
import argparse
import logging
import subprocess
import sys

import cv2
import ffmpeg
import numpy as np
import pyaudio

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def read_frame_as_jpeg(in_file, frame_num):
    """
    指定幀數讀取任意幀
    """
    out, err = (
        ffmpeg
        .input(in_file)
        .filter('select', 'gte(n,{})'.format(frame_num))
        .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
        .run(capture_stdout=True)
    )
    return out


def get_video_info(in_file):
    """
    獲取視訊基本資訊
    """
    try:
        probe = ffmpeg.probe(in_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print('No video stream found', file=sys.stderr)
            sys.exit(1)
        return video_stream
    except ffmpeg.Error as err:
        print(str(err.stderr, encoding='utf8'))
        sys.exit(1)


def ffmpeg_video_process(in_filename):
    logger.info('Starting ffmpeg process1')
    args = (
        ffmpeg
        .input(in_filename,
               hwaccel="dxva2",
               rtsp_transport="tcp",
               vsync="1",
               preset="slow",
               max_delay="500000")
        .output('pipe:',
                format='rawvideo',
                pix_fmt='yuv420p',
                preset="slow")
        .compile()
    )
    return subprocess.Popen(args, stdout=subprocess.PIPE)


def read_frame(video_process, width, height):
    """
    RGB24 size ＝ width * heigth * 3 Bit
    RGB32 size ＝ width * heigth * 4 Bit
    yuv420 size ＝ width * heigth * 1.5 Bit (yuv yuv yuv)
    yuv420p size ＝ width * heigth * 6 // 14 Bit (yyyyyyyy uuuuuuuu vvvvv)
    """
    logger.debug('Reading frame')

    yuv_height = height * 6 // 4
    frame_size = int(width * yuv_height)

    # read bytes of single frames
    in_bytes = video_process.stdout.read(frame_size)
    if len(in_bytes) == 0:
        yuv_frame = None
    else:
        assert len(in_bytes) == frame_size
        yuv_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([yuv_height, width])
        )

    return yuv_frame


def ffmpeg_audio_process(in_filename):
    try:
        args = (ffmpeg
                .input(in_filename, vsync="1")['a']
                .filter('volume', 1)
                .output('pipe:', format='s16le', acodec='pcm_s16le', ac=1, ar="16k")
                .overwrite_output()
                .compile()
                )
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    return subprocess.Popen(args, stdout=subprocess.PIPE)

def pyaudio_process(audio_process):
    # instantiate PyAudio (1)
    audio = pyaudio.PyAudio()

    # define callback (2)
    def callback(in_data, frame_count, time_info, status):
        if audio_process.poll() is None:
            data = audio_process.stdout.read(2 * frame_count)
            return (data, pyaudio.paContinue)
        # data = audio_process.stdout.read(2 * frame_count)
        # data = numpy.frombuffer(data, dtype="int32")
        # data = data.reshape((len(data)//2, 2))
        # # # data = pipe.readbuffer(frame_count)
        # return (data, pyaudio.paContinue)

    # open stream using callback (3)
    # pyaudio_player = audio.open(format=pyaudio.paInt32,
    #                             channels=2,
    #                             rate=44100,
    #                             output=True,
    #                             stream_callback=callback)
    pyaudio_player = audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=16000,
                                output=True,
                                stream_callback=callback)
    return pyaudio_player


if __name__ == '__main__':
    file_path = "rtsp://root:@172.19.1.122:554/live1s1.sdp"
    # audio init
    audio_process = ffmpeg_audio_process(file_path)
    pyaudio_player = pyaudio_process(audio_process)
    pyaudio_player.start_stream()

    # video init
    video_info = get_video_info(file_path)
    video_process = ffmpeg_video_process(file_path)

    while True:
        yuv_frame = read_frame(video_process, video_info['width'], video_info['height'])
        if yuv_frame is None:
            logger.info('End of input stream')
            break

        image_scale = 0.25
        yuv_frame = cv2.resize(yuv_frame, (0, 0), fx=image_scale, fy=image_scale)
        bgr_frame = cv2.cvtColor(yuv_frame, cv2.COLOR_YUV2BGR_I420)
        cv2.imshow('bgr_frame', bgr_frame)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        video_process.stdout.flush()
    cv2.destroyAllWindows()
