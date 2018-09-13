import datetime  
import os.path 
import sys 
import backtrader as bt
from data import Data
from symbol import SymbolData, SymbolCloseData
from preprocess import add_prior_days
from utility import *

COMMISION = 0.001
SLIPPAGE = 0.01
INITIAL_FUNDS = 10000
STAKE = 10

class Strategy(Data):
    
    def __init__(self, **params):
        self.neural = params['neural']
        self.start = params['start']
        self.end = params['end']
        self.symbol = params['symbol']
        self.options_list = self.neural.options_list
        self.days = self.neural.days
        super().__init__(neural=self.neural.params, start=self.start,
                end=self.end, symbol=self.symbol)

    def get_folder(self):
        return 'strategy'

    def get_data_path(self):
        return self.get_path('data.pkl')

    def read_data(self):
        return read_pickle(self.get_data_path())

    def write_data(self):
        write_pickle(self.get_data_path(), self.get_data())

    def get_new_data(self):
        log('Backtesting strategy...')
        self.setup_input_data()
        strategy = self.backtest()
        return strategy.get_results()

    def setup_input_data(self):
        # download price and specified indicators
        SymbolData(symbol=self.symbol, options_list=[DAILY_OPTIONS], 
                start=self.start, end=self.end)
        symbol_data = SymbolData(symbol=self.symbol, options_list=self.options_list,
                start=self.start, end=self.end)
        # get the path to the data
        self.symbol_path = symbol_data.get_symbol_path()
        symbol_data = symbol_data.get_data()
        # format data for input to neural network
        self.input_data = add_prior_days(symbol_data, self.days, symbol_data)

    # remove dates from feed that don't have any data
    def data_filter(self):
        def filter(data_feed):
            date = from_date(data_feed.datetime.date())
            if date not in self.input_data:
                data_feed.backwards()
                return True
            return False
        return filter

    def get_data_feed(self):
        # get OHLCV column indices in CSV
        headers = get_csv_headers(self.symbol_path)
        daily_indices = {}
        daily_crypt = get_daily_crypt()
        for key in daily_crypt:
            daily_indices[key] = headers.index(daily_crypt[key])
        # create BT data feed from saved symbol data in CSV
        data_feed = bt.feeds.GenericCSVData(
            dataname=self.symbol_path,
            fromdate=to_date(self.start),
            todate=to_date(self.end),
            dtformat=('%Y-%m-%d'),
            openinterest=-1,
            **daily_indices)
        # remove dates without data
        data_feed.addfilter(self.data_filter())
        return data_feed

    def get_cebebro(self):
        cerebro = bt.Cerebro()
        # add strategy based on given neural network
        cerebro.addstrategy(BTStrategy, symbol_data=self.input_data,
                    neural=self.neural)
        data_feed = self.get_data_feed()
        cerebro.adddata(data_feed)
        # add drawdown observer
        cerebro.addobserver(bt.observers.DrawDown)
        # set funds, commision, slippage, and position sizer
        cerebro.broker.setcash(INITIAL_FUNDS)
        cerebro.broker.setcommission(commission=COMMISION)
        cerebro.broker.set_slippage_perc(SLIPPAGE)
        cerebro.addsizer(bt.sizers.FixedSize, stake=STAKE)
        return cerebro

    def backtest(self):
        cerebro = self.get_cebebro()
        # log(cerebro.broker.getvalue())
        strategy = cerebro.run()[0]
        # log(cerebro.broker.getvalue())
        # cerebro.plot()
        return strategy


class BTStrategy(bt.Strategy):

    params = (
        ('symbol_data', None),
        ('neural', None),
        ('threshold', 0.8)   
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.symbol_data = self.params.symbol_data
        self.neural = self.params.neural
        self.threshold = self.params.threshold
        if not self.symbol_data:
            raise Exception('A Backtrader strategy expects a symbol_data parameter')
        if not self.neural:
            raise Exception('A Backtrader strategy expects a neural parameter')
        # keep track of pending orders
        self.order = None
        # keep track of trades
        self.trades = []

    def get_date(self):
        return from_date(self.datas[0].datetime.date())

    # def notify_trade(self, trade):
    #     if not trade.isclosed:
    #         return

    #     log(self.get_date(), 'OPERATION PROFIT, GROSS %.2f, NET %.2f' %
    #              (trade.pnl, trade.pnlcomm))

    def notify_order(self, order):
        # reset order status if order finished
        if order.status not in [order.Submitted, order.Accepted]:
            self.order = None
            if order.status == order.Completed:
                if order.isbuy():
                    self.trades.append({
                        'date': self.get_date(),
                        'buy': True,
                        'price': order.executed.price,
                        'value': order.executed.value,
                        'commission': order.executed.comm
                    })
                    # log(self.get_date(), 'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    #     (order.executed.price,
                    #      order.executed.value,
                    #      order.executed.comm))
                else:
                    self.trades.append({
                        'date': self.get_date(),
                        'buy': False,
                        'price': order.executed.price,
                        'value': order.executed.value,
                        'commission': order.executed.comm
                    })
                    # log(self.get_date(), 'SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    #      (order.executed.price,
                    #       order.executed.value,
                    #       order.executed.comm))

    def next(self):
        # check for pending order
        if self.order:
            return
        # format input data for neural network
        input_data = json_to_matrix(self.symbol_data[self.get_date()])
        # use neural network
        prediction = self.neural.predict(input_data)
        # buy/sell based on neural network prediction and position in market
        if prediction > self.threshold and not self.position:
            self.order = self.buy()
            # log(self.get_date(), 'buy', (self.datas[0].close[0]))
        elif prediction < -self.threshold and self.position:
            self.order = self.sell()
            # log(self.get_date(), 'sell', (self.datas[0].close[0]))

    def get_results(self):
        return self.trades

