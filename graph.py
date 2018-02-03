import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from optimal import get_close_data, get_optimal_trades
from utility import dicts_to_arrays


def plot_optimal_trades(symbol, start, end, tolerance, smoothed=True):
    prices = get_close_data(symbol, start, end)
    trades = get_optimal_trades(symbol, start, end, tolerance, smoothed)

    buy_sizes = { k: 20 * v for k, v in trades.items() if v > 0 }
    buy_prices = { k: prices[k] for k in buy_sizes }
    sell_sizes = { k: -20 * v for k, v in trades.items() if v < 0 }
    sell_prices = { k: prices[k] for k in sell_sizes }

    (xp, yp), (xb, ybp), (_, ybs), (xs, ysp), (_, yss) = dicts_to_arrays([
        prices, buy_prices, buy_sizes, sell_prices, sell_size
    ])

    fig = plt.figure()
    plt.plot(xp, yp)
    plt.scatter(xb, ybp, s=ybs, c='g')
    plt.scatter(xs, ysp, s=yss, c='r')
    return fig
