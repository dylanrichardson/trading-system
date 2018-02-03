from __future__ import (absolute_import, division, print_function, unicode_literals)
import sys
import os
from urllib.parse import urlencode
import requests
import json
import csv
import datetime
from utility import *
from params import PARAMS


OPTIONS_LIST = PARAMS['data_options']
API_KEY = PARAMS['credentials']['alphavantage']
DATE_LENGTH = 10


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
    return { date[:DATE_LENGTH]: sanitize_datum(data[date]) for date in data }


def sanitize_datum(datum):
    return { (key[3:] if key[1:3] == ". " else key): val for key, val in datum.items() }


def convert_data(options, data):
    columns = hash_options(options)
    return {
        date: {
            column_hash: data[date][column]
            for column, column_hash in columns if column in data[date]
        } for date in data.keys()
    }


def save_data(data, path):
    make_path(path)
    with open(path, 'w') as outfile:
        csv_file = csv.writer(outfile)
        columns = ['Date'] + get_columns(data)
        csv_file.writerow(columns)
        for date in sorted(data):
            csv_file.writerow(json_to_csv(data, date, columns))


def json_to_csv(data, date, headers):
    return [date] + list(map(lambda col: data[date].get(col, ""), headers[1:]))


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


def get_columns(data):
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


def get_latest_weekday():
    today = datetime.date.today()
    latest_day = today - datetime.timedelta(max(4, today.weekday()) - 4)
    return latest_day.strftime('%Y-%m-%d')


def get_old_columns(data):
    dates = sorted(data, reverse=True)
    if len(dates) == 0:
        return []
    # check latest data against date
    if dates[0] != get_latest_weekday():
        return get_columns(data)
    # check missing data
    columns = set()
    for date in dates:
        old_columns = [ k for k,v in data[date].items() if v == '' ]
        if len(old_columns) > 0:
            columns.update(old_columns)
        else:
            break
    return list(columns)


def refresh_symbol_data(symbol, options_list):
    data = get_symbol_data(symbol, options_list)
    # determine missing columns
    present_columns = get_columns(data)
    columns = list(map(lambda c: c[1], hash_options_list(options_list)))
    missing_columns = list_subtract(columns, present_columns)
    # determine old columns
    old_columns = get_old_columns(data)
    missing_columns += old_columns
    # download new data
    if missing_columns:
        missing_options = [ column_to_options(column, options_list) for column in missing_columns ]
        missing_options = remove_duplicates(missing_options)
        new_data = download_list(missing_options, symbol)
        dict_merge(data, new_data)
        save_data(data, path)


def refresh_data(portfolio, options_list):
    for symbol in portfolio:
        refresh_symbol_data(symbol, options_list)


def get_symbol_data(symbol, options_list):
    path = get_path(symbol, 'symbol', 'csv')
    data = retrieve_data(path)
    columns = list(map(lambda c: c[1], hash_options_list(options_list)))
    return filter_columns(columns, data)


def get_data(portfolio, options_list):
    data = {}
    for symbol in portfolio:
        new_data = get_symbol_data(symbol, options_list)
        dict_merge(data, new_data)
    return data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
        get_symbol_data(symbol, OPTIONS_LIST)
    else:
        print('Missing symbol argument')
