

import cv2
import numpy as np


class PointInt(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)


class Rectangle(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, p1: PointInt = PointInt(), p2: PointInt = PointInt()):
        self.p1 = p1
        self.p2 = p2


class Rectangles(list):

    def __init__(self):
        # 應規範，子類重寫父類方法的時候__init__初始化函式中要呼叫父類的__init__初始化函式
        super(Rectangles, self).__init__()
        self.data_type = Rectangle

    def append(self, obj):
        '''
        重寫父類的append方法
        :param obj: 是要儲存的元素
        :return: None
        '''
        if isinstance(obj, self.data_type):
            super(Rectangles, self).append(obj)  # 這裡需要訪問父類的append 方法來完成真正的儲存操作
        else:
            print(f"非指定型別{self.data_type}！")


class RectangleDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self):
        self.upper = Rectangles()
        self.lower = Rectangles()
        self.left = Rectangles()
        self.right = Rectangles()
        self.center = Rectangle()


def get_roi(height, width, crop_per, interval_num, target_step) -> RectangleDict:
    width_crop = int(width * crop_per)
    height_crop = int(height * crop_per)

    width_interval = (width - width_crop) / (interval_num - 1)
    height_interval = (height - height_crop) / (interval_num - 1)

    re_dict = RectangleDict()

    for gap in range(0, interval_num, target_step):
        upper = Rectangle(p1=PointInt(x=(gap * width_interval),
                                      y=0),
                          p2=PointInt(x=(gap * width_interval + width_crop),
                                      y=height_crop))
        re_dict.upper.append(upper)
        lower = Rectangle(p1=PointInt(x=(gap * width_interval),
                                      y=(height - height_crop)),
                          p2=PointInt(x=(gap * width_interval + width_crop),
                                      y=height))
        re_dict.lower.append(lower)
        left = Rectangle(p1=PointInt(x=(width - width_crop),
                                     y=(gap * height_interval)),
                         p2=PointInt(x=width,
                                     y=(gap * height_interval + height_crop)))
        re_dict.left.append(left)
        right = Rectangle(p1=PointInt(x=0,
                                      y=(gap * height_interval)),
                          p2=PointInt(x=width_crop,
                                      y=(gap * height_interval + height_crop)))
        re_dict.right.append(right)

    re_dict.center = Rectangle(p1=PointInt(x=(width / 2 - width_crop / 2),
                                           y=(height / 2 - height_crop / 2)),
                               p2=PointInt(x=(width / 2 + width_crop / 2),
                                           y=(height / 2 + height_crop / 2)))
    return re_dict


if __name__ == "__main__":
    height = 500
    width = 500

    crop_per = 5 / 100  # CROP
    interval_num = 21  # 切幾次
    target_step = 2  # 目標的間格步數，2為 1 3 5 7，3為 1 4 7 11

    re_dict = get_roi(height, width, crop_per, interval_num, target_step)

    # Create a blank 640x480 black image
    image = np.zeros((height, width, 3), np.uint8)
    # Fill image with gray color(set each pixel to gray)
    image[:] = (128, 128, 128)

    cv2.rectangle(image, (re_dict.center.p1.x, re_dict.center.p1.y), (re_dict.center.p2.x, re_dict.center.p2.y), (0, 0, 255), 2)
    roi_y_val = {}

    red_color = (0, 0, 255)  # BGR
    for index in range(len(re_dict.lower)):
        upper = Rectangle(**re_dict.upper[index])
        lower = Rectangle(**re_dict.lower[index])
        left = Rectangle(**re_dict.left[index])
        right = Rectangle(**re_dict.right[index])

        cv2.rectangle(image, (upper.p1.x, upper.p1.y), (upper.p2.x, upper.p2.y), (0, 255, 0), 2)
        cv2.rectangle(image, (lower.p1.x, lower.p1.y), (lower.p2.x, lower.p2.y), (255, 255, 0), 2)
        cv2.rectangle(image, (left.p1.x, left.p1.y), (left.p2.x, left.p2.y), (255, 0, 0), 2)
        cv2.rectangle(image, (right.p1.x, right.p1.y), (right.p2.x, right.p2.y), (0, 0, 0), 2)

    cv2.imshow('Result', image)
    cv2.waitKey(0)
