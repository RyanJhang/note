import multiprocessing
import os

from LogExporter import LogExporter


def worker(log):
    # logggg = LogExporter({},{},i)
    # print(logggg.log)

    log.info(str(os.getpid()) + " --- " + "1Logging...")
    log.info(str(os.getpid()) + " --- " + "2Logging...")
    log.info(str(os.getpid()) + " --- " + "3Logging...")
    log.debug(str(os.getpid()) + " --- " + "debug...")
    log.debug(str(os.getpid()) + " --- " + "debug...")
    log.debug(str(os.getpid()) + " --- " + "debug...")
    print('log id = ',id(log))


if __name__ == "__main__":
    procs=[]
    for i in range(5):
        processes = multiprocessing.Process(target=worker(LogExporter({},{},i)))

        procs.append(processes)

    for p in procs:
        p.start()

    for p in procs:
        p.join()


