import unittest
import shutil
from symbol import SymbolData
from optimal import *
from preprocess import NeuralNetworkData
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
    file = open(path, 'r+', encoding = 'utf-8')
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

    def test_all(self):
        PARAMS['data_folder'] = 'test'
        remove_folder('test')

        log('\n\nTesting symbol data...\n\n')

        SymbolData('AAPL', get_options_list(['sma', 'ema']))
        SymbolData('AAPL', get_options_list(['macd', 'ema']))
        data = SymbolData('AAPL', get_options_list(['sma']))

        log('refreshing data...')
        remove_last_line(data.get_path())

        SymbolData('AAPL', get_options_list(['sma', 'ema'])).refresh_data(update_old=True)

        log('\n\nTesting Yahoo screener...\n\n')

        yahoo('day_gainers')

        log('\n\nTesting optimal trade data...\n\n')

        OptimalTrades('AAPL', '2018-01-01', '2018-01-31', 0.01)
        OptimalTrades('AAPL', '2018-01-01', '2018-01-31', 0)

        log('\n\nTesting graphs...\n\n')

        OptimalTradesGraph('AAPL', '2018-01-01', '2018-01-31', 0.01)
        OptimalTradesGraph('AAPL', '2018-01-01', '2018-01-30', 0.01)


        log('\n\nTesting neural network data...\n\n')

        NeuralNetworkData('AAPL', get_options_list(['sma', 'ema']), 0, '2018-01-01', '2018-01-31', 0.01)
        NeuralNetworkData('AAPL', get_options_list(['macd', 'ema']), 1, '2018-01-01', '2018-01-31', 0.01)

        remove_folder('test')


if __name__ == '__main__':
    unittest.main()
