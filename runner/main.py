from asyncio import threads
from concurrent.futures import process
from zoneinfo import available_timezones
from run_get_new_servers import new_servers
from run_update_servers import update_servers
import sys
import multiprocessing as mp
import argparse


def args():
    parser = argparse.ArgumentParser(description='Run Open Proxy Updater')
    parser.add_argument('--threads', metavar='N', type=int, default=12)
    parser.add_argument('--once', action="store_true")
    parsed = parser.parse_args()

    threads_no, once = parsed.threads, parsed.once

    return threads_no, once


threads_no, once = args()

process = [
    mp.Process(target=new_servers, args=(threads_no, once, )),
    #mp.Process(target=update_servers, args=(True, threads_no, once, )),
    #mp.Process(target=update_servers, args=(False, threads_no, once, )),
]

if __name__ == '__main__':
    mp.set_start_method('spawn')
    for p in process:
        p.start()
    for p in process:
        p.join()
