import csv
import os
import pathlib

from datetime import datetime
from typing import List, Dict

from tqdm import tqdm
from influxdb import InfluxDBClient
    

def conv_list_value_type(data: list) -> list:
    result = []
    for v in data:
        try:
            value = float(v)
            result.append(value)
        except ValueError:
            value = str(v)
            result.append(value)
    return result


def to_rfc3339(timestamp: str) -> str:
        if '/' in timestamp:
            return datetime.strptime(timestamp.partition('.')[0] + '+0900', '%Y/%m/%d %H:%M:%S%z').isoformat()
        elif '-' in timestamp:
            return datetime.strptime(timestamp.partition('.')[0] + '+0900', '%Y-%m-%d %H:%M:%S%z').isoformat()


class InfluxOp(InfluxDBClient):

    def csv_write(self, csvfile: str, measurement: str, tags: dict) -> None:
        with open(csvfile, 'r') as f:
            table =  [_ for _ in csv.reader(f)]
            cnt = 0
            for row in tqdm(table):
                if cnt == 0:
                    header = row
                    cnt += 1
                    continue
                row = conv_list_value_type(row)
                fields = {}
                for k, v in zip(header[1:], row[1:]):
                    try:
                        fields[k] = v
                    except IndexError:
                        pass
                to_line_protocol = [
                    {
                        'measurement': measurement,
                        'tags': tags,
                        'time': to_rfc3339(row[0]),
                        'fields': fields
                    }
                ]
                try:
                    self.write_points(to_line_protocol)
                except:
                    pass

        return None
        

if __name__ == '__main__':
    pass

