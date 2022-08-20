from run_get_new_servers import new_servers
from run_update_servers import update_servers
from ipc_server import ipc_server

from time import sleep

import threading as td
import argparse


def args():
    parser = argparse.ArgumentParser(description='Run Open Proxy Updater')
    parser.add_argument('--threads', metavar='N', type=int, default=5)
    parser.add_argument('--once', action="store_true")
    parsed = parser.parse_args()

    threads_no, once = parsed.threads, parsed.once

    return threads_no, once


threads_no, once = args()

threads = [
    td.Thread(target=ipc_server, args=()),
    td.Thread(target=new_servers, args=(threads_no, once, )),
    #td.Thread(target=update_servers, args=(True, threads_no, once, )),
    #td.Thread(target=update_servers, args=(False, threads_no, once, )),
]

if __name__ == '__main__':
    for t in threads:
        t.start()
        sleep(2)
    for t in threads:
        t.join()
