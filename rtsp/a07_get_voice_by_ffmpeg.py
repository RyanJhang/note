
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
    command = [FFMPEG_BIN,
               '-f', 'dshow',
               '-i', in_filename,
               '-acodec', 'pcm_s32le',
               '-f', 's16le',
               '-ar', '44100',  # ouput will have 44100 Hz
               '-ac', '2',  # stereo (set to '1' for mono)
               '-']
    return subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10**8)


pipe = decode_audio('audio=麥克風 (15- IPEVO V4K)')

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
