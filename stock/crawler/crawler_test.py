
import datetime
from io import StringIO

import numpy as np
import pandas as pd
import requests


def crawl_price(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-', '') + '&type=ALL')
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '})
                                          for i in r.text.split('\n')
                                          if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    ret = ret.set_index('證券代號')
    ret['成交金額'] = ret['成交金額'].str.replace(',', '')
    ret['成交股數'] = ret['成交股數'].str.replace(',', '')
    return ret


if __name__ == '__main__':
    date = datetime.datetime.now()
    p = crawl_price(date)
    print(p)
