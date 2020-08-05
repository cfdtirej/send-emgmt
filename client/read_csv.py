import csv
import os
import chardet
import yaml


# check the csv file charset
def check_charset(filepath):
    with open(filepath, 'rb') as f:
        reader = f.readlines()
        byte_row = b''
        for r, i in zip(reader, range(8)):
            byte_row += r
        file_details = chardet.detect(byte_row)
        return file_details['encoding']


# Get file diff array
def get_file_diff(latest_file, prev_file):
    charset = check_charset(latest_file)
    with open(latest_file, 'r', encoding=charset) as f:
        reader = csv.reader(f)
        latest_table = [row for row in reader]
    with open(prev_file, 'r', encoding=charset) as f:
        reader = csv.reader(f)
        prev_table = [row for row in reader]
    for prev in prev_table:
        for latest in latest_table:
            if latest == prev:
                latest_table.remove(latest)
    return latest_table


if __name__ == '__main__':
    print(get_file_diff('log_data/dc.CSV', 'prev_log/dc.CSV'))
