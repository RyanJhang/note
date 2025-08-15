from multiprocessing import Array, Process, Value


def increment_value(shared_int: Value):
    shared_int.value = shared_int.value + 1


def increment_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1


if __name__ == '__main__':
    integer = Value('i', 0)
    integer_array = Array('i', [0, 0])

    # 如果他们共同操作一个共享变量就会翻车（race condition)问题，这时候就需要使用Lock
    procs = [Process(target=increment_value, args=(integer,)),
             Process(target=increment_array, args=(integer_array,))]

    [p.start() for p in procs]
    [p.join() for p in procs]

    print(integer.value)
    print(integer_array[:])

