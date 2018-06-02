from __future__ import (absolute_import, division, print_function, unicode_literals)
from urllib.parse import urlencode
import requests
import csv
from data import Data
from utility import *
from params import PARAMS

API_KEY = PARAMS['credentials']['alphavantage']
DAILY_OPTIONS = PARAMS['data_options']['daily']()


class SymbolData(Data):

    def __init__(self, **params):
        self.symbol = params['symbol']
        self.options_list = params['options_list']
        self.start = params.get('start', None)
        self.end = params.get('end', None)
        self.all_data = {}
        super().__init__(symbol=self.symbol)
        self.params = params
        self.write_params()

    def get_folder(self):
        return 'symbol'

    def get_symbol_path(self):
        return self.get_path(self.symbol + '.csv')

    def write_data(self):
        write_symbol_data(self.get_all_data(), self.get_symbol_path())

    def get_all_data(self):
        if not self.all_data:
            self.get_data()
        return self.all_data

    def read_data(self):
        self.all_data = self.read_all_data()
        self.refresh_data()
        if self.all_data:
            data = self.filter_data(self.all_data)
            return data

    def filter_data(self, data):
        return filter_data(data, self.options_list, self.start, self.end)

    def read_all_data(self):
        return read_symbol_data(self.get_symbol_path())

    def get_new_data(self):
        data = download_symbol_data(self.symbol, self.options_list)
        dict_merge(self.all_data, data)
        return self.filter_data(data)

    def refresh_data(self, update_old=False):
        missing_columns = get_missing_columns(self.all_data, self.options_list)
        if update_old:
            missing_columns += get_old_columns(self.all_data)
        missing_options = columns_to_options(missing_columns)
        if missing_options:
            new_data = download_symbol_data(self.symbol, missing_options)
            dict_merge(self.all_data, new_data)
            self.write_data()


class SymbolCloseData(SymbolData):

    def __init__(self, **params):
        self.data = None
        super().__init__(options_list=[DAILY_OPTIONS], **params)

    def get_data(self):
        if not self.data:
            data = super().get_data()
            self.data = filter_close(data)
        return self.data


def download_symbol_datum(symbol, options):
    options = {
        key: value for key, value in options.items() if value is not 'columns'
    }
    log('Downloading %s data for %s...' % (options['function'], symbol))
    data = request({**{
        'symbol': symbol,
        'apikey': API_KEY
    }, **options})
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
    return {date[:DATE_LENGTH]: sanitize_datum(data[date]) for date in data}


def sanitize_datum(datum):
    return {(key[3:] if key[1:3] == ". " else key): val for key, val in datum.items()}


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
    return {date: datum}


def columns_to_options(columns):
    options_list = [decrypt_dict(column) for column in columns]
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
        old_columns = [k for k, v in data[date].items() if v == '']
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


def get_portfolio_data(symbols, options_list, start, end, refresh):
    data = {}
    for symbol in symbols:
        data[symbol] = SymbolData(symbol=symbol, options_list=options_list, start=start, end=end)
        data[symbol].refresh_data(update_old=refresh)
    return data


def write_symbol_data(data, path):
    with open(path, 'w') as outfile:
        csv_file = csv.writer(outfile)
        columns = ['Date'] + get_columns(data)
        csv_file.writerow(columns)
        for date in sorted(data):
            csv_file.writerow(json_to_csv(data, date, columns))


def read_symbol_data(path):
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


def filter_data(data, options_list, start, end):
    columns = list(map(lambda c: c[1], encrypt_options_list(options_list)))
    data = filter_columns(columns, data)
    if start and end:
        data = filter_dates(data, start, end)
    data = filter_incomplete(data)
    return data


def add_symbol_args(parser):
    parser.add_argument('-s', '--symbols', type=str, nargs='+', help='symbol(s)')
    parser.add_argument('-y', '--screener', type=str, help='name of Yahoo screener')
    parser.add_argument('-l', '--limit', type=int,
                        help='take the first l symbols')
    parser.add_argument('--start', type=str, action='append', default=[],
                        help='start date of data')
    parser.add_argument('--end', type=str, action='append', default=[],
                        help='end date of data')


def add_args(parser):
    add_symbol_args(parser)
    parser.add_argument('-o', '--options', type=str, nargs='+', required=True,
                        help='indices of data_options in params.py')
    parser.add_argument('-r', '--refresh', action='store_true', help='refresh the data')


def handle_symbol_args(args, parser):
    if not args.symbols and not args.screener:
        parser.error('At least one of -s/--symbols or -y/--screener is required')
    args.symbols = get_symbols(args.symbols, args.screener, args.limit)


def handle_options_args(args, parser):
    args.options_list = get_options_list(args.options)


def handle_dates(args, parser):
        args.start = first(args.start)
        args.end = first(args.end)


def handle_args(args, parser):
    handle_symbol_args(args, parser)
    handle_options_args(args, parser)
    handle_dates(args, parser)


def main():
    args = parse_args('Load symbol data.', add_args, handle_args)
    data = get_portfolio_data(args.symbols, args.options_list, args.start, args.end, args.refresh)
    log({k: v.get_data() for k, v in data.items()}, force=args.print)
    if args.path:
        [log(k, v.get_path(), force=args.print) for k, v in data.items()]


if __name__ == '__main__':
    main()
