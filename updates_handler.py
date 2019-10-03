import threading, time
from datetime import timedelta


WAIT_TIME_SECONDS = 3


class PeriodicExecutor(threading.Thread):
    def __init__(self, interval_sec, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = True
        self.stopped = threading.Event()
        self.interval = timedelta(seconds=interval_sec)
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)


if __name__ == "__main__":
    def foo():
        print(time.ctime())
    job = PeriodicExecutor(interval_sec=WAIT_TIME_SECONDS, execute=foo)
    job.start()

    print('Start waiting')
    while True:
        time.sleep(2)
