import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from indicators import *


ALPHAVANTAGE = 'alphavantage_key'
INTRINIO_USERNAME = 'intrinio_username'
INTRINIO_PASSWORD = 'intrinio_password'
DATA_FOLDER = 'data'


def check_credentials():
    for var in [ALPHAVANTAGE, INTRINIO_USERNAME, INTRINIO_PASSWORD]:
        if not os.environ.get(var):
            not_found(var)


def not_found(var):
    raise Exception(var + ' not found in environment')


check_credentials()


PARAMS = {

    'verbose': False,

    'credentials': {
        'alphavantage': os.environ.get(ALPHAVANTAGE),
        'intrinio': {
            'username': os.environ.get(INTRINIO_USERNAME),
            'password': os.environ.get(INTRINIO_PASSWORD)
        }
    },

    'data_folder': os.environ.get('data_folder') or DATA_FOLDER,

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

    'data_options': {
        'daily': daily,
        'daily_adj': daily_adjusted,
        'sma': sma,
        'ema': ema,
        'macd': macd,
        'stoch': stoch,
        'rsi': rsi,
        'adx': adx,
        'cci': cci,
        'aroon': aroon,
        'bbands': bbands,
        'ad': ad,
        'obv': obv
    }

}
