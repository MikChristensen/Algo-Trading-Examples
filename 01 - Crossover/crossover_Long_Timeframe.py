## https://squareoff.in/a-simple-ema-crossover-trading-strategy-with-exceptional-returns/

from datetime import datetime
import backtrader as bt
from backtrader.indicators import SMA
from GetData import getData
import numpy as np
import matplotlib as plt


date = '2022-05-16'
symbol = 'googl'
interval = '1wk'
period = '10y'

getdata = getData()
rawData = getdata.getHistoryYfinance(symbol=symbol, interval=interval, period=period)

class SmaCross(bt.Strategy):
    
    # list of parameters which are configurable for the strategy
    params = dict(
        pEMA1=10,  # period for the fast moving average - Default 10
        pEMA2=50  # period for the fast moving average - Default 50
    )

    def __init__(self):
        self.EMA1 = bt.ind.EMA(period=self.p.pEMA1)  # fast moving average
        self.EMA2 = bt.ind.EMA(period=self.p.pEMA2)  # fast moving average
        self.LongPos = False
        self.ShortPos = False                    


    def next(self):
        if self.EMA1 > self.EMA2 :  # cross upwards
            if self.position and self.ShortPos == True:
                print('CLOSE SHORT , %.2f' % self.data.close[0])
                self.ShortPos = False
                self.close()

            print('BUY CREATE , %.2f' % self.data.close[0])
            self.LongPos = True
            self.buy()

        elif self.EMA1 < self.EMA2:
            if self.position and self.LongPos ==True:
                print('CLOSE LONG , %.2f' % self.data.close[0])
                self.LongPos = False
                self.close()

#            if not self.p.onlylong:
            print('SELL CREATE , %.2f' % self.data.close[0])
            self.ShortPos = True
            self.sell()



cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = bt.feeds.PandasData(dataname=rawData)

cerebro.adddata(data)  # Add the data feed
cerebro.broker.set_cash(1000) 
cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.run()  # run it all
  # and plot it with a single command

print(cerebro.broker.getvalue())

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize']=[18, 16]
plt.rcParams['figure.dpi']=200
plt.rcParams['figure.facecolor']='w'
plt.rcParams['figure.edgecolor']='k'
cerebro.plot(height= 30, iplot= False)