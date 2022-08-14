from concurrent.futures import process
import multiprocessing as mp
from zoneinfo import available_timezones

from run_get_new_servers import new_servers
from run_update_servers import update_servers

process = [
    mp.Process(target=new_servers, args=()),
    mp.Process(target=update_servers, args=(True,)),
    mp.Process(target=update_servers, args=(False,)),
]

if __name__ == '__main__':
    mp.set_start_method('spawn')
    for p in process:
        p.start()
    for p in process:
        p.join()
