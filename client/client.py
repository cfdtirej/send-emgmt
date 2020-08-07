import socket

import client.read_csv as read_csv
import client.config as config


class SendEmgmt:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, latest_file, prev_file):
        csv_diff = read_csv.get_csv_diff(latest_file, prev_file) # dictionary type
        column = csv_diff[0][1:]
        time = []
        for i in range(len(csv_diff)):
            time.append(csv_diff[i][0])
        count = 0
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                influx_json = [
                    {
                        'measurement': 'measurement',
                        'tags': {
                            'type': 'tag value'
                        },
                        'time': time[count],
                        'fields': dict(zip(column, csv_diff[count][1:]))
                    }
                ]
                msg = 'msg'
                client.connect((self.host, self.port))
                client.sendall(msg.encode('utf-8'))
                recv_msg = client.recv(4096)
                print('#---Server message---#\n{}'.format(recv_msg))
                count += 1
                if count == len(csv_diff):
                    break


if __name__ == '__main__':
    host = config.host
    port = config.port