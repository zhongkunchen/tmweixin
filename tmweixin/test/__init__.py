#!coding: utf-8
__author__ = 'zkchen'
from multiprocessing import Process
import os
import time


def sleeper(name, seconds):
    print("Process ID# %s and parent ID#%s" % (os.getpid(), os.getppid()))
    print("%s will sleep %s seconds" % (name, seconds))
    for i in range(seconds):
        print("%s =>%s" % (name, i))
        time.sleep(1)
    print("%s done" % name)


if __name__ == "__main__":
    child_proc1 = Process(target=sleeper, args=("sss", 5))
    child_proc2 = Process(target=sleeper, args=("kkk", 4))
    child_proc3 = Process(target=sleeper, args=("yyy", 3))
    child_proc1.start()
    child_proc2.start()
    child_proc1.join()
    child_proc2.join()
    child_proc3.start()
    child_proc3.join(2)
    print("main done..")
