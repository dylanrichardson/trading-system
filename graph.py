import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pickle
from argparse import ArgumentParser
from data import Data
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


    def get_figure(self):
        return self.get_data()


    def get_new_data(self):
        return self.make_figure()


    def make_figure(self):
        raise NotImplementedError()


    def show(self):
        self.get_figure().show()


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


    def make_figure(self):
        log('Making new symbol data graph...')
        data = SymbolData(self.symbol, self.options_list, self.start, self.end).get_data()
        columns = get_columns(data)
        data_list = [ extract_column(col, data) for col in columns ]

        xys = dicts_to_xys(data_list)

        fig = plt.figure()
        for x, y in xys:
            plt.plot(x, y)

        return fig


class OptimalTradesGraph(Graph):

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


    def make_figure(self):
        prices = SymbolCloseData(self.symbol, self.start, self.end).get_data()
        trades = OptimalTrades(self.symbol, self.start, self.end, self.tolerance).get_data()

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


def parse_args():
    parser = ArgumentParser(description='Load a graph.')
    parser.add_argument('-d', '--data', type=str, choices=['data', 'optimal', 'neural'],
                        help='data to graph', required=True)
    parser.add_argument('-s', '--symbols', type=str, nargs='+', help='symbol(s)')
    parser.add_argument('-y', '--screener', type=str, help='name of Yahoo screener')
    parser.add_argument('-l', '--limit', type=int, help='take the first l symbols')
    parser.add_argument('-o', '--options', type=int, nargs='+',
                        help='indices of data_options in params.py')
    parser.add_argument('-t', '--tolerance', type=float, help='tolerance to use in algorithm')
    parser.add_argument('--start', type=str, help='start date of data')
    parser.add_argument('--end', type=str, help='end date of data')
    parser.add_argument('-p', '--print', action='store_true', help='show the graph')
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug messages')

    args = parser.parse_args()

    PARAMS['verbose'] = args.verbose

    if not args.symbols and not args.screener:
        parser.error('At least one of -s/--symbols or -y/--screener is required')

    if args.data == 'optimal' and not args.tolerance:
        parser.error('-t/--tolerance is required to graph optimal trades')

    if args.data == 'data' and not args.options:
        parser.error('-o/--options is required to graph symbol data')

    return args


def get_symbol_data_graphs(symbols, options_indices, start, end):
    options_list = get_options_list(options_indices)
    graphs = {}
    for symbol in symbols:
        graphs[symbol] = SymbolDataGraph(symbol, options_list, start, end).get_figure()
    return graphs


def get_optimal_trades_graphs(symbols, start, end, tolerance):
    graphs = {}
    for symbol in symbols:
        graphs[symbol] = OptimalTradesGraph(symbol, start, end, tolerance).get_figure()
    return graphs


def main():
    args = parse_args()
    symbols = get_symbols(args.symbols, args.screener, args.limit)
    if args.data == 'data':
        get_symbol_data_graphs(symbols, args.options, args.start, args.end)
    elif args.data == 'optimal':
        get_optimal_trades_graphs(symbols, args.start, args.end, args.tolerance)
    else:
        pass # TODO get_neural_network_graphs()
    if args.print:
        plt.show()


if __name__ == '__main__':
    main()
