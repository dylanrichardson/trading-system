import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PARAMS = {

    'credentials': {
        'alphavantage': os.environ.get('alphavantage'),
        'intrinio': {
            'username': os.environ.get('intrinio_username'),
            'password': os.environ.get('intrinio_password')
        }
    },

    'screeners': {
        'yahoo': [
            'undervalued_growth_stocks',
            'day_gainers',
            'day_losers',
            'most_actives',
            'growth_technology_stocks',
            'undervalued_large_caps',
            'aggressive_small_caps',
            'portfolio_anchors',
            'solid_large_growth_funds'
        ],
        'intrinio': {
            'undervalued': {
                'conditions': [
                    ['pricetoearnings', '<=', 20],
                    ['pricetoearnings', '>', 0]
                ]
            }
        }
    },

    'data_options': [{
        'function': 'TIME_SERIES_DAILY',
        'columns': ['open', 'high', 'low', 'close', 'volume'],
        'outputsize': 'full'
    }, {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'columns': ['adjusted close', 'dividend amount', 'split coefficient'],
        'outputsize': 'full'
    }, {
        'function': 'SMA',
        'columns': ['SMA'],
        'interval': 'daily',
        'time_period': '50',
        'series_type': 'close'
    }, {
        'function': 'SMA',
        'columns': ['SMA'],
        'interval': 'daily',
        'time_period': '200',
        'series_type': 'close'
    }, {
        'function': 'EMA',
        'columns': ['EMA'],
        'interval': 'daily',
        'time_period': '50',
        'series_type': 'close'
    }, {
        'function': 'EMA',
        'columns': ['EMA'],
        'interval': 'daily',
        'time_period': '200',
        'series_type': 'close'
    }, {
        'function': 'MACD',
        'columns': ['MACD_Signal', 'MACD_Hist', 'MACD'],
        'interval': 'daily',
        'series_type': 'close',
        'fastperiod': '12',
        'slowperiod': '26',
        'signalperiod': '9',
    }, {
        'function': 'MACD',
        'columns': ['MACD_Signal', 'MACD_Hist', 'MACD'],
        'interval': 'daily',
        'series_type': 'close',
        'fastperiod': '5',
        'slowperiod': '35',
        'signalperiod': '5',
    }, {
        'function': 'STOCH',
        'columns': ['SlowD', 'SlowK'],
        'interval': 'daily',
        'series_type': 'close',
        'fastkperiod': '5',
        'slowkperiod': '3',
        'slowdperiod': '3',
        'slowkmatype': '0',
        'slowdmatype': '0'
    }, {
        'function': 'STOCH',
        'columns': ['SlowD', 'SlowK'],
        'interval': 'daily',
        'series_type': 'close',
        'fastkperiod': '5',
        'slowkperiod': '3',
        'slowdperiod': '3',
        'slowkmatype': '1',
        'slowdmatype': '1'
    }, {
        'function': 'STOCH',
        'columns': ['SlowD', 'SlowK'],
        'interval': 'daily',
        'series_type': 'close',
        'fastkperiod': '5',
        'slowkperiod': '3',
        'slowdperiod': '3',
        'slowkmatype': '2',
        'slowdmatype': '2'
    }, {
        'function': 'STOCH',
        'columns': ['SlowD', 'SlowK'],
        'interval': 'daily',
        'series_type': 'close',
        'fastkperiod': '5',
        'slowkperiod': '3',
        'slowdperiod': '3',
        'slowkmatype': '7',
        'slowdmatype': '7'
    }, {
        'function': 'STOCH',
        'columns': ['SlowD', 'SlowK'],
        'interval': 'daily',
        'series_type': 'close',
        'fastkperiod': '5',
        'slowkperiod': '3',
        'slowdperiod': '3',
        'slowkmatype': '8',
        'slowdmatype': '8'
    }, {
        'function': 'RSI',
        'columns': ['RSI'],
        'interval': 'daily',
        'series_type': 'close',
        'time_period': '14'
    }, {
        'function': 'RSI',
        'columns': ['RSI'],
        'interval': 'daily',
        'series_type': 'close',
        'time_period': '60'
    }, {
        'function': 'ADX',
        'columns': ['ADX'],
        'interval': 'daily',
        'series_type': 'close',
        'time_period': '14'
    }, {
        'function': 'ADX',
        'columns': ['ADX'],
        'interval': 'daily',
        'series_type': 'close',
        'time_period': '60'
    }, {
        'function': 'CCI',
        'columns': ['CCI'],
        'interval': 'daily',
        'series_type': 'close',
        'time_period': '20'
    }, {
        'function': 'CCI',
        'columns': ['CCI'],
        'interval': 'daily',
        'time_period': '60'
    }, {
        'function': 'AROON',
        'columns': ['Aroon Up', 'Aroon Down'],
        'interval': 'daily',
        'time_period': '14'
    }, {
        'function': 'AROON',
        'columns': ['Aroon Up', 'Aroon Down'],
        'interval': 'daily',
        'time_period': '60'
    }, {
        'function': 'BBANDS',
        'columns': ['Real Middle Band', 'Real Upper Band', 'Real Lower Band'],
        'interval': 'daily',
        'time_period': '14',
        'series_type': 'close',
        'nbdevup': '2',
        'nbdevdn': '2',
        'matype': '0'
    }, {
        'function': 'BBANDS',
        'columns': ['Real Middle Band', 'Real Upper Band', 'Real Lower Band'],
        'interval': 'daily',
        'time_period': '14',
        'series_type': 'close',
        'nbdevup': '2',
        'nbdevdn': '2',
        'matype': '1'
    }, {
        'function': 'BBANDS',
        'columns': ['Real Middle Band', 'Real Upper Band', 'Real Lower Band'],
        'interval': 'daily',
        'time_period': '14',
        'series_type': 'close',
        'nbdevup': '2',
        'nbdevdn': '2',
        'matype': '2'
    }, {
        'function': 'BBANDS',
        'columns': ['Real Middle Band', 'Real Upper Band', 'Real Lower Band'],
        'interval': 'daily',
        'time_period': '14',
        'series_type': 'close',
        'nbdevup': '2',
        'nbdevdn': '2',
        'matype': '7'
    }, {
        'function': 'BBANDS',
        'columns': ['Real Middle Band', 'Real Upper Band', 'Real Lower Band'],
        'interval': 'daily',
        'time_period': '14',
        'series_type': 'close',
        'nbdevup': '2',
        'nbdevdn': '2',
        'matype': '8'
    }, {
        'function': 'AD',
        'columns': ['Chaikin A/D'],
        'interval': 'daily',
    }, {
        'function': 'OBV',
        'columns': ['OBV'],
        'interval': 'daily',
    }]

}
