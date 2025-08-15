# SuperFastPython.com
# example of an attempted race condition with a shared variable
from multiprocessing import Process, cpu_count, set_start_method
from time import sleep

a = cpu_count()
# make additions into the global variable
def adder(amount, repeats):
    global value
    value = 0
    for _ in range(repeats):
        # copy the value
        tmp = value
        # suggest a context switch
        sleep(0)
        # change the copy
        tmp = tmp + amount
        # suggest a context switch
        sleep(0)
        # copy the value back
        value = tmp
 
# make subtractions from the global variable
def subtractor(amount, repeats):
    global value
    value = 0
    for _ in range(repeats):
        # copy the value
        tmp = value
        # suggest a context switch
        sleep(0)
        # change the copy
        tmp = tmp - amount
        # suggest a context switch
        sleep(0)
        # copy the value back
        value = tmp

if __name__ == '__main__':
    # set start method
    # set_start_method('fork')
    # define the global variable
    global value
    value = 0
    # start a thread making additions
    adder_thread = Process(target=adder, args=(1, 1000000))
    adder_thread.start()
    # start a thread making subtractions
    subtractor_thread = Process(target=subtractor, args=(1, 1000000))
    subtractor_thread.start()
    # wait for both processes to finish
    print('Waiting for processes to finish...')
    adder_thread.join()
    # subtractor_thread.join()
    # report the value
    print(f'Value: {value}')