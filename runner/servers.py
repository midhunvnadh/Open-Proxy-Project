import requests
from time import sleep
import json
import threading


def remove_duplicates(ls):
    new_list = list(set(ls))

    no_of_duplicates = len(ls) - len(new_list)
    if(no_of_duplicates > 0):
        print(
            f"[!] Duplicates found in the list. Removed {no_of_duplicates} duplicates."
        )

    return new_list


def revert_json_list(json_list):
    return [json.loads(x) for x in json_list]


servers_list = []


def get_data(provider):
    try:
        req = requests.get(provider["url"]).text.split("\n")
        proto = provider["proto"]
        for proxy in req:
            servers_list.append(
                json.dumps({
                    "proto": proto,
                    "url": f"{provider['proto']}://{proxy}"
                })
            )
        print(
            f"[+] Fetched {provider['proto']} proxies from {provider['url']}"
        )
    except Exception as e:
        print("[!] Error occoured with provider!:")


def servers():

    providers = []

    try:
        with open("providers.json", "r") as f:
            providers = json.load(f)
    except FileNotFoundError:
        print("[!] No providers.json found.")
        sleep(10)
        exit()
    except Exception as e:
        print(f"[!] Error: {e}")
        sleep(10)
        exit()

    threads = []
    for provider in providers:
        t1 = threading.Thread(
            target=get_data, args=(provider, ))
        threads.append(t1)

    for t in threads:
        t.start()
        sleep(0.2)
    for t in threads:
        t.join()
    threads.clear()

    remove_duplicates_server_list = revert_json_list(
        remove_duplicates(servers_list))
    return remove_duplicates_server_list
