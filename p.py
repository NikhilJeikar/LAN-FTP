from _thread import start_new_thread
import time


def fun1():
    while True:
        time.sleep(2)
        print(1)


def fun2():
    start_new_thread(fun1, ())
    print(2)
    a


start_new_thread(fun2,())

while True:
    time.sleep(2)
    print(3)
