import numpy as np
import pickle
from data import get_symbol_data
from optimal import get_optimal_trades
from utility import *
from params import PARAMS

def get_ann_model():
    pass # TODO


def get_ann_data(symbol, options_list, days, start, end, tolerance, smoothed):
    params = {
        'symbol': symbol,
        'options_list': options_list,
        'days': days,
        'start': start,
        'end': end,
        'tolerance': tolerance,
        'smoothed': smoothed
    }
    path = get_path(params, 'ann', 'pkl')
    data = retrieve_ann_data(path)
    if data:
        return data
    matrix_in, matrix_out = calc_ann_data(symbol, options_list, days, start, end, tolerance, smoothed)
    save_ann_data(matrix_in, matrix_out, path)
    return matrix_in, matrix_out


def calc_ann_data(symbol, options_list, days, start, end, tolerance, smoothed):
    data = get_symbol_data(symbol, options_list)
    trades = get_optimal_trades(symbol, start, end, tolerance, smoothed)
    data_in, data_out = filter_incomplete(data, trades)
    data_in = add_prior_days(data_in, days)
    matrix_in = json_to_matrix(data_in)
    matrix_out = json_to_matrix(data_out)
    return matrix_in, matrix_out


def add_prior_days(data, days):
    new_data = {}
    data_list = list(enumerate(data))
    for current, date in data_list[days:]:
        # print('date', date)
        new_data[date] = {}
        for prior in range(days + 1):
            # print('prior', prior)
            prior_data = data[data_list[current - prior][1]]
            # print(prior_data)
            for col in list(prior_data):
                # print('col', col, prior_data[col])
                new_data[date][str(col) + str(prior)] = prior_data[col]
                # print('new_data', new_data)
            # print('new_data', new_data)
        # print('new_data', new_data)
    return new_data


def retrieve_ann_data(path):
    try:
        with open(path, 'rb') as fh:
            data = pickle.loads(fh.read())
            return data['in'], data['out']
    except (FileNotFoundError, EOFError) as e:
        return


def save_ann_data(matrix_in, matrix_out, path):
    make_path(path)
    with open(path, 'wb') as fh:
        fh.write(pickle.dumps({'in': matrix_in, 'out': matrix_out}))


def filter_incomplete(data, trades):
    data = { k: v for k, v in data.items() if k in trades and complete(v) }
    trades = { k: v for k, v in trades.items() if k in data }
    return data, trades


def complete(datum):
    for _, v in datum.items():
        if v is None or v == '':
            return False
    return True


def json_to_matrix(data):
    if type(data) is dict:
        return np.array([ json_to_matrix(data[k]) for k in sorted(data) ])
    return float(data)
