

import os
import json,random
import time

import socket
from smb.SMBConnection import SMBConnection

import threading
import time


def read_info(__file__):
    folder_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(folder_path, "connection_info.json")

    with open(json_path) as f:
        data = json.load(f)
    return data


def connect_smb(connect_info, TH="0"):
    host = connect_info['ip']  # ip或域名
    username = connect_info['username']
    password = connect_info['password']
    service_name = connect_info['service_name']
    path = connect_info['dst_path']

    start_time = time.time()
    print("準備連線", start_time)
    conn = SMBConnection(username, password, socket.gethostname(), "ntp_user", is_direct_tcp=True)
    result = conn.connect(host, 445)
    print("登錄成功")

    files = conn.listPath(service_name, path)
    # file_names = []
    # for file in files:
    #     if file.filename not in [os.curdir, os.pardir]:
    file = files.pop(random.randint(2,len(files)-1))
    filename = file.filename
    print(filename)
    old_path = os.path.join(path, filename)
    new_path = os.path.join(path, filename + TH)
    conn.rename(service_name, old_path, new_path, timeout=30)
    # print(file_names)
    conn.close()
    duration_time = time.time() - start_time
    print("關閉連線成功", duration_time)


if __name__ == '__main__':
    info = read_info(__file__)
    connect_info = info["FACTORY_DELTA"]
    connect_smb(connect_info)

    threads = []
    for i in range(5):
        threads.append(threading.Thread(target=connect_smb, args=(connect_info, str(i),)))
        threads[i].start()

    # 等待所有子執行緒結束
    for i in range(5):
        threads[i].join()

    print("Done.")
