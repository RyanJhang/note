from multiprocessing import Pool, Value, get_start_method, set_start_method



def add_one():
    with num.get_lock():
        num.value += 1


num = Value('d', 0.0)


with Pool(4) as pool:
    for _ in range(100):
        pool.apply_async(add_one, error_callback=lambda e: print(e))
    pool.close()
    pool.join()


print(num.value)