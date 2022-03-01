

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

    def __init__(self, p1: PointInt = PointInt(), p2: PointInt = PointInt(), y_val: float = 0):
        self.p1 = p1
        self.p2 = p2
        self.y_val = y_val


class Rectangles(list):
    __getattr__ = list.__getitem__

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

    rect_dicts = RectangleDict()

    for gap in range(0, interval_num, target_step):
        upper = Rectangle(p1=PointInt(x=(gap * width_interval),
                                      y=0),
                          p2=PointInt(x=(gap * width_interval + width_crop),
                                      y=height_crop))
        rect_dicts.upper.append(upper)
        lower = Rectangle(p1=PointInt(x=(gap * width_interval),
                                      y=(height - height_crop)),
                          p2=PointInt(x=(gap * width_interval + width_crop),
                                      y=height))
        rect_dicts.lower.append(lower)
        left = Rectangle(p1=PointInt(x=(width - width_crop),
                                     y=(gap * height_interval)),
                         p2=PointInt(x=width,
                                     y=(gap * height_interval + height_crop)))
        rect_dicts.left.append(left)
        right = Rectangle(p1=PointInt(x=0,
                                      y=(gap * height_interval)),
                          p2=PointInt(x=width_crop,
                                      y=(gap * height_interval + height_crop)))
        rect_dicts.right.append(right)

    rect_dicts.center = Rectangle(p1=PointInt(x=(width / 2 - width_crop / 2),
                                              y=(height / 2 - height_crop / 2)),
                                  p2=PointInt(x=(width / 2 + width_crop / 2),
                                              y=(height / 2 + height_crop / 2)))
    return rect_dicts


def calculate_y_of_roi(rect: Rectangle, image):
    img_crop = image[rect.p1.y:rect.p2.y, rect.p1.x:rect.p2.x]
    img_crop_y_frame = cv2.cvtColor(img_crop, cv2.COLOR_BGR2YUV)
    rect.y_val = np.mean(img_crop_y_frame[:, :, 0])


def draw_result(image, y_similarity_percent, rois: RectangleDict, right: Rectangle):
    height, width, _ = image.shape
    roi_y_percent = float(right.y_val / rois.center.y_val)
    if 1 or roi_y_percent <= y_similarity_percent:
        cv2.rectangle(image, (right.p1.x, right.p1.y), (right.p2.x, right.p2.y), (0, 0, 255), 2)
        text_p = (right.p1.x - 30 if right.p1.x + 30 > width else right.p1.x + 30,
                  right.p1.y - 30 if right.p1.y + 30 > height else right.p1.y + 30)
        cv2.putText(image, str(round(roi_y_percent, 2)), text_p, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)


if __name__ == "__main__":
    img_path = r"C:\Users\ryan.jhang\Documents\ryan\note\opencv\draw\[Source][FDL203V05386].jpg"
    image = cv2.imread(img_path)
    height, width, channels = image.shape

    y_similarity_percent = 80 / 100  # y相似度的百分比
    crop_per = 1 / 100  # CROP
    interval_num = 21  # 切幾次
    target_step = 2  # 目標的間格步數，2為 1 3 5 7，3為 1 4 7 11

    rois = get_roi(height, width, crop_per, interval_num, target_step)

    red_color = (0, 0, 255)  # BGR
    cv2.rectangle(image, (rois.center.p1.x, rois.center.p1.y), (rois.center.p2.x, rois.center.p2.y), red_color, 1)
    calculate_y_of_roi(rois.center, image)

    for index in range(len(rois.upper)):
        calculate_y_of_roi(rois.upper[index], image)
        calculate_y_of_roi(rois.lower[index], image)
        calculate_y_of_roi(rois.left[index], image)
        calculate_y_of_roi(rois.right[index], image)

        upper = Rectangle(**rois.upper[index])
        lower = Rectangle(**rois.lower[index])
        left = Rectangle(**rois.left[index])
        right = Rectangle(**rois.right[index])

        draw_result(image, y_similarity_percent, rois, upper)
        draw_result(image, y_similarity_percent, rois, lower)
        draw_result(image, y_similarity_percent, rois, left)
        draw_result(image, y_similarity_percent, rois, right)

    cv2.imwrite("Result.jpg", image)
    cv2.imshow('Result', image)
    cv2.waitKey(0)
