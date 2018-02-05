import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pickle
from optimal import OptimalTrades
from symbol import SymbolData, SymbolCloseData
from utility import *


class Graph(Data):

    def get_folder(self):
        return 'graph'


    def get_extension(self):
        return ''


    def read_data(self):
        try:
            with open(self.get_path() + 'pkl', 'rb') as fh:
                return pickle.load(fh)
        except FileNotFoundError:
            return


    def write_data(self):
        fig = self.get_data()
        fig.savefig(self.get_path() + 'png')
        with open(self.get_path() + 'pkl', 'wb') as fh:
            pickle.dump(fig, fh)


class SymbolDataGraph(Graph):

    def __init__(self, symbol, options_list, start, end):
        self.symbol = symbol
        self.options_list = options_list
        self.start = start
        self.end = end
        super().__init__()


    def get_params(self):
        return {
            'symbol': self.symbol,
            'options_list': self.options_list,
            'start': self.start,
            'end': self.end
        }


    def get_new_data(self):
        print('graph new data')
        data = SymbolData(self.symbol, self.options_list, self.start, self.end).get_data()
        columns = get_columns(data)
        data_list = [ extract_column(col, data) for col in columns ]

        xys = dicts_to_xys(data_list)

        fig = plt.figure()
        for x, y in xys:
            plt.plot(x, y)

        return fig


class OptimalTradesGraph(Graph):

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
        prices = SymbolCloseData(self.symbol, self.start, self.end).get_data()
        trades = OptimalTrades(self.symbol, self.start, self.end, self.tolerance, self.smoothed).get_data()

        buy_sizes = { k: 20 * v for k, v in trades.items() if v > 0 }
        buy_prices = { k: prices[k] for k in buy_sizes }
        sell_sizes = { k: -20 * v for k, v in trades.items() if v < 0 }
        sell_prices = { k: prices[k] for k in sell_sizes }

        (xp, yp), (xb, ybp), (_, ybs), (xs, ysp), (_, yss) = dicts_to_xys([
            prices, buy_prices, buy_sizes, sell_prices, sell_sizes
        ])

        fig = plt.figure()
        plt.plot(xp, yp)
        plt.scatter(xb, ybp, s=ybs, c='g')
        plt.scatter(xs, ysp, s=yss, c='r')

        return fig
