import threading, time
from multiprocessing import Process


WAIT_TIME_SECONDS = 2


class Timer:
    def __init__(self):
        self.wait_time_sec = 5

    def _on_forecast_update(self):
        print(time.ctime())

    def start(self):
        ticker = threading.Event()
        while not ticker.wait(WAIT_TIME_SECONDS):
            self._on_forecast_update()


timer = Timer()
timer.start()

# def foo():
#     print(time.ctime())
#
# ticker = threading.Event()
# while not ticker.wait(WAIT_TIME_SECONDS):
#     foo()
