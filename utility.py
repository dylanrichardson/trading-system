import pickle
from argparse import ArgumentParser
from hashlib import sha1
from collections import Mapping
from itertools import filterfalse
import json
from datetime import datetime, timedelta, date as Date
import numpy as np
from binascii import hexlify, unhexlify
import os
from Crypto.Cipher import AES
from params import PARAMS
from screener import yahoo

DATE_LENGTH = 10
CRYPT_KEY = '1234567890123456'


def log(*args, force=False, **kwargs):
    if PARAMS['verbose'] or force:
        args = list(args)
        for i, arg in enumerate(args):
            if type(arg) is dict:
                try:
                    args[i] = json.dumps(arg, indent=4, sort_keys=True)
                except:
                    pass
        print(*args, **kwargs)


def set_verbosity(verbose):
    PARAMS['verbose'] = verbose or PARAMS['verbose']


def shorten_path(path):
    return str(sha1(path.encode('utf-8')).hexdigest())


def make_path(path):
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def write_pickle(path, data):
    with open(path, 'wb') as fh:
        fh.write(pickle.dumps(data))


def read_pickle(path):
    try:
        with open(path, 'rb') as fh:
            return pickle.loads(fh.read())
    except (FileNotFoundError, EOFError):
        return


def parse_args(description, add_args, handle_args):
    parser = ArgumentParser(description=description)
    add_args(parser)
    parser.add_argument('-p', '--print', action='store_true', help='print the data')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable logging')
    parser.add_argument('--path', action='store_true', help='print the data path')
    args = parser.parse_args()
    set_verbosity(args.verbose)
    handle_args(args, parser)
    return args


def filter_incomplete(d):
    return {k: v for k, v in d.items() if complete(v)}


def filter_matching(d1, d2):
    d1 = filter_incomplete(d1)
    d2 = filter_incomplete(d2)
    d1 = {k: v for k, v in d1.items() if k in d2}
    d2 = {k: v for k, v in d2.items() if k in d1}
    return d1, d2


def complete(datum):
    if type(datum) is dict:
        for _, v in datum.items():
            if v is None or v == '':
                return False
    return True


def json_to_matrix(data):
    if type(data) is dict:
        return np.array([json_to_matrix(data[k]) for k in sorted(data)])
    return float(data)


def encrypt_dict(d):
    e = AES.new(CRYPT_KEY, AES.MODE_CFB, CRYPT_KEY)
    s = json.dumps(d, sort_keys=True)
    return hexlify(e.encrypt(s)).decode('utf-8')


def decrypt_dict(crypt):
    e = AES.new(CRYPT_KEY, AES.MODE_CFB, CRYPT_KEY)
    s = e.decrypt(unhexlify(crypt))
    return json.loads(s.decode('utf-8'))


def dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def merge_data(datum_list):
    data = {}
    for datum in datum_list:
        dict_merge(data, datum)
    return data


def list_subtract(l1, l2):
    return list(filterfalse(lambda x: x in l2, l1))


def remove_duplicates(l):
    return [i for n, i in enumerate(l) if i not in l[:n]]


def encrypt_options(options):
    return [(column, encrypt_dict({**options, **{'column': column}}))
            for column in options['columns']]


def encrypt_options_list(options_list):
    return [column for options in options_list for column in encrypt_options(options)]


def get_close_crypt():
    daily_options = PARAMS['data_options']['daily']()
    daily_crypt = encrypt_options(daily_options)
    return [col for col in daily_crypt if 'close' in col][0][1]


def filter_columns(keep, data):
    return {
        date: {
            column: val
            for column, val in columns.items() if column in keep
        } for date, columns in data.items()
    }


def extract_column(column, data):
    return {date: columns[column] for date, columns in data.items()}


def get_latest_weekday():
    today = Date.today()
    latest_day = today - timedelta(max(4, today.weekday()) - 4)
    return latest_day.strftime('%Y-%m-%d')


def to_date(date):
    return datetime.strptime(date, '%Y-%m-%d')


# inclusive
def date_between(date, start, end):
    date = to_date(date)
    start = to_date(start)
    end = to_date(end)
    return start <= date <= end


def filter_dates(data, start, end):
    return {
        date: val for date, val in data.items() if date_between(date, start, end)
    }


def filter_close(data):
    close_hash = get_close_crypt()
    return {date: float(columns[close_hash]) for date, columns in data.items()}


def get_columns(data):
    for date in data.keys():
        if len(date) == DATE_LENGTH:
            return list(data[date].keys())
    return []


def dicts_to_xys(dicts):
    keys = set()
    for d in dicts:
        keys.update(d.keys())
    keys = list(enumerate(sorted(keys)))
    xys = []
    for d in dicts:
        x = []
        y = []
        for i, v in keys:
            if v in d:
                x.append(i)
                y.append(d[v])
        xys.append((x, y))
    return xys


def get_symbols(symbols, screener, limit):
    symbols = symbols or []
    if screener:
        symbols += yahoo(screener)
    return symbols[:limit]


def get_options(options_str):
    paren = options_str.find('(')
    if paren == -1:
        return PARAMS['data_options'][options_str]()
    name = options_str[:paren]
    args = options_str[paren + 1:-1].split(',')
    return PARAMS['data_options'][name](*args)


def get_options_list(options_strs):
    return [get_options(options_str) for options_str in options_strs]
