# https://pymotw.com/3/multiprocessing/basics.html
# https://docs.python.org/zh-cn/3.7/library/multiprocessing.html

import logging
import os
import time
import multiprocessing as mp
# mp.set_start_method("spawn", True)

FORMAT = '%(asctime)s - %(process)d - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%y%m%d %H:%M:%S.%s')
logger = logging.getLogger('myserver')


def worker(num):
    """worker function"""
    logger.debug(f'name={mp.current_process().name}, pid={mp.current_process().pid}')
    time.sleep(100)
    logger.warning(f"pid-{mp.current_process().pid} exist")


if __name__ == '__main__':
    jobs = []
    count = int(os.getenv("PROCESSES", 5))
    logger.warning(f"PROCESSES = {count}, boss.pid = {mp.current_process().pid}")
    for i in range(count):
        p = mp.Process(name=f'myprocess-worker-{i}', target=worker, args=(i,))
        jobs.append(p)
        p.start()

    for j in jobs:
        p.join()
        logger.info(f"exit code: {j.exitcode}")
