from hashlib import new
from time import sleep
import requests
import re
from random import randint


def get_private_filter(server):
    privacy = server["privacy"]
    return privacy["vpn"] == False and privacy["proxy"] == False and server["asn"]["type"] != "hosting"


def test_server(server_url):
    available = False
    private = False
    data = {}
    server_url = server_url.strip()
    retry = 4
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', server_url)
    while(retry > 0):
        try:
            r = requests.get(
                f"https://ipinfo.io/widget/demo/{ip[0]}",
                proxies={
                    "http": server_url,
                    "https": server_url,
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                    "referer": "https://ipinfo.io/"
                },
                timeout=5
            )
            r = r.json()
            data = r["data"]
            country_code = data["country"]
            privacy = data["privacy"]
            private = get_private_filter(data)
            available, private, data = True, private, data
            break
        except requests.exceptions.Timeout as e:
            retry -= 1
        except requests.exceptions.ProxyError as e:
            break
        except requests.exceptions.SSLError as e:
            break
        except requests.exceptions.InvalidHeader as e:
            break
        except requests.exceptions.ConnectionError as e:
            retry -= 1
        except requests.exceptions.JSONDecodeError as e:
            break
        except Exception as e:
            retry -= 1
            print(e)
            raise Exception(f"Some error occoured! {server_url}")
        sleep(2 + randint(1, 3))
    return available, private, data
