from __future__ import (absolute_import, division, print_function, unicode_literals)
import sys
import os
from urllib.parse import quote_plus
import requests
import json
from base64 import b64encode
from params import USERNAME, PASSWORD
from pyquery import PyQuery as pq


def get_portfolio(name):
    return yahoo(name)


# get data from Yahoo predefined screeners
def yahoo(name):
    d = pq(url='https://finance.yahoo.com/screener/predefined/%s' % name)
    elements = d("td.Va\\(m\\) > a.Fw\\(b\\)")
    return [ a.text for a in elements ]


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
