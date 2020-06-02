# https://www.cloudcity.io/blog/2019/02/27/things-i-wish-they-told-me-about-multiprocessing-in-python/
import time
import multiprocessing as mp


class TimerProcWorker(object):
    INTERVAL_SECS = 30
    MAX_SLEEP_SECS = 1

    def __init__(self, stop_event, name: str):
        self.stop_event = stop_event
        self.name = name

    def main_loop(self):
        next_time = int(time.time() + self.INTERVAL_SECS)
        print(f"next_time={next_time}")
        while not self.stop_event.is_set():
            sleep_secs = max(0, min(next_time - time.time(), self.MAX_SLEEP_SECS))
            time.sleep(sleep_secs)
            if int(time.time()) == next_time:
                print("TIMER EVENT")
                next_time = int(time.time() + self.INTERVAL_SECS)
            


if __name__ == "__main__":
    stop_event = mp.Event()
    worker = TimerProcWorker(stop_event, "timer-worker")
    proc = mp.Process(target=worker.main_loop, args=())
    proc.start()
