import threading
import json
from servers import servers
from test_server import test_server
from stats import stats


def update_servers(list, filename="servers.json"):
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

    try:
        server_available, private, data = test_server(server_url)
        server["data"] = data
        server["private"] = private
        if private:
            n_private_servers += 1
    except Exception as e:
        print(e)
        pass
    finally:
        if(server_available):
            available_servers.append(server)
        proxies_length -= 1
        emoji = "[+]" if server_available else "[-]"

        print(f"{emoji}\t{server_url} \t\t\t [{proxies_length} Left]")


def main():
    global servers_length, proxies_length
    servers_list = servers()
    proxies_length = len(servers_list)
    threads = []
    print("[+] Starting test...")
    for server in servers_list:
        t1 = threading.Thread(target=test_availability, args=(server, ))
        threads.append(t1)
        if(len(threads) >= 50):
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            threads.clear()
    update_servers(available_servers)


main()

stats(len(available_servers), n_private_servers)
