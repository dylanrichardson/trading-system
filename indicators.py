

def daily():
    return {
        'function': 'TIME_SERIES_DAILY',
        'columns': ['open', 'high', 'low', 'close', 'volume'],
        'outputsize': 'full'
    }


def daily_adjusted():
    return {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'columns': ['adjusted close', 'dividend amount', 'split coefficient'],
        'outputsize': 'full'
    }


def sma(period=30):
    return {
        'function': 'SMA',
        'columns': ['SMA'],
        'interval': 'daily',
        'time_period': period,
        'series_type': 'close'
    }


def ema(period=20):
    return {
        'function': 'EMA',
        'columns': ['EMA'],
        'interval': 'daily',
        'time_period': period,
        'series_type': 'close'
    }


def macd(fast=12, slow=26, signal=9):
    return {
        'function': 'MACD',
        'columns': ['MACD_Signal', 'MACD_Hist', 'MACD'],
        'interval': 'daily',
        'series_type': 'close',
        'fastperiod': fast,
        'slowperiod': slow,
        'signalperiod': signal,
    }


def stoch(fastk, slowk, slowd, kma, dma):
    return {
        'function': 'STOCH',
        'columns': ['SlowD', 'SlowK'],
        'interval': 'daily',
        'series_type': 'close',
        'fastkperiod': fastk,
        'slowkperiod': slowk,
        'slowdperiod': slowd,
        'slowkmatype': kma,
        'slowdmatype': dma
    }


def rsi(period=14):
    return {
        'function': 'RSI',
        'columns': ['RSI'],
        'interval': 'daily',
        'series_type': 'close',
        'time_period': period
    }


def adx(period=14):
    return {
       'function': 'ADX',
       'columns': ['ADX'],
       'interval': 'daily',
       'series_type': 'close',
       'time_period': period
   }


def cci(period=14):
    return {
        'function': 'CCI',
        'columns': ['CCI'],
        'interval': 'daily',
        'series_type': 'close',
        'time_period': period
    }


def aroon(period=14):
    return {
        'function': 'AROON',
        'columns': ['Aroon Up', 'Aroon Down'],
        'interval': 'daily',
        'time_period': period
    }

def bbands(period=14, ndev=2, ma=0):
    return {
        'function': 'BBANDS',
        'columns': ['Real Middle Band', 'Real Upper Band', 'Real Lower Band'],
        'interval': 'daily',
        'time_period': period,
        'series_type': 'close',
        'nbdevup': ndev,
        'nbdevdn': ndev,
        'matype': ma
    }


def ad():
    return {
        'function': 'AD',
        'columns': ['Chaikin A/D'],
        'interval': 'daily',
    }


def obv():
    return {
        'function': 'OBV',
        'columns': ['OBV'],
        'interval': 'daily',
    }
