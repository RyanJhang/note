import cv2,os
import time
import numpy as np


class ErodeDilate:
    def __init__(self):
        self.kernel = self.init_mask()

    def init_mask(self):
        """mask for ErodeDilate # 遮罩

        Returns:
            {list} -- [5*5 block]
        """
        kernel = np.uint8(np.zeros((7, 7)))  # 3 5 7
        for x in range(7):
            kernel[x, 2] = 1
            kernel[2, x] = 1
        return kernel

    def erode_dilate(self, img):
        """erode and dilate

        Arguments:
            img {cv2.img} -- [description]

        Returns:
            result_img {cv2.img} -- through erode and dilate
        """
        # 膨脹
        img = cv2.dilate(img, self.kernel)
        # 侵蝕
        img = cv2.erode(img, self.kernel)

        return img


class ROI:
    def __init__(self):
        pass

    def roi(self, img, left_b=0.3, right_b=0.7, top_b=0.3, bottom_b=0.7):
        """Region of Interest

        Arguments:
            img {cv2.image} -- It's any img and read by cv2.imread

        Keyword Arguments:
            left_b {float} -- It's left bounding of result img (default: {0.3}) (value:[0:1])
            right_b {float} -- It's right bounding of result img (default: {0.7}) (value:[0:1])
            top_b {float} -- It's top bounding of result img (default: {0.3}) (value:[0:1])
            bottom_b {float} -- It's bottom bounding of result img (default: {0.7}) (value:[0:1])

        Returns:
            res {cv2.image} -- It's a captured img
        """

        # Region of Interest
        left = int(img.shape[0] * left_b)
        right = int(img.shape[0] * right_b)
        top = int(img.shape[1] * top_b)
        bottom = int(img.shape[1] * bottom_b)
        res = img[left:right, top:bottom]
        return res


class HSVDetect:
    def __init__(self):
        pass

    def hsv(self, img, lower, upper):
        """hsv detect

        Arguments:
            img {cv2.image} -- It's any img and read by cv2.imread
            lower {list} -- example:[h,s,v]
            upper {lsit} -- example:[h,s,v]
            showimg {bool} -- open hsv result or not

        Returns:
            res {cv2.image} -- result(assign color) img
            mask {cv2.image} -- mask(binary) img
        """

        # Convert BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # define range of color in HSV
        lower = np.array(lower)
        upper = np.array(upper)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower, upper)

        if lower[0] < 0:
            lower[0] = 180 + lower[0]
            upper[0] = 180
            lower = np.array(lower)
            upper = np.array(upper)

            mask2 = cv2.inRange(hsv, lower, upper)
            mask = mask + mask2

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(img, img, mask=mask)

        return res, mask


