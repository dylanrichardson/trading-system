from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import json
from argparse import ArgumentParser
from data import Data
from params import PARAMS
from utility import *
from symbol import SymbolCloseData


BUY = 1
SELL = -1

class OptimalTrades(Data):

    def __init__(self, symbol, start, end, tolerance):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.tolerance = tolerance
        super().__init__()


    def get_params(self):
        return {
            'symbol': self.symbol,
            'start': self.start,
            'end': self.end,
            'tolerance': self.tolerance
        }

    def get_new_data(self):
        data = SymbolCloseData(self.symbol, self.start, self.end).get_data()
        return calc_trades(data, self.tolerance)


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


def calc_trades(data, tolerance):
    dates = sorted(data)
    prices = [ data[date] for date in dates ]
    trades = optimize_trades(prices, tolerance)
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


def parse_args():
    parser = ArgumentParser(description='Load optimal trades.')
    parser.add_argument('-s', '--symbols', type=str, nargs='+', help='symbol(s)')
    parser.add_argument('-y', '--screener', type=str, help='name of Yahoo screener')
    parser.add_argument('-l', '--limit', type=int, help='take the first l symbols')
    parser.add_argument('-t', '--tolerance', type=float, required=True,
                        help='tolerance to use in algorithm')
    parser.add_argument('--start', type=str, help='start date of data')
    parser.add_argument('--end', type=str, help='end date of data')
    parser.add_argument('-p', '--print', action='store_true', help='print the data')
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug messages')

    args = parser.parse_args()

    PARAMS['verbose'] = args.verbose

    if not args.symbols and not args.screener:
        parser.error('At least one of --symbols or --screener is required')

    return args


def get_optimal_trades(symbols, screener, limit, start, end, tolerance):
    symbols = get_symbols(symbols, screener, limit)
    trades = {}
    for symbol in symbols:
        trades[symbol] = OptimalTrades(symbol, start, end, tolerance).get_data()
    return trades


def main():
    args = parse_args()
    trades = get_optimal_trades(args.symbols, args.screener, args.limit,
        args.start, args.end, args.tolerance)
    if args.print:
        print(json.dumps(trades, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
