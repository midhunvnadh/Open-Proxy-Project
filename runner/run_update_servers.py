from mongo_conn import mongo_client
from time import sleep
from test_server import test_server
from speedtest import speedtest
from random import randint
from format_string import format_string
import datetime
import threading


def update_server_in_db(server):
    id = server["_id"]
    collection = client.servers
    servers = collection.servers
    servers.update_one({"_id": id}, {"$set": server})


def test_availability(server):
    server_url = server["url"]
    private = False
    server_available = False
    data = {}
    server_added = False
    server_speed_rating = 0

    retry = 3
    streak = server["streak"] if "streak" in server else 0
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
                    server["streak"] = (streak + 1) if streak < 100 else 100
                    server_added = True
                else:
                    server["available"] = False
                    server["updated_at"] = datetime.datetime.utcnow()
                    server["streak"] = 0
            else:
                server["available"] = False
                server["updated_at"] = datetime.datetime.utcnow()
                server["streak"] = 0
            update_server_in_db(server)
            break
        except Exception as e:
            print(e)
            sleep(2 + randint(1, 3))
            retry -= 1

    emoji = "[+]" if server_added else "[-]"
    print(
        f"[Status Update] {emoji}\t{format_string(server_url, 31)} \t [Speed Rating: {format_string(server_speed_rating, 3)}]"
    )


def servers(available=True):
    collection = client.servers
    servers = collection.servers
    available_servers = servers.find({"available": available})
    return available_servers


def run_threads(threads):
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
        t.join()


def update_servers(available=True, threads_no=16, once=False):
    global client
    while True:
        threads = []
        try:
            client = mongo_client()
            available_servers = servers(available)
            for server in available_servers:
                t1 = threading.Thread(
                    target=test_availability,
                    args=(server,)
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
