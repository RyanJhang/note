
import socket
import time
import matplotlib.pyplot as plt
import numpy as np
import time
from math import *
import matplotlib.pyplot as plt


def get_w05_data(s):
    while True:
        data = "RD W05.U\r\n"
        send_data = data.encode()
        # print(send_data)
        s.send(send_data)

        # delay
        time.sleep(0.001)

        indata = s.recv(16)
        result = (int(indata.decode().replace("\r\n", "")))
        # print(result)
        if result != 9999:
            return result 


if __name__ == '__main__':

    HOST = '172.19.16.183'
    PORT = 8501
# --------------------------------------

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((HOST, PORT))
    # get_w05_data(s)
    # s.close()
# --------------------------------------

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    count = 200
    plt.ion()  # 开启interactive mode 成功的关键函数
    plt.figure(1)
    t = np.arange(count)
    result = []
    for i in t:
        # plt.clf() # 清空画布上的所有内容。此处不能调用此函数，不然之前画出的轨迹，将会被清空。
        # y = np.sin(t*i/10.0)
        # print(y)
        result.append(get_w05_data(s))
        plt.plot(t[0:i + 1], result)  # 一条轨迹
        # plt.draw()  # 注意此函数需要调用
        # time.sleep(0.1)
        plt.pause(0.01)

    s.close()

    max_value = max(result)
    max_index = result.index(max_value)
    plt.plot(max_index, max_value, 'ks')
    show_max = f"[{max_index}, {max_value}]"
    plt.annotate(show_max, xytext=(max_index, max_value), xy=(max_index, max_value))

    min_value = min(result)
    min_index = result.index(min_value)
    plt.plot(min_index, min_value, 'gs')
    show_min = f"[{min_index}, {min_value}]"
    plt.annotate(show_min, xytext=(min_index, min_value), xy=(min_index, min_value))

    print(f"AVG:{(sum(result) / len(result))}")
    print(t, result)
    plt.pause(10000)
    # x = range(0,101)
    # y = result

    # plt.plot(x,y)
    # plt.show()
