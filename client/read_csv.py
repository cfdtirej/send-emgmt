import csv
import os
import chardet
import numpy as np
import pprint


# check the csv file charset
def check_charset(csvpath):
    with open(csvpath, 'rb') as f:
        reader = f.readlines()
        byte_row = b''
        for r, i in zip(reader, range(8)):
            byte_row += r
        file_details = chardet.detect(byte_row)
        return file_details['encoding']


def get_file_diff(latest_file, bak_file):
    charset = check_charset(latest_file)

    with open(latest_file, 'r', encoding=charset) as f:
        reader = csv.reader(f)
        latest_table = [row for row in reader]
    with open(bak_file, 'r', encoding=charset) as f:
        reader = csv.reader(f)
        bak_table = [row for row in reader]
    for bak in bak_table:
        for latest in latest_table:
            if latest == bak:
                latest_table.remove(latest)
    return latest_table


if __name__ == '__main__':
    print()

