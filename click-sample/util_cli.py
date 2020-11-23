# https://docs.python.org/zh-cn/3/library/subprocess.html
import logging
import subprocess


def run(cmd, verbose=True) -> None:
    """Run Command, use stdout as output"""
    if verbose:
        logging.debug(cmd)
    subprocess.run(args=cmd, shell=True, check=True)