class FindContours:
    def __init__(self, img, lower_color, upper_color, ignore_area, error_img_path):
        """find contours

        Arguments:
            img {cv2.image} -- It's any img and read by cv2.imread
        """
        self.__img = img
        self.__findContours()
        self.lower_color = lower_color
        self.upper_color = upper_color
        self.ignore_area = ignore_area
        self.error_img_path = error_img_path

    def __findContours(self):
        """cv2.findContours
            # binary，它返回了你所處理的圖像
            # contours，正是我們要找的，輪廓的點集
            # hierarchy，各層輪廓的索引
            input is gray img
        """
        gray = cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)
        # ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        cv2.imshow("gray", gray)
        cv2.waitKey(1)
        contours, hierarchy = cv2.findContours(
            gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.__contours = contours

    def find_h(self, lower, upper):
        """detect height of contoures in range of lower and upper

        Keyword Arguments:
            lower {int} -- the lower height of contoures
            upper {int} -- the upper height of contoures

        Returns:
            int -- conform with lower and upper, if not only, raise
        """
        candidate_list = []
        #  choose by h or w
        for hier, points in enumerate(self.__contours):
            x, y, w, h = cv2.boundingRect(points)
            if w * h > self.ignore_area:
                candidate_list.append(h)

        if not candidate_list:
            raise Exception(0x03c81, "can not detect image fail")

        h = candidate_list[0]

        if len(candidate_list) != 1 or h > upper or h < lower:
            cv2.imwrite(self.error_img_path, self.__img)

            if len(candidate_list) != 1:
                raise Exception(0x03c82, "detect {} lines, please adjust light".format(len(candidate_list)))
            else:
                raise Exception(0x03c83, "line length is not expect, length:{}".format(h))

        return candidate_list[0]

    def find_w(self, lower, upper):
        """detect width of contoures in range of lower and upper

        Keyword Arguments:
            lower {int} -- the lower width of contoures
            upper {int} -- the upper width of contoures

        Returns:
            int -- conform with lower and upper, if not only, raise
        """
        candidate = []
        #  choose by h or w
        for hier, points in enumerate(self.__contours):
            x, y, w, h = cv2.boundingRect(points)
            if w * h > self.ignore_area:
                if upper > w > lower:
                    candidate.append(w)

        if len(candidate) != 1:
            path = 'error_img/find_w_error_{}.png'.format(
                time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
            cv2.imwrite(path, self.__img)
            raise Exception(0x03c84, "img {} {} is not detect interest object, object num = {}".format(self.lower_color, self.upper_color, len(candidate)))

        return candidate[0]


class ObjectDetect(ErodeDilate):
    def __init__(self, error_img_path, setting):
        self.error_img_path = error_img_path
        self.setting = setting
        ErodeDilate.__init__(self)

    def main(self, image_path):
        """
        Returns:
            [bool] -- detect True or False
            [int] -- the lengh of height or width
        """

        # Capture img
        frame = cv2.imread(image_path, 1)
        if frame is None:
            Exception('image is empty')

        # ROI
        roi_img = ROI.roi(self, frame,
                          float(self.setting["left"]),
                          float(self.setting["right"]),
                          float(self.setting["top"]),
                          float(self.setting["bottom"]))

        lower = [int(i) for i in self.setting["lower"]]
        upper = [int(i) for i in self.setting["upper"]]
        result_b, length = self.detect(roi_img, lower, upper, self.setting["mode"])

        k = cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()

        return result_b, length

    def detect(self, roi_img, lower_color, upper_color, switch):
        """detect h or w

        Arguments:
            roi_img {img} --
            lower_color {list} -- h,s,v lower
            upper_color {list} -- h,s,v upper
            switch {string} -- chooese "height" or "width" mode

        Returns:
            [bool] -- detect True or False
            [int] -- the lengh of height or width
        """

        # define range of blue color in HSV
        res, mask = HSVDetect.hsv(self, roi_img, lower_color, upper_color)

        # denoise
        res_erode_dilate = self.erode_dilate(res)
        # Find Contours
        fc = FindContours(res_erode_dilate, lower_color,
                          upper_color,
                          int(self.setting["ignore_area"]),
                          self.error_img_path
                          )

        if switch == "height":
            h = fc.find_h(int(self.setting["height_lower"]), int(
                self.setting["height_upper"]))
            return True, h

        elif switch == "width":
            w = fc.find_w(int(self.setting["width_lower"]), int(self.setting["width_upper"]))
            return True, w


def check_fov(image_path, error_img_path, setting):
    obj_detect = ObjectDetect(error_img_path, setting)
    result, length = obj_detect.main(image_path)
    if result == True:
        return


if __name__ == "__main__":
    setting = {
            "left": 0.3,
            "right": 0.7,
            "top": 0.3,
            "bottom": 0.7,
            "lower": [-10, 100, 100],
            "upper": [20, 255, 255],
            "mode": 'height',
            "height_lower": 50,
            "height_upper": 160,
            "width_lower": 0,
            "width_upper": 0,
            "ignore_area": 500,
        }
    filename = '[DBR224T00003].jpg'    
    image_path = os.path.join(os.path.dirname(__file__), filename)
    check_fov(image_path, os.path.dirname(__file__), setting)
