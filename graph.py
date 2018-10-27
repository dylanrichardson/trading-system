import optimal
import symbol
import matplotlib.pyplot as plt
import neural
from data import Data
from optimal import OptimalTrades
from symbol import SymbolData, SymbolCloseData
from utility import *

PT_SIZE = 20

class Graph(Data):

    def get_folder(self):
        return 'graph'

    def get_fig_path(self):
        return self.get_path('graph.pkl')

    def get_pic_path(self):
        return self.get_path('graph.png')

    def read_data(self):
        return read_pickle(self.get_fig_path())

    def write_data(self):
        fig = self.get_data()
        fig.savefig(self.get_pic_path())
        write_pickle(self.get_fig_path(), fig)

    def get_figure(self):
        return self.get_data()

    def get_new_data(self):
        return self.make_figure()

    def show(self):
        plt.show()

    def make_figure(self):
        raise NotImplementedError()


class SymbolDataGraph(Graph):

    def __init__(self, **params):
        self.symbol = params['symbol']
        self.options_list = params['options_list']
        self.start = params.get('start', None)
        self.end = params.get('end', None)
        super().__init__(**params)

    def make_figure(self):
        log('Making new symbol data graph...')
        return graph_symbol_data(self.symbol, self.options_list, self.start, self.end)


class OptimalTradesGraph(Graph):

    def __init__(self, **params):
        self.symbol = params['symbol']
        self.tolerance = params.get('tolerance', 0.01)
        self.start = params.get('start', None)
        self.end = params.get('end', None)
        super().__init__(**params)

    def make_figure(self):
        log('Making new optimal trades graph...')
        return graph_optimal_trades(self.symbol, self.start, self.end, self.tolerance)


class StrategyTradesGraph(Graph):

    def __init__(self, strategy=None):
        self.strategy = strategy
        super().__init__(strategy=self.strategy.params)

    def make_figure(self):
        log('Making new strategy trades graph...')
        return graph_strategy_trades(self.strategy)


def graph_symbol_data(symbol, options_list, start, end):
    data = SymbolData(symbol=symbol, options_list=options_list, start=start, end=end).get_data()
    columns = get_columns(data)
    data_list = [extract_column(col, data) for col in columns]

    xys = dicts_to_xys(data_list)

    fig = plt.figure()
    for x, y in xys:
        plt.plot(x, y)

    plt.title('Symbol Data (%s)' % symbol)
    plt.ylabel('Indicator Value')
    plt.xlabel('Date')
    # TODO add legend

    return fig


def graph_optimal_trades(symbol, start, end, tolerance):
    prices = SymbolCloseData(symbol=symbol, start=start, end=end).get_data()
    trades = OptimalTrades(symbol=symbol, start=start, end=end,
                            tolerance=tolerance).get_data()

    buy_sizes = {k: PT_SIZE * v for k, v in trades.items() if v > 0}
    buy_prices = {k: prices[k] for k in buy_sizes}
    sell_sizes = {k: -PT_SIZE * v for k, v in trades.items() if v < 0}
    sell_prices = {k: prices[k] for k in sell_sizes}

    (xp, yp), (xb, ybp), (_, ybs), (xs, ysp), (_, yss) = dicts_to_xys([
        prices, buy_prices, buy_sizes, sell_prices, sell_sizes
    ])

    fig = plt.figure()
    plt.plot(xp, yp)
    plt.scatter(xb, ybp, s=ybs, c='g')
    plt.scatter(xs, ysp, s=yss, c='r')

    plt.title('Optimal Trades (%s)' % symbol)
    plt.ylabel('Price')
    plt.xlabel('Date')
    # TODO fix date labels

    return fig


def graph_strategy_trades(strategy):
    prices = SymbolCloseData(symbol=strategy.symbol, start=strategy.start,
                            end=strategy.end).get_data()
    trades = strategy.get_data()

    buy_prices = { t['date']: t['price'] for t in trades if t['buy'] }
    sell_prices = { t['date']: t['price'] for t in trades if not t['buy'] }

    (xp, yp), (xb, ybp), (xs, ysp) = dicts_to_xys([
        prices, buy_prices, sell_prices
    ])

    fig = plt.figure()
    plt.plot(xp, yp)
    plt.scatter(xb, ybp, c='g')
    plt.scatter(xs, ysp, c='r')

    plt.title('Strategy Trades (%s)' % strategy.symbol)
    plt.ylabel('Price')
    plt.xlabel('Date')

    return fig


def get_symbol_data_graphs(symbols, options_list, start, end):
    graphs = {}
    log(end)
    for symbol in symbols:
        graphs[symbol] = SymbolDataGraph(symbol=symbol, options_list=options_list,
                                         start=start, end=end).get_figure()
    return graphs


def get_optimal_trades_graphs(symbols, start, end, tolerance):
    graphs = {}
    for symbol in symbols:
        graphs[symbol] = OptimalTradesGraph(symbol=symbol, tolerance=tolerance,
                                            start=start, end=end).get_figure()
    return graphs


def add_args(parser):
    parser.add_argument('data', type=str, help='data to graph',
                        choices=['data', 'optimal', 'neural', 'strategy'])
    neural.add_args(parser)


def handle_args(args, parser):
    if args.data == 'neural':
        neural.handle_args(args, parser)
    elif args.data == 'optimal':
        optimal.handle_args(args, parser)
    elif args.data == 'data':
        symbol.handle_args(args, parser)


def get_neural_network_graph():
    print('neural network graph not implemented')


def get_strategy_graph():
    print('strategy graph not implemented')


def main():
    args = parse_args('Load a graph.', add_args, handle_args)
    data = []
    if args.data == 'data':
        data += get_symbol_data_graphs(args.symbols, args.options_list, args.start, args.end)
    if args.data == 'optimal':
        data += get_optimal_trades_graphs(args.symbols, args.start, args.end, args.tolerance)
    if args.data == 'neural':
        data += get_neural_network_graph()
    if args.data == 'strategy':
        data += get_strategy_graph()
    if args.print or PARAMS['verbose']:
        plt.show()
    if args.path:
        [log(d.get_path(), force=args.print) for d in data]


if __name__ == '__main__':
    main()
