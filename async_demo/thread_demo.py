import time
import threading


def addNum():
    global num  # 在每个线程中都获取这个全局变量
    print('--get num:', num)
    time.sleep(1)
    lock.acquire()  # 修改数据前加锁
    num -= 1  # 对此公共变量进行-1操作
    lock.release()  # 修改后释放


num = 100  # 设定一个共享变量
thread_list = []
lock = threading.Lock()  # 生成全局锁
for i in range(100):
    t = threading.Thread(target=addNum)
    t.start()
    thread_list.append(t)

for t in thread_list:  # 等待所有线程执行完毕
    t.join()

print('final num:', num)