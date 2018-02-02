import unittest
from optimal import calc_trades, smooth_trades, optimize_trades, BUY, SELL

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


if __name__ == '__main__':
    unittest.main()
