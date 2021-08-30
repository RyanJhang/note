
import ffmpeg
import pyaudio
import numpy
import time
import sys
import subprocess

# FFMPEG_BIN = "ffmpeg" # on Linux
FFMPEG_BIN = "ffmpeg.exe"  # on Windows
CHUNK = 1024


def decode_audio(in_filename, **input_kwargs):
    try:
        args = (ffmpeg
                .input(in_filename, **input_kwargs)
                .output('pipe:', format='s32le', acodec='pcm_s32le', ac=2, ar=44100)
                .compile()
                )
    except ffmpeg.Error as e:
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    return subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=10**8)


pipe = decode_audio("rtsp://root:12345678z@172.19.1.137:554/live1s1.sdp")

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=pyaudio.paInt32,
                channels=2,         # use ffprobe to get this from the file beforehand
                rate=44100,         # use ffprobe to get this from the file beforehand
                output=True)

# read data
data = pipe.stdout.read(CHUNK)

# play stream (3)
while len(data) > 0:
    # data = numpy.frombuffer(data, dtype="int32")
    # data = data.reshape((len(data) // 2, 2))
    stream.write(data)
    data = pipe.stdout.read(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()