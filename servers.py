import requests
from time import sleep
import json


def remove_duplicates(list):
    new_list = [
        i for n,
        i in enumerate(list)
        if i not in list[:n]
    ]

    if(len(list) != len(new_list)):
        no_of_duplicates = len(list) - len(new_list)
        print(
            f"[!] Duplicates found in the list. Removed {no_of_duplicates} duplicates."
        )

    return new_list


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
                    {
                        "proto": proto,
                        "url": f"{proto}://{proxy}"
                    }
                )
        except Exception as e:
            print("[!] Error occoured with provider!:")
            pass

    remove_duplicates_server_list = remove_duplicates(servers_list)
    return remove_duplicates_server_list
