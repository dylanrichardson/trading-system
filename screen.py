from __future__ import (absolute_import, division, print_function, unicode_literals)
import sys
import os
from urllib.parse import quote_plus
import requests
import json
from base64 import b64encode
from params import USERNAME, PASSWORD
from pyquery import PyQuery as pq


def get_portfolio(screener):
    return yahoo(screener)


# get data from Yahoo predefined screeners
def yahoo(screener):
    d = pq(url='https://finance.yahoo.com/screener/predefined/%s' % screener)
    elements = d("td.Va\\(m\\) > a.Fw\\(b\\)")
    return [ a.text for a in elements ]


# AAII screener 'table > tbody > tr:nth-child(2n+1) > td:nth-child(2) > a'
# needs authentication

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
