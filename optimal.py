from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import json
from params import PARAMS
from utility import *
from data import get_symbol_data


BUY = 1
SELL = -1


def get_optimal_trades(symbol, start, end, tolerance):
    path = get_path(symbol, start, end, tolerance)
    trades = retrieve_trades(path)
    if trades:
        return trades
    data = get_close_data(symbol, start, end)
    trades = calc_trades(data, tolerance)
    save_trades(trades, path)
    return trades


def get_path(symbol, start, end, tolerance):
    file_name = hash_dict({
        'symbol': symbol,
        'start': start,
        'end': end,
        'tolerance': tolerance
    })
    cwd = os.getcwd()
    return os.path.join(cwd, 'data', 'optimal', file_name + '.json')


def retrieve_trades(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_trades(trades, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'w') as outfile:
        json.dump(trades, outfile)


def get_close_data(symbol, start, end):
    daily_options = PARAMS['data_options'][0]
    data = get_symbol_data([daily_options], symbol)
    data = filter_dates(data, start, end)
    data = filter_close(data)
    return data


def filter_dates(data, start, end):
    return {
        date: val for date, val in data.items() if date_between(date, start, end)
    }


def filter_close(data):
    close_hash = get_close_hash()
    return { date: float(columns[close_hash]) for date, columns in data.items() }


def calc_trades(data, tolerance):
    dates = sorted(data)
    prices = [ data[date] for date in dates ]
    trades = optimize_trades(prices, tolerance)
    trade_data = { dates[key]: val for key, val in trades.items() }
    return trade_data


def optimize_trades(prices, tolerance):
    if len(prices) < 2:
        return {}

    buying = True
    delay = 0
    trades = {}

    # determine whether to buy or sell first
    for index, price in enumerate(prices[1:]):
        index -= delay # index is behind by one = index - 1
        price_diff = (price - prices[index]) / prices[index]

        if 0 <= price_diff and price_diff <= tolerance:
            delay += 1
        else:
            delay = 0
            if price_diff > 0:
                buying = True
                break
        if -tolerance <= price_diff and price_diff < 0:
            delay += 1
        else:
            delay = 0
            if price_diff < 0:
                trades[index] = SELL
                buying = False
                break

    # determine when to buy and sell
    for index, price in enumerate(prices[1:]):
        index -= delay # index is behind by one = index - 1
        price_diff = (price - prices[index]) / prices[index]

        if buying: # looking to buy
            if 0 <= price_diff and price_diff <= tolerance:
                delay += 1
            else:
                delay = 0
                if price_diff > 0:
                    trades[index] = BUY
                    buying = False
        else: # looking to sell
            if -tolerance <= price_diff and price_diff <= 0:
                delay += 1
            else:
                delay = 0
                if price_diff < 0:
                    trades[index] = SELL
                    buying = True

    return trades

get_optimal_trades('AAPL', '2018-01-01', '2018-01-30', 0.01)
