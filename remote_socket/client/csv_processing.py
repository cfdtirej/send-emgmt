import csv
import chardet

import config


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
def get_csv_diff(latest_file, prev_file):
    # using 'check_charset' function
    charset = check_charset(latest_file)
    with open(latest_file, 'r', encoding=charset) as f:
        reader = csv.reader(f)
        latest_table = [row for row in reader]
        if 'hpcs' in latest_file:
            column = latest_table[0]
            del latest_table[0]
        else:
            column = latest_table[2]
            del latest_table[:2]
    with open(prev_file, 'r', encoding=charset) as f:
        reader = csv.reader(f)
        prev_table = [row for row in reader]
        if 'hpcs' in prev_file:
            del prev_table[0]
        else:
            del prev_table[:2]
    # get latest to previous diff two dim array
    for prev in prev_table:
        for latest in latest_table:
            if latest == prev:
                latest_table.remove(latest)
    # type conversion
    for i in range(len(latest_table)):
        for j in range(len(latest_table[0])):
            try:
                latest_table[i][j] = float(latest_table[i][j])
            except ValueError:
                latest_table[i][j] = str(latest_table[i][j])
    latest_table.insert(0, column)
    return latest_table


if __name__ == '__main__':
    latest_file = config.filepath['LatestLog']['dc']
    prev_file = config.filepath['PrevLog']['dc']
    csv_diff = get_csv_diff(latest_file, prev_file)
    print(csv_diff)
