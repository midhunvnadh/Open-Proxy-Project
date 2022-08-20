from multiprocessing.connection import Listener
import socketio
import os

sio = socketio.Client()
address = ('localhost', 6000)
listener = Listener(address, authkey=b'password')
connection = False
AUTH_TOKEN = os.getenv("LOG_TOKEN")

if (not AUTH_TOKEN):
    print("Please set LOG_TOKEN environment variable")
    exit()


def send_log(line):
    sio.emit('send-log-line', {'line': line})


def log_to_server(line):
    global connection, sio
    if (connection == False):
        connection = sio.connect(
            'https://api.oproxy.ml',
            auth=('log', AUTH_TOKEN)
        )
        print('Connected to API Server')
    send_log(line)


def socket_io_logger(msg):
    try:
        log_to_server(msg)
    except Exception as e:
        print(e)
    print(msg)


def ipc_server():
    global listener
    conn = listener.accept()
    while True:
        msg = conn.recv()
        socket_io_logger(msg)
        if (msg == "end connection"):
            listener.close()
            break
