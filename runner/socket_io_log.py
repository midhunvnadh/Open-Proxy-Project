from cmath import log
import socketio

sio = socketio.Client()


def send_log(line):
    sio.emit('send-log-line', {'line': line})


def disconnect():
    print('disconnected from server')


connection = False


def log_to_server(line):
    global connection
    if(connection == False):
        connection = sio.connect(
            'https://api.oproxy.ml',
            auth=('log', 'token')
        )
        print('Connected to API Server')
    send_log(line)


def socket_io_logger(msg):
    try:
        log_to_server(msg)
    except Exception as e:
        print(e)
        exit()
    print(msg)


if __name__ == '__main__':
    socket_io_logger("Hello World")
