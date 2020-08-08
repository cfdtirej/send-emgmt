import socket
import json
import time

import csv_processing
import config

class SendEmgmt:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def emgmt_client(self, latest_file, prev_file):
        csv_diff = csv_processing.get_csv_diff(latest_file, prev_file)
        column = csv_diff[0][1:]
        times_list = []
        for i in range(len(csv_diff)-1):
            times_list.append(csv_diff[i][0])
        count = 0
        while True:
            if count > 0:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    data = {
                        'measurement': 'measurement',
                        'tags': {
                            'type': 'tag value'
                        },
                        'time': times_list[count],
                        'fields': dict(zip(column, csv_diff[count][1:]))
                    }
                    if csv_diff[count][1:] is None:
                        break
                    send_json = json.dumps(data)
                    s.connect((self.host, self.port))
                    s.sendall(send_json.encode('utf-8'))
                    recv_msg = s.recv(4096)
                    print('#---Server message---#\n{}'.format(recv_msg))
            count += 1
            if count == len(csv_diff) - 1:
                break


if __name__ == '__main__':
    host = config.host
    port = config.port
    latest_file = config.latest_path['dc']
    prev_file = config.prev_path['dc']
    dc = SendEmgmt(host, port)
    dc.emgmt_client(latest_file, prev_file)
