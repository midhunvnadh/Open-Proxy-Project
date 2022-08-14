import requests
import time
from func_timeout import func_set_timeout, func_timeout

timeout = 10


@func_set_timeout(timeout)
def speed(url, proxies):
    time_diff = 0
    try:
        time_start = time.time()
        r = requests.get(url, proxies=proxies, timeout=timeout)
        time_end = time.time()
        time_diff = time_end - time_start
        if(time_diff < 1 and time_diff > 0):
            time_diff = 1
    except Exception as e:
        pass
    return time_diff


def speedtest(proxy_server_url):
    url = 'https://raw.githubusercontent.com/jamesward/play-load-tests/master/public/1mb.txt'
    proxies = {
        'https': proxy_server_url,
        'http': proxy_server_url
    }

    time_diff = 0
    retry = 3

    while(retry > 0):
        try:
            time_diff = speed(url, proxies)
            break
        except:
            time.sleep(2)
            retry -= 1

    if(time_diff > 0):
        kbps = float(1024/time_diff)
        percent = (kbps/1024) * 100
        return int(percent)
    else:
        return 0
