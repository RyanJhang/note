
import cv2
import numpy as np
import subprocess

# Use public RTSP Stream for testing
in_stream = "rtsp://root:12345678z@192.168.1.119:554/live1s1.sdp"

if 1:
    # Read video width, height and framerate using OpenCV (use it if you don't know the size of the video frames).

    # Use public RTSP Streaming for testing:
    cap = cv2.VideoCapture(in_stream)

    framerate = cap.get(5) #frame rate

    # Get resolution of input video
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Release VideoCapture - it was used just for getting video resolution
    cap.release()
else:
    # Set the size here, if video frame size is known
    width = 240
    height = 160


command = ['ffmpeg.exe',
           #'-rtsp_flags', 'listen',  # The "listening" feature is not working (probably because the stream is from the web)
           '-rtsp_transport', 'tcp',  # Force TCP (for testing)
           '-max_delay', '30000000',  # 30 seconds (sometimes needed because the stream is from the web).
           '-i', in_stream,
           '-f', 'image2pipe',
           '-pix_fmt', 'bgr24',
           '-vcodec', 'rawvideo', '-an', '-']

# Open sub-process that gets in_stream as input and uses stdout as an output PIPE.
p1 = subprocess.Popen(command, stdout=subprocess.PIPE)

while True:
    # read width*height*3 bytes from stdout (1 frame)
    raw_frame = p1.stdout.read(width*height*3)

    if len(raw_frame) != (width*height*3):
        print('Error reading frame!!!')  # Break the loop in case of an error (too few bytes were read).
        break

    # Convert the bytes read into a NumPy array, and reshape it to video frame dimensions
    frame = np.fromstring(raw_frame, np.uint8)
    frame = frame.reshape((height, width, 3))

    # Show video frame
    image_scale = 0.25
    frame = cv2.resize(frame, (0, 0), fx=image_scale, fy=image_scale)
    cv2.imshow('image', frame)
    cv2.waitKey(1)
  
# Wait one more second and terminate the sub-process
try:
    p1.wait(1)
except (sp.TimeoutExpired):
    p1.terminate()


'''```
----------------------------------------------------------------

```'''
# import ffmpeg

# stream = ffmpeg.input("rtsp://root:12345678z@192.168.1.119:554/live1s1.sdp", ss=0)
# file = stream.output("test.png", vframes=1)
# testfile = file.run(capture_stdout=True, capture_stderr=True)


'''```
----------------------------------------------------------------

```'''



# import ffmpeg
# import numpy
# import cv2
# import sys
# import random , os


# def read_frame_as_jpeg(in_file, frame_num):
#     """
#     指定幀數讀取任意幀
#     """
#     out, err = (
#         ffmpeg.input(in_file)
#               .filter('select', 'gte(n,{})'.format(frame_num))
#               .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
#               .run(capture_stdout=True)
#     )
#     return out


# def get_video_info(in_file):
#     """
#     獲取視訊基本資訊
#     """
#     try:
#         probe = ffmpeg.probe(in_file)
#         video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
#         if video_stream is None:
#             print('No video stream found', file=sys.stderr)
#             sys.exit(1)
#         return video_stream
#     except ffmpeg.Error as err:
#         print(str(err.stderr, encoding='utf8'))
#         sys.exit(1)


# if __name__ == '__main__':
#     file_path = r'C:\Users\jhang\Documents\ryan\note\test.mp4'
#     print(os.path.exists(file_path))
#     # video_info = get_video_info(file_path)
#     # total_frames = int(video_info['nb_frames'])
#     # print('總幀數：' + str(total_frames))
#     # random_frame = random.randint(1, total_frames)
#     # print('隨機幀：' + str(random_frame))
#     random_frame = 1
#     out = read_frame_as_jpeg(file_path, random_frame)
#     image_array = numpy.asarray(bytearray(out), dtype="uint8")
#     image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
#     cv2.imshow('frame', image)
#     cv2.waitKey()