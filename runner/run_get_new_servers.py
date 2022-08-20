from curses import echo
from http import client
from random import randint
import threading
import datetime
from servers import servers
from test_server import test_server
from speedtest import speedtest
from format_string import format_string
from time import sleep
from mongo_conn import mongo_client
from mongo_conn import mongo_client
from ipc_client import send_log as logger


def check_server_present(server):
    collection = client.servers
    servers = collection.servers
    already_present = servers.count_documents({"url": server["url"]})
    return already_present > 0


def add_server_to_db(server):
    collection = client.servers
    servers = collection.servers
    if (check_server_present(server)):
        logger(
            f"\n\n\n[!] {server['url']} already present in the database\n\n\n"
        )
    else:
        servers.insert_one(server)


def test_availability(server):
    global total_servers
    server_url = server["url"]
    private = False
    server_available = False
    data = {}
    server_added = False
    server_speed_rating = 0

    retry_count = retry = 3
    while (retry > 0):
        try:
            server_available, private, data = test_server(server_url)
            server["data"] = data
            server["private"] = private
            if (server_available):
                if (not data):
                    break
                server_speed_rating = speedtest(server_url)
                server["speed_score"] = server_speed_rating
                if (server_speed_rating > 0):
                    server["available"] = True
                    server["updated_at"] = datetime.datetime.utcnow()
                    server["streak"] = 1
                    add_server_to_db(server)
                    server_added = True
            if (server_added):
                break
            else:
                retry -= 1
        except Exception as e:
            logger(f"[!] Error occoured on {server_url}")
            retry -= 1
            sleep(2 + randint(1, 3))

    emoji = "[+]" if server_added else "[-]"
    total_servers -= 1
    if (server_added):
        logger(
            f"[Found  Update] {emoji}\t Try({retry_count - retry}) \t {format_string(server_url, 31)} \t [Speed Rating: {format_string(server_speed_rating, 3)}] \t {format_string(total_servers, 6)} Left"
        )


def run_threads(threads):
    for t in threads:
        #t.daemon = True
        t.start()
    for t in threads:
        t.join()


total_servers = 0


def new_servers(threads_no=16, once=False):
    global client, total_servers
    while True:
        try:
            client = mongo_client()
            servers_list = servers()
            total_servers = len(servers_list)
            threads = []
            i = 0

            for server in servers_list:
                i += 1
                t1 = threading.Thread(
                    target=test_availability, args=(server, )
                )
                threads.append(t1)
                if (len(threads) >= threads_no):
                    run_threads(threads)
                    threads.clear()

            run_threads(threads)
        except Exception as e:
            print(e)
            sleep(5)
        if (once):
            print("Done")
            break
