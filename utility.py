from hashlib import sha1
from collections import Mapping
from itertools import filterfalse
from json import dumps
from datetime import datetime
from params import PARAMS


def hash_dict(d):
    return str(sha1(dumps(d, sort_keys=True).encode('utf8')).hexdigest())


def dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def list_subtract(l1, l2):
    return list(filterfalse(lambda x: x in l2, l1))


def remove_duplicates(l):
    return [ i for n, i in enumerate(l) if i not in l[n + 1:] ]


def hash_options(options):
    return [
        (column, column + hash_dict({
            key: val for key, val in options.items() if key is not "columns"
        }))
        for column in options['columns']
    ]


def hash_options_list(options_list):
    return [ column for options in options_list for column in hash_options(options) ]


def get_close_hash():
    daily_options = PARAMS['data_options'][0]
    daily_hash = hash_options(daily_options)
    return [ col for col in daily_hash if 'close' in col ][0][1]


def filter_data(keep, data):
    return {
        date: {
            column: val
            for column, val in columns.items() if column in keep
        } for date, columns in data.items()
    }

# inclusive
def date_between(date, start, end):
    date_format = '%Y-%m-%d'
    date = datetime.strptime(date, date_format)
    start = datetime.strptime(start, date_format)
    end = datetime.strptime(end, date_format)
    return start <= date <= end


def dicts_to_arrays(dicts):
    keys = set()
    for d in dicts:
        keys.update(d.keys())
    keys = list(enumerate(sorted(keys)))
    arrays = []
    for d in dicts:
        x = []
        y = []
        for i, v in keys:
            if v in d:
                x.append(i)
                y.append(d[v])
        arrays.append((x, y))
    return arrays
