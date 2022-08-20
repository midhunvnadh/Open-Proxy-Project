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
    if(check_server_present(server)):
        print(
            f"\n\n\n[!] {server['url']} already present in the database\n\n\n"
        )
    else:
        servers.insert_one(server)


def test_availability(server):
    if(check_server_present(server)):
        return False

    server_url = server["url"]
    private = False
    server_available = False
    data = {}
    server_added = False
    server_speed_rating = 0

    retry = 3
    while(retry > 0):
        try:
            server_available, private, data = test_server(server_url)
            server["data"] = data
            server["private"] = private
            if(not data):
                break
            if(server_available):
                server_speed_rating = speedtest(server_url)
                server["speed_score"] = server_speed_rating
                if(server_speed_rating > 0):
                    server["available"] = True
                    server["updated_at"] = datetime.datetime.utcnow()
                    server["streak"] = 1
                    add_server_to_db(server)
                    server_added = True
            break
        except Exception as e:
            print(e)
            sleep(2 + randint(1, 3))
            retry -= 1

    emoji = "[+]" if server_added else "[-]"
    if server_added:
        line = (
            f"[Found  Update] {emoji}\t{format_string(server_url, 31)} \t [Speed Rating: {format_string(server_speed_rating, 3)}]"
        )
        logger(line)


def run_threads(threads):
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
        t.join()


def new_servers(threads_no=16, once=False):
    global client
    while True:
        try:
            client = mongo_client()
            servers_list = servers()
            threads = []
            i = 0

            for server in servers_list:
                i += 1
                t1 = threading.Thread(
                    target=test_availability, args=(server, )
                )
                threads.append(t1)
                if(len(threads) >= threads_no):
                    run_threads(threads)
                    threads.clear()

            run_threads(threads)
        except Exception as e:
            print(e)
            sleep(5)
        if(once):
            break
