import threading
import json
from servers import servers
from test_server import test_server
from stats import stats
from speedtest import speedtest
from format_string import format_string


def update_servers(list, filename="servers.json"):
    if(len(list) == 0):
        raise Exception("No servers found!")
    servers = json.dumps(list)
    with open(filename, "w") as f:
        f.write(servers)
        f.close()


available_servers = []
proxies_length = 0
n_private_servers = 0


def test_availability(server):
    global available_servers, proxies_length, n_private_servers
    server_url = server["url"]
    private = False
    server_available = False
    data = {}
    server_added = False
    server_speed_rating = 0

    try:
        server_available, private, data = test_server(server_url)
        server["data"] = data
        server["private"] = private
    except Exception as e:
        print(e)
        pass
    finally:
        if(server_available):
            server_speed_rating = speedtest(server_url)
            server["speed_score"] = server_speed_rating
            if(server_speed_rating > 0):
                available_servers.append(server)
                server_added = True
                if private:
                    n_private_servers += 1
        proxies_length -= 1
        emoji = "[+]" if server_added else "[-]"

        print(
            f"{emoji}\t{format_string(server_url, 31)} \t [Speed Rating: {format_string(server_speed_rating, 3)}] \t\t [{format_string(proxies_length, 6)} Left]"
        )


def run_threads(threads):
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threads.clear()


def main():
    global servers_length, proxies_length
    servers_list = servers()
    proxies_length = len(servers_list)
    threads = []
    print("[+] Starting test...")

    for server in servers_list:
        t1 = threading.Thread(target=test_availability, args=(server, ))
        threads.append(t1)
        if(len(threads) >= 1000):
            run_threads(threads)
    run_threads(threads)

    update_servers(available_servers)


main()

stats(len(available_servers), n_private_servers)
