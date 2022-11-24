import pandas as pd
import yfinance as yf
import datetime as dt
import time
import requests


def yfinance_data(ticker, interval='1d', years_data=7):

    """
    DATES EXAMPLE = '2022-10-06'
    """

    try:

        start = dt.datetime.today() - dt.timedelta(365*years_data)
        start = start.strftime('%Y-%m-%d')

        end = dt.datetime.today() + dt.timedelta(1)
        end = end.strftime('%Y-%m-%d')

        data = yf.download(tickers=ticker, interval=interval, auto_adjust=True, start=start, end=end)

        data.index = pd.to_datetime(data.index)
        data = data.tz_localize(None)

    except:
        data = pd.DataFrame()

    return data


def data_etfs(tickers, interval='1d', years_data=10):

    dfs = []
    for ticker in tickers:

        print(f'Descargando data {ticker}')

        data = yfinance_data(ticker=ticker, interval=interval, years_data=years_data)

        if data.empty:
            print(f'Error con ticker {ticker}')
            continue

        data_filter = pd.DataFrame()
        data_filter[ticker] = data['Close']

        dfs.append(data_filter)

    data_all = pd.concat(dfs, axis=1)

    return data_all

