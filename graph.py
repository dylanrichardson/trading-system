import optimal
import symbol

import matplotlib.pyplot as plt
import pickle
from argparse import ArgumentParser

import neural
from data import Data
from optimal import OptimalTrades
from symbol import SymbolData, SymbolCloseData
from utility import *


class Graph(Data):

    def get_folder(self):
        return 'graph'

    def get_extension(self):
        return ''

    def get_fig_path(self):
        return self.get_path() + 'pkl'

    def get_pic_path(self):
        return self.get_path() + 'png'

    def read_data(self):
        try:
            return read_pickle(self.get_fig_path())
        except FileNotFoundError:
            return

    def write_data(self):
        fig = self.get_data()
        fig.savefig(self.get_pic_path())
        write_pickle(self.get_fig_path(), fig)

    def get_figure(self):
        return self.get_data()

    def get_new_data(self):
        log('Graphing...')
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
        return graph_symbol_data(self.symbol, self.options_list, self.start, self.end)


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
        return graph_optimal_trades(self.symbol, self.start, self.end, self.tolerance)


def graph_symbol_data(symbol, options_list, start, end):
    data = SymbolData(symbol, options_list, start, end).get_data()
    columns = get_columns(data)
    data_list = [extract_column(col, data) for col in columns]

    xys = dicts_to_xys(data_list)

    fig = plt.figure()
    for x, y in xys:
        plt.plot(x, y)

    return fig


def graph_optimal_trades(symbol, start, end, tolerance):
    prices = SymbolCloseData(symbol, start, end).get_data()
    trades = OptimalTrades(symbol, start, end, tolerance).get_data()

    buy_sizes = {k: 20 * v for k, v in trades.items() if v > 0}
    buy_prices = {k: prices[k] for k in buy_sizes}
    sell_sizes = {k: -20 * v for k, v in trades.items() if v < 0}
    sell_prices = {k: prices[k] for k in sell_sizes}

    (xp, yp), (xb, ybp), (_, ybs), (xs, ysp), (_, yss) = dicts_to_xys([
        prices, buy_prices, buy_sizes, sell_prices, sell_sizes
    ])

    fig = plt.figure()
    plt.plot(xp, yp)
    plt.scatter(xb, ybp, s=ybs, c='g')
    plt.scatter(xs, ysp, s=yss, c='r')

    return fig


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


def add_args(parser):
    parser.add_argument('data', type=str, action='append', choices=['data', 'optimal', 'neural'],
                        help='data to graph')
    neural.add_args(parser)


def handle_args(args, parser):
    if args.data == 'optimal':
        optimal.handle_args(args, parser)
    if args.data == 'data':
        symbol.handle_args(args, parser)
    if args.data == 'neural':
        neural.handle_args(args, parser)


def get_neural_network_graph():
    print('AYO')


def main():
    args = parse_args('Load a graph.', add_args, handle_args)
    data = []
    if args.data == 'data':
        data += get_symbol_data_graphs(args.symbols, args.options, args.start, args.end)
    if args.data == 'optimal':
        data += get_optimal_trades_graphs(args.symbols, args.start, args.end, args.tolerance)
    if args.data == 'neural':
        data += get_neural_network_graph()
    if args.print or PARAMS['verbose']:
        plt.show()
    if args.path:
        [log(d.get_path(), force=args.print) for d in data]


if __name__ == '__main__':
    main()
