import requests
from time import sleep
import json
import threading
from mongo_conn import mongo_client
from ipc_client import send_log as logger

servers_list = []
client = mongo_client()


def remove_duplicates(ls):
    new_list = list(set(ls))
    servers_list = servers_in_db()

    common_removed = remove_common(new_list, servers_list)
    no_of_common_removed = len(new_list) - len(common_removed)
    no_of_duplicates = len(ls) - len(new_list)

    if (no_of_duplicates > 0):
        logger(
            f"[!] Duplicates found in the list. Removed {no_of_duplicates} duplicates."
        )
    if (no_of_common_removed > 0):
        logger(
            f"[!] Commons found in the list. Removed {no_of_common_removed} commons."
        )

    return new_list


def remove_common(ls1, ls2):
    ls1 = [x for x in ls1 if x not in ls2]
    return ls1


def revert_json_list(json_list):
    return [json.loads(x) for x in json_list]


def servers_in_db():
    collection = client.servers
    servers = collection.servers
    available_servers = servers.aggregate([
        {
            "$project": {
                "proto": 1,
                "_id": 0,
                "url": 1
            }
        }
    ])
    return list([json.dumps(x) for x in available_servers])


def get_data(provider):
    try:
        req = requests.get(provider["url"]).text.split("\n")
        proto = provider["proto"]
        for proxy in req:
            servers_list.append(
                json.dumps({
                    'proto': proto,
                    'url': f'{provider["proto"]}://{proxy}'
                })
            )
        logger(
            f"[+] Fetched {provider['proto']} proxies from {provider['url']}"
        )
    except Exception as e:
        logger("[!] Error occoured with provider!:")


def servers():

    providers = []

    try:
        with open("providers.json", "r") as f:
            providers = json.load(f)
    except FileNotFoundError:
        logger("[!] No providers.json found.")
        sleep(10)
        exit()
    except Exception as e:
        logger(f"[!] Error: {e}")
        sleep(10)
        exit()

    threads = []
    for provider in providers:
        t1 = threading.Thread(
            target=get_data,
            args=(provider, )
        )
        threads.append(t1)

    for t in threads:
        t.start()
        sleep(0.2)
    for t in threads:
        t.join()
    threads.clear()

    remove_duplicates_server_list = revert_json_list(
        remove_duplicates(servers_list)
    )
    return remove_duplicates_server_list
