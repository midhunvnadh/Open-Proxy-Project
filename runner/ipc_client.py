from multiprocessing.connection import Client

address = ('localhost', 6000)

conn = False


def send_log(msg):
    global conn
    try:
        if (conn == False):
            conn = Client(address, authkey=b'password')
        conn.send(msg)
    except Exception as E:
        print(E)
        pass
