from cmath import log
import socketio
import os

sio = socketio.Client()


def send_log(line):
    sio.emit('send-log-line', {'line': line})


def disconnect():
    print('disconnected from server')


connection = False


AUTH_TOKEN = os.getenv("LOG_TOKEN")

if(not AUTH_TOKEN):
    print("Please set LOG_TOKEN environment variable")
    exit()


def log_to_server(line):
    global connection
    if(connection == False):
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


if __name__ == '__main__':
    socket_io_logger("Hello World")
