from hashlib import new
import requests
import re


def get_private_filter(privacy):
    return privacy["vpn"] == False and privacy["proxy"] == False and privacy["tor"] == False and privacy["hosting"] == False


def test_server(server_url):
    available = False
    private = False
    data = {}
    try:
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', server_url)[0]
        r = requests.get(
            f"https://ipinfo.io/widget/demo/{ip}",
            proxies={
                "http": server_url,
                "https": server_url,
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "referer": "https://ipinfo.io/"
            },
            timeout=3
        )
        r = r.json()
        data = r["data"]
        country_code = data["country"]
        privacy = data["privacy"]
        private = get_private_filter(privacy)
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
        print(e)
        raise Exception("Some error occoured!")
    finally:
        return available, private, data
