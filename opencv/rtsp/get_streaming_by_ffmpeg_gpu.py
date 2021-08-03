import subprocess
import json

# Use public RTSP Stream for testing
in_stream = "rtsp://root:@192.168.1.116:554/live1s1.sdp"

probe_command = ['ffprobe.exe',
                 '-loglevel', 'error',
                 '-rtsp_transport', 'tcp',  # Force TCP (for testing)]
                 '-select_streams', 'v:0',  # Select only video stream 0.
                 '-show_entries', 'format=bit_rate,filename,start_time:stream=duration,width,height,display_aspect_ratio,r_frame_rate,bit_rate', # Select only width and height entries
                 '-of', 'json', # Get output in JSON format
                 in_stream]

# Read video width, height using FFprobe:
p0 = subprocess.Popen(probe_command, stdout=subprocess.PIPE)
probe_str = p0.communicate()[0] # Reading content of p0.stdout (output of FFprobe) as string
p0.wait()
probe_dct = json.loads(probe_str) # Convert string from JSON format to dictonary.

print(probe_dct)
# Get width and height from the dictonary
width = probe_dct['streams'][0]['width']
height = probe_dct['streams'][0]['height']



import subprocess as sp
import cv2
import numpy as np
from PIL import Image
# import tensorflow as tf

ffmpeg_cmd_1 = ["ffmpeg.exe", "-y",
                # "-hwaccel",  "nvdec",
                "-c:v",  "h264_qsv",
                "-vsync", "1",
                # "-max_delay", "500000",
                # "-reorder_queue_size", "10000",
                "-i", "rtsp://root:@172.19.1.84:554/live1s1.sdp",
                "-f", "rawvideo",
                "-pix_fmt", "yuv420p",
                "-preset", "slow",
                "-an", "-sn",
                # "-vf", "fps=15",
                "-"]


ffmpeg1 = sp.Popen(ffmpeg_cmd_1, stdout=sp.PIPE, bufsize=10)

h, w = height, width
h_half, w_half = h//2, w//2
k = w * h
k_offset = k//4

frame_bytes = int(w*h*6//4)
while True:
    
    raw_frame = ffmpeg1.stdout.read(frame_bytes)  # read bytes of single frames
    
    if raw_frame == b'':
        print('Error reading frame!!!')  # Break the loop in case of an error (too few bytes were read).
        break

    # y = np.frombuffer(raw_frame[0:k], dtype=np.uint8).reshape((h, w))
    # u = np.frombuffer(raw_frame[k:k+k_offset], dtype=np.uint8).reshape((h_half, w_half))
    # v = np.frombuffer(raw_frame[k+k_offset:], dtype=np.uint8).reshape((h_half, w_half))
    # u = np.reshape(cv2.resize(np.expand_dims(u, -1), (w, h)), (h, w))
    # v = np.reshape(cv2.resize(np.expand_dims(v, -1), (w, h)), (h, w))
    # image = np.stack([y, u, v], axis=-1)
    # img_YUV = cv2.merge([y, u, v])
    
    # img_YUV = cv2.resize(img_YUV, None, fx=1/2, fy=1/2)
    # dst = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)
    # cv2.imshow("YUV2BGR_I420", dst)
    # frame = np.frombuffer(raw_frame, np.uint8)
    # frame = frame.reshape((height*6//4, width))
    
    yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height*6//4, width))

    image_scale = 0.25
    yuv = cv2.resize(yuv, (0, 0), fx=image_scale, fy=image_scale)

    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
    cv2.imshow('image', bgr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ffmpeg1.stdout.flush()

cv2.destroyAllWindows()
