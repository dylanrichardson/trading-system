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


API_KEY = PARAMS['credentials']['alphavantage']
DAILY_OPTIONS = PARAMS['data_options'][0]


class SymbolData(Data):

    def __init__(self, symbol, options_list, start=None, end=None):
        self.symbol = symbol
        self.options_list = options_list
        self.start = start
        self.end = end
        self.all_data = {}
        super().__init__()


    def get_params(self):
        return {
            'symbol': self.symbol
        }


    def get_folder(self):
        return 'symbol'


    def get_extension(self):
        return 'csv'


    def write_data(self):
        with open(self.get_path(), 'w') as outfile:
            csv_file = csv.writer(outfile)
            data = self.get_all_data()
            columns = ['Date'] + get_columns(data)
            csv_file.writerow(columns)
            for date in sorted(data):
                csv_file.writerow(json_to_csv(data, date, columns))


    def get_all_data(self):
        if not self.all_data:
            self.get_data()
        return self.all_data


    def read_data(self):
        self.all_data = self.read_all_data()
        self.refresh_data()
        if self.all_data:
            data =  self.filter_data(self.all_data)
            return data


    def filter_data(self, data):
        columns = list(map(lambda c: c[1], encrypt_options_list(self.options_list)))
        data = filter_columns(columns, data)
        if self.start and self.end:
            data = filter_dates(data, self.start, self.end)
        return data


    def read_all_data(self):
        try:
            with open(self.get_path(), 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                data = {}
                for row in reader:
                    new_data = csv_to_json(row)
                    dict_merge(data, new_data)
                return data
        except FileNotFoundError:
            return {}


    def get_new_data(self):
        data = download_symbol_data(self.symbol, self.options_list)
        dict_merge(self.all_data, data)
        return self.filter_data(data)


    def refresh_data(self, update_old=False):
        missing_columns = get_missing_columns(self.all_data, self.options_list)
        if update_old:
            missing_columns += get_old_columns(self.all_data)
        # print('missing %s columns' % len(missing_columns))
        missing_options = columns_to_options(missing_columns)
        if missing_options:
            new_data = download_symbol_data(self.symbol, missing_options)
            dict_merge(self.all_data, new_data)
            self.write_data()


class SymbolCloseData(SymbolData):

    def __init__(self, symbol, start=None, end=None):
        super().__init__(symbol, [DAILY_OPTIONS], start, end)


    def get_data(self):
        if not hasattr(self, 'data'):
            data = super().get_data()
            self.data = filter_close(data)
        return self.data


def download_symbol_datum(symbol, options):
    options = {
        key: value for key, value in options.items() if value is not 'columns'
    }
    print('downloading', symbol, 'with options', options)
    data = request({ **{
        'symbol': symbol,
        'apikey': API_KEY
    }, **options })
    data = sanitize_data(data)
    data = convert_data(data, options)
    return data


def download_symbol_data(symbol, options_list):
    data = {}
    for options in options_list:
        new_data = download_symbol_datum(symbol, options)
        dict_merge(data, new_data)
    return data



def request(options):
    url = 'https://www.alphavantage.co/query?%s' % urlencode(options)
    data = requests.get(url).json()
    if 'Error Message' in data:
        raise Exception(data['Error Message'])
    data = next(data[key] for key in data.keys() if key != 'Meta Data')
    return data


def sanitize_data(data):
    return { date[:DATE_LENGTH]: sanitize_datum(data[date]) for date in data }


def sanitize_datum(datum):
    return { (key[3:] if key[1:3] == ". " else key): val for key, val in datum.items() }


def convert_data(data, options):
    columns = encrypt_options(options)
    return {
        date: {
            column_hash: data[date][column]
            for column, column_hash in columns if column in data[date]
        } for date in data.keys()
    }


def json_to_csv(data, date, headers):
    return [date] + list(map(lambda col: data[date].get(col, ""), headers[1:]))


def csv_to_json(datum):
    date = datum['Date']
    del datum['Date']
    return { date: datum }


def columns_to_options(columns):
    options_list = [ decrypt_dict(column) for column in columns ]
    for options in options_list:
        del options['column']
    return remove_duplicates(options_list)


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


def get_missing_columns(data, options_list):
    present_columns = get_columns(data)
    columns = list(map(lambda c: c[1], encrypt_options_list(options_list)))
    missing_columns = list_subtract(columns, present_columns)
    return missing_columns
