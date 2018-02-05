from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import json
from params import PARAMS
from utility import *
from symbol import SymbolCloseData


BUY = 1
SELL = -1

class OptimalTrades(Data):

    def __init__(self, symbol, start, end, tolerance, smoothed):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.tolerance = tolerance
        self.smoothed = smoothed
        super().__init__()


    def get_params(self):
        return {
            'symbol': self.symbol,
            'start': self.start,
            'end': self.end,
            'tolerance': self.tolerance,
            'smoothed': self.smoothed
        }

    def get_new_data(self):
        data = SymbolCloseData(self.symbol, self.start, self.end).get_data()
        return calc_trades(data, self.tolerance, self.smoothed)


    def get_folder(self):
        return 'optimal'


    def get_extension(self):
        return 'json'


    def read_data(self):
        try:
            with open(self.get_path(), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return


    def write_data(self):
        with open(self.get_path(), 'w') as fh:
            json.dump(self.get_data(), fh)


def calc_trades(data, tolerance, smoothed):
    dates = sorted(data)
    prices = [ data[date] for date in dates ]
    trades = optimize_trades(prices, tolerance)
    if smoothed:
        trades = smooth_trades(trades, prices)
    trade_data = { dates[key]: val for key, val in trades.items() }
    return trade_data


def smooth_trades(trades, prices):
    if len(trades) < 2:
        return trades

    buy_price = None
    sell_price = None
    ordered_trades = sorted(trades.items())

    for i, (date, trade) in enumerate(ordered_trades[1:]):
        last_date = ordered_trades[i][0]
        if trade == BUY:
            buy_price = prices[date]
            sell_price = prices[last_date]
        else:
            buy_price = prices[last_date]
            sell_price = prices[date]
        for j, price in enumerate(prices[last_date + 1:date]):
            trades[last_date + 1 + j] = smooth_trade(price, buy_price, sell_price)

    return trades


def smooth_trade(price, buy_price, sell_price):
    return 1 - 2 * (price - buy_price) / (sell_price - buy_price)


def optimize_trades(prices, tolerance):
    if len(prices) < 2:
        return {}

    # determine whether to buy or sell first
    buying = should_buy_first(prices, tolerance)

    delay = 0
    trades = {}

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


def should_buy_first(prices, tolerance):
    delay = 0

    for index, price in enumerate(prices[1:]):
        index -= delay # index is behind by one = index - 1
        price_diff = (price - prices[index]) / prices[index]

        if 0 <= price_diff and price_diff <= tolerance:
            delay += 1
        else:
            delay = 0
            if price_diff > 0:
                return True
        if -tolerance <= price_diff and price_diff < 0:
            delay += 1
        else:
            delay = 0
            if price_diff < 0:
                return False
