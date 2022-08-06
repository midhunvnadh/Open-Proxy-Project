from logging import PercentStyle
import requests
import time


def speedtest(proxy_server_url):
    url = 'https://raw.githubusercontent.com/jamesward/play-load-tests/master/public/1mb.txt'
    proxies = {
        'https': proxy_server_url,
        'http': proxy_server_url
    }
    time_diff = 0
    try:
        time_start = time.time()
        r = requests.get(url, proxies=proxies, timeout=30)
        time_end = time.time()
        time_diff = time_end - time_start
    except Exception as e:
        pass
    if(time_diff > 0):
        kbps = float(1024/time_diff)
        percent = (kbps/1024) * 100
        return int(percent)
    else:
        return 0
