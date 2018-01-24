from __future__ import (absolute_import, division, print_function, unicode_literals)
import sys
import os
from urllib.parse import urlencode
import requests
import json
import csv
import collections
import itertools
from hashlib import sha1
from params import DATA_OPTIONS_LIST, API_KEY


def request(options):
    url = 'https://www.alphavantage.co/query?%s' % urlencode(options)
    data = requests.get(url).json()
    if 'Error Message' in data:
        raise Exception(data['Error Message'])
    data = next(data[key] for key in data.keys() if key != 'Meta Data')
    return data


def download(options, symbol):
    options = {
        key: value for key, value in options.items() if value is not 'columns'
    }
    print('downloading', symbol, 'with options', options)
    data = request({ **{
        'symbol': symbol,
        'apikey': API_KEY
    }, **options })
    data = sanitize_data(data)
    data = convert_data(options, data)
    return data


def download_list(options_list, symbol):
    data = {}
    for options in options_list:
        new_data = download(options, symbol)
        dict_merge(data, new_data)
    return data


def sanitize_data(data):
    return { date: sanitize_datum(data[date]) for date in data }


def sanitize_datum(datum):
    return { (key[3:] if key[1:3] == ". " else key): val for key, val in datum.items() }


def hash_options(options):
    return [
        (column, column + str(sha1(json.dumps({
            key: val for key, val in options.items() if key is not "columns"
        }, sort_keys=True).encode('utf8')).hexdigest()))
        for column in options['columns']
    ]


def hash_options_list(options_list):
    return [ column for options in options_list for column in hash_options(options) ]


def convert_data(options, data):
    columns = hash_options(options)
    return {
        date: {
            column_hash: data[date][column]
            for column, column_hash in columns if column in data[date]
        } for date in data.keys()
    }


def save_data(data, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'w') as outfile:
        csv_file = csv.writer(outfile)
        columns = ['Date'] + get_columns(data)
        csv_file.writerow(columns)
        for date in sorted(data):
            csv_file.writerow(json_to_csv(data, date, columns))


def json_to_csv(data, date, headers):
    return [date] + list(map(lambda col: data[date].get(col, ""), headers[1:]))


def get_path(symbol, folder=None):
    cwd = os.getcwd()
    folder = folder or os.path.join(cwd, 'data')
    path = os.path.join(folder, symbol + '.csv')
    return path


def csv_to_json(datum):
    date = datum['Date']
    del datum['Date']
    return { date: datum }


def retrieve_data(path):
    try:
        with open(path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            data = {}
            for row in reader:
                new_data = csv_to_json(row)
                dict_merge(data, new_data)
            return data
    except FileNotFoundError:
        return {}


def dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def list_subtract(l1, l2):
    return list(itertools.filterfalse(lambda x: x in l2, l1))


def get_columns(data):
    DATE_LENGTH = 10
    for date in data.keys():
        if len(date) == DATE_LENGTH:
            return list(data[date].keys())
    return []


def column_to_options(column, options_list):
    for options in options_list:
        columns = map(lambda c: c[1], hash_options(options))
        if column in columns:
            return options
    return {}


def filter_data(keep, data):
    return {
        date: {
            column: val
            for column, val in columns.items() if column in keep
        } for date, columns in data.items()
    }

def remove_duplicates(l):
    return [ i for n, i in enumerate(l) if i not in l[n + 1:] ]


def get_symbol_data(options_list, symbol, folder=None):
    path = get_path(symbol, folder)
    data = retrieve_data(path)
    present_columns = get_columns(data)
    columns = list(map(lambda c: c[1], hash_options_list(options_list)))
    missing_columns = list_subtract(columns, present_columns)
    if missing_columns:
        missing_options = [ column_to_options(column, options_list) for column in missing_columns ]
        missing_options = remove_duplicates(missing_options)
        new_data = download_list(missing_options, symbol)
        dict_merge(data, new_data)
        save_data(data, path)
    data = filter_data(columns, data)
    return data


def get_data(options_list, portfolio, folder=None):
    data = {}
    for symbol in portfolio:
        new_data = get_symbol_data(options_list, symbol, folder)
        dict_merge(data, new_data)
    return data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
        folder = None
        if len(sys.argv) > 2:
            folder = sys.argv[2]
        get_data(DATA_OPTIONS_LIST, [symbol], folder)
    else:
        print('Missing symbol argument')
