from asyncio.windows_events import NULL
from symtable import Symbol
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import yfinance as yf
import pyodbc
import datetime as dt
class getData():

    def getHistoryYfinance(self, symbol, interval, period, start = None):

        data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = symbol,

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        # period = "ytd",
        period = period,

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = interval,

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = False,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = False,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None, 
        start = start
    )
        return data

    def getStockDataMonthSQL(self, symbol, interval):
                        
            myConnection = pyodbc.connect(
                        r'Driver=SQL Server;'
                r'Server=.\SQLEXPRESS;'
                r'Database=StockData;'
                r'Trusted_Connectstr(ion=)yes;')

            sqlstr = ("""SELECT 
                [Datetime]
                ,[Adj Close]
                ,[Close]
                ,[High]
                ,[Low]
                ,[Open]
                ,[Volume]
                FROM [StockData].[dbo].[VI_StockData]
                WHERE 
                [SymbolName] = '""" + symbol + """'
                AND [Interval] = '""" + interval + """'
                AND CAST(Datetime AS Date) BETWEEN '2022-02-01' AND '2022-03-01'
                """)
            sql_query = pd.read_sql_query (sqlstr, myConnection)

            df = pd.DataFrame(sql_query, columns = ['Datetime', 'AdjClose', 'Close', 'High', 'Low', 'Open', 'Volume'])
            df = df.set_index(['Datetime'])
            return(df)                
