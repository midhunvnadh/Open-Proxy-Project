import requests
from time import sleep
import json


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


def servers():
    servers_list = []

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

    for provider in providers:
        try:
            print(
                f"[+] Fetching {provider['proto']} proxies from {provider['url']}"
            )
            req = requests.get(provider["url"]).text.split("\n")
            proto = provider["proto"]
            for proxy in req:
                servers_list.append(
                    json.dumps({
                        "proto": proto,
                        "url": f"{proto}://{proxy}"
                    })
                )
        except Exception as e:
            print("[!] Error occoured with provider!:")
            pass

    remove_duplicates_server_list = revert_json_list(
        remove_duplicates(servers_list))
    return remove_duplicates_server_list
