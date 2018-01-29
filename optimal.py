from __future__ import (absolute_import, division, print_function, unicode_literals)


BUY = 1
SELL = -1


def get_optimal_trades(data, tolerance):
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
        index = index - delay # index is behind by one = index - 1
        price_diff = (price - prices[index]) / prices[index]

        if 0 <= price_diff and price_diff <= tolerance:
            delay = delay + 1
        else:
            delay = 0
            if price_diff > 0:
                buying = True
                break
        if -tolerance <= price_diff and price_diff < 0:
            delay = delay + 1
        else:
            delay = 0
            if price_diff < 0:
                trades[index] = SELL
                buying = False
                break

    # determine when to buy and sell
    for index, price in enumerate(prices[1:]):
        index = index - delay # index is behind by one = index - 1
        price_diff = (price - prices[index]) / prices[index]

        if buying: # looking to buy
            if 0 <= price_diff and price_diff <= tolerance:
                delay = delay + 1
            else:
                delay = 0
                if price_diff > 0:
                    trades[index] = BUY
                    buying = False
        else: # looking to sell
            if -tolerance <= price_diff and price_diff <= 0:
                delay = delay + 1
            else:
                delay = 0
                if price_diff < 0:
                    trades[index] = SELL
                    buying = True

    return trades
