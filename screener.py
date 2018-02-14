from __future__ import (absolute_import, division, print_function, unicode_literals)

from argparse import ArgumentParser
from urllib.parse import quote_plus
import requests
from base64 import b64encode
from pyquery import PyQuery as pq
from utility import *


# get data from Yahoo predefined screeners
def yahoo(screener):
    d = pq(url='https://finance.yahoo.com/screener/predefined/%s' % screener)
    elements = d("td.Va\\(m\\) > a.Fw\\(b\\)")
    return [a.text for a in elements]


# AAII screener 'table > tbody > tr:nth-child(2n+1) > td:nth-child(2) > a'
# needs authentication


USERNAME = PARAMS['credentials']['intrinio']['username']
PASSWORD = PARAMS['credentials']['intrinio']['password']


# get data from Intrinio custom screeners
def request(conditions):
    params = encode_conditions(conditions)
    url = 'https://api.intrinio.com/securities/search?conditions=%s' % quote_plus(params)
    auth = 'Basic %s' % b64encode(('%s:%s' % (USERNAME, PASSWORD)).encode()).decode()
    headers = {
        'Authorization': auth
    }
    return requests.get(url, headers=headers).json()


def encode_element(element):
    if element == '>':
        return 'gt'
    elif element == '>=':
        return 'gte'
    elif element == '<':
        return 'lt'
    elif element == '<=':
        return 'lte'
    elif element == '=':
        return 'eq'
    else:
        return str(element)


def encode_condition(condition):
    return "~".join(map(encode_element, condition))


def encode_conditions(conditions):
    return ",".join(map(encode_condition, conditions))


def add_args(parser):
    parser.add_argument('screener', type=str, help='name of Yahoo screener')
    parser.add_argument('-l', '--limit', type=int, help='take the first l symbols')


def handle_args(args, parser):
    pass


def main():
    args = parse_args('Screen for symbols.', add_args, handle_args)
    data = ' '.join(get_symbols(None, args.screener, args.limit))
    log(data, force=args.print)


if __name__ == '__main__':
    main()