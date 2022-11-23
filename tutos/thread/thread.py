
import utime
import _thread

def core1():
    while True:
        print("Thread 1")
        utime.sleep(1)

def core0():
    while True:
        print("Thread 2")
        utime.sleep(3)

threadID = _thread.start_new_thread(core1, ())
core0()