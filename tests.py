import unittest
import shutil
from neural import NeuralNetwork
from symbol import SymbolData
from optimal import *
from preprocess import NeuralNetworkData, stratify_parts
from graph import OptimalTradesGraph
from screener import yahoo


class TestOptimal(unittest.TestCase):

    def test_no_tolerance1(self):
        prices = [10, 20, 19, 30, 10, 15]
        trades = {0: BUY, 1: SELL, 2: BUY, 3: SELL, 4: BUY}
        self.assertEqual(optimize_trades(prices, 0), trades)

    def test_no_tolerance2(self):
        prices = [10, 20, 20, 10, 20]
        trades = {0: BUY, 1: SELL, 3: BUY}
        self.assertEqual(optimize_trades(prices, 0), trades)

    def test_tolerance1(self):
        prices = [10, 20, 21, 10, 15]
        trades = {0: BUY, 2: SELL, 3: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_tolerance2(self):
        prices = [10, 20, 19, 30, 10, 15]
        trades = {0: BUY, 3: SELL, 4: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_tolerance3(self):
        prices = [10, 20, 19, 20, 10, 15]
        trades = {0: BUY, 1: SELL, 4: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_tolerance4(self):
        prices = [10, 20, 19, 18, 10, 15]
        trades = {0: BUY, 1: SELL, 4: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_tolerance5(self):
        prices = [10, 20, 19, 21, 10, 15]
        trades = {0: BUY, 3: SELL, 4: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_tolerance6(self):
        prices = [10, 20, 19, 21, 10, 15]
        trades = {0: BUY, 3: SELL, 4: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_tolerance7(self):
        prices = [10, 20, 19, 18, 21, 20, 11, 10, 11, 15]
        trades = {0: BUY, 4: SELL, 7: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_sell_first1(self):
        prices = [20, 10, 20]
        trades = {0: SELL, 1: BUY}
        self.assertEqual(optimize_trades(prices, 0), trades)

    def test_sell_first2(self):
        prices = [19, 20, 10, 15]
        trades = {1: SELL, 2: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_buy_first(self):
        prices = [20, 19, 30, 20]
        trades = {1: BUY, 2: SELL}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_buy_first2(self):
        prices = [20, 19, 20, 21, 30]
        trades = {1: BUY}
        self.assertEqual(optimize_trades(prices, 0.1), trades)

    def test_dates(self):
        data = {"2018-01-01": 20, "2018-01-02": 19, "2018-01-03": 30, "2018-01-04": 20}
        trades = {"2018-01-02": 1, "2018-01-03": -1}
        self.assertEqual(calc_trades(data, 0.1), trades)

    def test_smooth1(self):
        prices = [10, 15, 25, 30, 10]
        trades = {0: BUY, 3: SELL}
        smoothed = {0: BUY, 1: 0.5, 2: -0.5, 3: SELL}
        self.assertEqual(smooth_trades(trades, prices), smoothed)

    def test_smooth2(self):
        prices = [10, 25, 15, 30, 10]
        trades = {0: BUY, 3: SELL}
        smoothed = {0: BUY, 1: -0.5, 2: 0.5, 3: SELL}
        self.assertEqual(smooth_trades(trades, prices), smoothed)

    def test_smooth3(self):
        prices = [20, 30, 10]
        trades = {0: BUY, 1: SELL}
        self.assertEqual(smooth_trades(trades, prices), trades)


def remove_last_line(path):
    file = open(path, 'r+', encoding='utf-8')
    file.seek(0, os.SEEK_END)
    pos = file.tell() - 1
    while pos > 0 and file.read(1) != "\n":
        pos -= 2
        file.seek(pos, os.SEEK_SET)
    if pos > 0:
        file.seek(pos, os.SEEK_SET)
        file.truncate()
    file.close()


def remove_folder(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


class TestAllData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PARAMS['data_folder'] = 'test'
        remove_folder('test')

    @classmethod
    def tearDownClass(cls):
        remove_folder('test')

    def test_symbol_data1(self):
        log('\n\nTesting symbol data...\n\n')
        SymbolData(symbol='AAPL', options_list=get_options_list(['sma', 'ema']))

    def test_symbol_data2(self):
        SymbolData(symbol='AAPL', options_list=get_options_list(['macd', 'ema']))

    def test_symbol_data3(self):
        data = SymbolData(symbol='AAPL', options_list=get_options_list(['sma']))
        log('refreshing data...')
        remove_last_line(data.get_symbol_path())
        SymbolData(symbol='AAPL', options_list=get_options_list(['sma', 'ema'])).refresh_data(update_old=True)

    def test_screener(self):
        log('\n\nTesting Yahoo screener...\n\n')
        yahoo('day_gainers')

    def test_optimal_trades1(self):
        log('\n\nTesting optimal trade data...\n\n')
        OptimalTrades(symbol='AAPL', start='2018-01-01', end='2018-01-31')

    def test_optimal_trades2(self):
        OptimalTrades(symbol='AAPL', start='2018-01-01', end='2018-01-31', tolerance=0)

    def test_optimal_graph1(self):
        log('\n\nTesting graphs...\n\n')
        OptimalTradesGraph(symbol='AAPL', start='2018-01-01', end='2018-01-31')

    def test_optimal_graph2(self):
        OptimalTradesGraph(symbol='AAPL', start='2018-01-01', end='2018-01-30', tolerance=0)

    def test_preprocess1(self):
        log('\n\nTesting neural network data...\n\n')
        NeuralNetworkData(**stratify_parts(['AAPL'], [0.25]*3, '2017-01-01', '2018-01-01'),
                          options_list=get_options_list(['sma', 'ema']))

    def test_preprocess2(self):
        NeuralNetworkData(**stratify_parts(['AAPL', 'MSFT'], [0.5, 0.3, 0.1], '2017-01-01', '2018-01-01'),
                          options_list=get_options_list(['sma']), days=5)

    def test_neural1(self):
        log('\n\nTesting neural network...\n\n')
        NeuralNetwork(**stratify_parts(['AAPL'], [0.25]*3, '2017-01-01', '2018-01-01'),
                      options_list=get_options_list(['sma', 'ema']))

    def test_neural2(self):
        NeuralNetwork(**stratify_parts(['AAPL', 'MSFT'], [0.5, 0.1, 0.3], '2017-01-01', '2018-01-01'),
                      options_list=get_options_list(['sma']), days=5, tolerance=0.05)


if __name__ == '__main__':
    unittest.main()
