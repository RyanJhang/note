from multiprocessing import Manager, Pool

m = Manager()
n = m.Value('d', 0.0)
lock = m.Lock()


def add_one():
    lock.acquire()
    n.value += 1
    lock.release()


with Pool(4) as pool:
    for _ in range(100):
        pool.apply_async(add_one, error_callback=lambda e: print(e))
    pool.close()
    pool.join()


print(n.value)