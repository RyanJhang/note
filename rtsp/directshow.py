import re
import subprocess

import cv2
import numpy as np


def get_dshow_web_cam():
    list_cmd = 'ffmpeg -list_devices true -f dshow -i dummy'.split()
    p = subprocess.Popen(list_cmd, stderr=subprocess.PIPE)
    web_cams = []
    flagcam = None
    for line in iter(p.stderr.readline, ''):
        if flagcam:
            cam = re.search('"(.*)"', line.decode(encoding='UTF-8')).group(1)
            cam = 'video=' + cam if cam else ''
            web_cams.append(cam)
            flagcam = False
        elif 'DirectShow video devices'.encode(encoding='UTF-8') in line:
            flagcam = True
        elif 'Immediate exit requested'.encode(encoding='UTF-8') in line:
            break
    return web_cams


class DeviceOption:
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


def get_device_option(dshow_web_cam, device_number='0'):
    command = [
        'ffmpeg.exe',
        '-list_options', 'true',
        '-video_device_number', device_number,
        '-f', 'dshow',
        '-i', dshow_web_cam
    ]
    p = subprocess.Popen(command, stderr=subprocess.PIPE)
    option = DeviceOption()

    for line in iter(p.stderr.readline, ''):
        print(line)
        re_result = re.search(r'vcodec=(.+)  min s=(\d+x\d+) fps=(\d+) max s=(\d+x\d+) fps=(\d+)', line.decode(encoding='UTF-8'))
        if re_result:
            option.vcodec.append(re_result.group(1))
            option.min_s.append(re_result.group(2))
            option.min_fps.append(re_result.group(3))
            option.max_s.append(re_result.group(4))
            option.max_fps.append(re_result.group(5))
        if 'Immediate exit requested'.encode(encoding='UTF-8') in line:
            break
    return option


if __name__ == '__main__':
    dshow_web_cams = get_dshow_web_cam()
    if len(dshow_web_cams) > 1:
        raise Exception('Comfirm the number of web_cams')

    dshow_web_cam = dshow_web_cams[0]

    device_option = get_device_option(dshow_web_cam)
    vcodec, video_size, fps, _, _ = device_option.get_info_by_max_video_size()

    width, height = [int(s) for s in video_size.split('x')]

    command = [
        'ffmpeg.exe',
        '-hwaccel', 'auto',
        '-video_size', video_size,
        '-video_device_number', '0',
        '-f', 'dshow',
        '-i', dshow_web_cam,

        '-y',
        '-r', fps,
        '-pix_fmt', 'yuv420p',
        '-f', 'rawvideo',
        '-preset', 'slow',
        '-'
    ]

    # Open sub-process that gets in_stream as input and uses stdout as an output PIPE.
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
    print(' '.join(command))

    yuv_height = height * 6 // 4
    frame_size = int(width * yuv_height)
    while True:
        raw_frame = p1.stdout.read(frame_size)

        if len(raw_frame) != (frame_size):
            print('Error reading frame!!!')  # Break the loop in case of an error (too few bytes were read).
            continue

        # Convert the bytes read into a NumPy array, and reshape it to video frame dimensions
        yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((yuv_height, width))
        image_scale = 0.25
        yuv = cv2.resize(yuv, (0, 0), fx=image_scale, fy=image_scale)

        # Show video frame
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
        cv2.imshow('image', bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        p1.stdout.flush()

    # Wait one more second and terminate the sub-process
    try:
        p1.wait(1)
    except (sp.TimeoutExpired):
        p1.terminate()
