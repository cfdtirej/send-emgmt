import json
import shutil
import socket
import zlib

import csv_processing
import config


class SendEmgmt:
    def __init__(self, host, port, measurement):
        self.host = host
        self.port = port
        self.measurement = measurement

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
                    data_json = {
                        'measurement': self.measurement,
                        'tags': {
                            'class': self.measurement
                        },
                        'time': times_list[count],
                        'fields': dict(zip(column, csv_diff[count][1:]))
                    }
                    if csv_diff[count][1:] is None:
                        break
                    compress_json = zlib.compress(json.dumps(data_json).encode('utf-8'))
                    s.connect((self.host, self.port))
                    s.sendall(compress_json)
                    recv_msg = s.recv(4096)
                    print('#---Server message---#\n{}'.format(recv_msg))
            count += 1
            if count == len(csv_diff) - 1:
                # Copy latest csv file to prev folder
                # shutil.copy(latest_file, prev_file)
                break


if __name__ == '__main__':
    host = config.socket_info['host']
    port = config.socket_info['port']
    latest_file = config.filepath['LatestLog']['dc']
    prev_file = config.filepath['PrevLog']['dc']
    dc = SendEmgmt(host, port, 'dc')
    dc.emgmt_client(latest_file, prev_file)
