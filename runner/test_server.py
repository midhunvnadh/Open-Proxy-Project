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
    ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', server_url)
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
    except requests.exceptions.Timeout as e:
        pass
    except requests.exceptions.ProxyError as e:
        pass
    except requests.exceptions.SSLError as e:
        pass
    except requests.exceptions.InvalidHeader as e:
        pass
    except requests.exceptions.ConnectionError as e:
        pass
    except requests.exceptions.JSONDecodeError as e:
        pass
    except Exception as e:
        raise Exception(f"Some error occoured! {server_url}")
    return available, private, data
