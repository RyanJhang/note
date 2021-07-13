
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
        # time.sleep(0.001)

        indata = s.recv(16)
        result = (int(indata.decode().replace("\r\n", "")))
        # print(result)
        if result != 9999:
            return result 



def draw_point(i, curr_dist, icon):
    plt.plot(i, curr_dist, icon)
    # show_max = f"{icon}\n[{i}, {curr_dist}]"
    # plt.annotate(show_max, xytext=(i, curr_dist), xy=(i, curr_dist))


if __name__ == '__main__':

    HOST = '192.168.1.10'
    PORT = 8501
# --------------------------------------

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((HOST, PORT))
    # get_w05_data(s)
    # s.close()
# --------------------------------------

    h_dist_th = 600
    l_dist_th = 500

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # 擷取頻率 1/1000 秒
    count = 30
    avg_count = 1
    t = np.arange(count)

    plt.ion()  # 开启interactive mode 成功的关键函数
    plt.figure(1)
    plt.plot(t, [h_dist_th] * int(count/avg_count), color='r', label="h_dist_th")
    plt.plot(t, [l_dist_th] * int(count/avg_count), color='b', label="l_dist_th")
    plt.legend(loc="best", fontsize=20)
    
    result = []
    for i in t:
        curr_dist = get_w05_data(s)
        result.append(curr_dist)

        if avg_count == 1:
            plt.plot(t[0:i + 1], result, color='g')  # 一条轨迹
        else:
            if i % 5 == 0 and i != 0:
                plt.plot(i, np.mean(result[i-4:i]), color='g')  # 一条轨迹

        if curr_dist > h_dist_th:
            icon = 'rs'
            draw_point(i, curr_dist, icon)
        elif curr_dist < l_dist_th:
            icon = 'bs'
            draw_point(i, curr_dist, icon)

        # plt.draw()  # 注意此函数需要调用
        # time.sleep(0.1)
        plt.pause(0.1)

    s.close()

    # max_value = max(result)
    # max_index = result.index(max_value)
    # plt.plot(max_index, max_value, 'ks')
    # show_max = f"[{max_index}, {max_value}]"
    # plt.annotate(show_max, xytext=(max_index, max_value), xy=(max_index, max_value))

    # min_value = min(result)
    # min_index = result.index(min_value)
    # plt.plot(min_index, min_value, 'gs')
    # show_min = f"[{min_index}, {min_value}]"
    # plt.annotate(show_min, xytext=(min_index, min_value), xy=(min_index, min_value))

    print(f"AVG:{(sum(result) / len(result))}")
    print(t, result)
    plt.pause(100)
    # x = range(0,101)
    # y = result

    # plt.plot(x,y)
    # plt.show()
