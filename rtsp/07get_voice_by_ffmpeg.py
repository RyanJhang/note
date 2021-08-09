
import ffmpeg
import pyaudio
import numpy
import time
import sys
import subprocess

# FFMPEG_BIN = "ffmpeg" # on Linux
FFMPEG_BIN = "ffmpeg.exe"  # on Windows


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

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = pipe.stdout.read(10000)
    data = numpy.frombuffer(data, dtype="int32")
    data = data.reshape((len(data) // 2, 2))
    #data = pipe.readbuffer(frame_count)
    return (data, pyaudio.paContinue)


# open stream using callback (3)
stream = p.open(format=pyaudio.paInt32,
                channels=2,
                rate=44100,
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()

# close PyAudio (7)
p.terminate()
