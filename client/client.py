import socket

import read_csv
import config

class SendEmgmt:
    def __init__(self, host, port, measurement):
        self.host = host
        self.port = port
        self.measurement = measurement

    def send(self, table):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
                msg = 'msg'
                s.connect((self.host, self.port))
                s.sendall(msg.encode('utf-8'))
                recv_msg = s.recv(4096)
                print(recv_msg + '\n ##############################################')


if __name__ == '__main__':
    host = config.host
    port = config.port
    measurement = config.