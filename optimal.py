from __future__ import (absolute_import, division, print_function, unicode_literals)
from data import Data
from utility import *
from symbol import SymbolCloseData, add_symbol_args, handle_symbol_args

BUY = 1
SELL = -1


class OptimalTrades(Data):

    def __init__(self, **params):
        self.symbol = params['symbol']
        self.start = params.get('start', None)
        self.end = params.get('end', None)
        self.tolerance = params.get('tolerance', 0.01)
        super().__init__(**params)

    def get_new_data(self):
        log('Calculating optimal trades...')
        return get_optimal_trades(self.symbol, self.start, self.end, self.tolerance)

    def get_folder(self):
        return 'optimal'

    def get_data_path(self):
        return self.get_path('data.pkl')

    def read_data(self):
        return read_pickle(self.get_data_path())

    def write_data(self):
        write_pickle(self.get_data_path(), self.get_data())


def get_optimal_trades(symbol, start, end, tolerance):
    data = SymbolCloseData(symbol=symbol, start=start, end=end).get_data()
    return calc_trades(data, tolerance=tolerance)


def calc_trades(data, tolerance):
    dates = sorted(data)
    prices = [data[date] for date in dates]
    trades = optimize_trades(prices, tolerance)
    trades = smooth_trades(trades, prices)
    trade_data = {dates[key]: val for key, val in trades.items()}
    return trade_data


def smooth_trades(trades, prices):
    if len(trades) < 2:
        return trades

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
        index -= delay  # index is behind by one = index - 1
        price_diff = (price - prices[index]) / prices[index]

        if buying:  # looking to buy
            if 0 <= price_diff <= tolerance:
                delay += 1
            else:
                delay = 0
                if price_diff > 0:
                    trades[index] = BUY
                    buying = False
        else:  # looking to sell
            if -tolerance <= price_diff <= 0:
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
        index -= delay  # index is behind by one = index - 1
        price_diff = (price - prices[index]) / prices[index]

        if 0 <= price_diff <= tolerance:
            delay += 1
        else:
            delay = 0
            if price_diff > 0:
                return True
        if -tolerance <= price_diff < 0:
            delay += 1
        else:
            delay = 0
            if price_diff < 0:
                return False


def get_optimal_trades_dict(symbols, start, end, tolerance):
    trades = {}
    for symbol in symbols:
        trades[symbol] = OptimalTrades(symbol=symbol, start=start, end=end, tolerance=tolerance)
    return trades


def add_args(parser):
    add_symbol_args(parser)
    parser.add_argument('-t', '--tolerance', type=float, default=0.01,
                        help='tolerance to use in algorithm')


def handle_args(args, parser):
    handle_symbol_args(args, parser)


def main():
    args = parse_args('Load optimal trades.', add_args, handle_args)
    data = get_optimal_trades_dict(args.symbols, args.start, args.end, args.tolerance)
    [log(k, v.get_data(), force=args.print) for k, v in data.items()]
    if args.path:
        [log(k, v.get_path(), force=args.print) for k, v in data.items()]


if __name__ == '__main__':
    main()
