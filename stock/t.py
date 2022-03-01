from twstock import Stock
import datetime


def get_stock_price(stock_id):
    s = Stock(stock_id)
    ret = []
    today = datetime.datetime.today()
    stock_closing = 1 if today < today.replace(hour=13, minute=30, second=0) else 0
    for index, i in enumerate(s.price[-5:]):
        date = today - datetime.timedelta(days=(4 - index + stock_closing))
        ret.append(
            {
                'date': date.strftime('%Y-%m-%d'),
                'price': i,
            }
        )
        s.fetch()
    return ret


if __name__ == '__main__':
    price = get_stock_price("2330")
    print(price)

    import matplotlib.pyplot as plt
    import pandas as pd

    stock_6207 = Stock("6207")
    stock_6207_2018 = stock_6207.fetch_from(2018, 1)     # 獲取 2018 年 01 月至今日之股票資料
    stock_6207_2018_pd = pd.DataFrame(stock_6207_2018)
    stock_6207_2018_pd = stock_6207_2018_pd.set_index('date')

    fig = plt.figure(figsize=(10, 6))
    plt.plot(stock_6207_2018_pd.close, '-', label="收盤價")
    plt.plot(stock_6207_2018_pd.open, '-', label="開盤價")
    plt.title('雷科股份2018 開盤/收盤價曲線', loc='right')
    # loc->title的位置
    plt.xlabel('日期')
    plt.ylabel('收盤價')
    plt.grid(True, axis='y')
    plt.legend()
    fig.savefig('day20_01.png')
