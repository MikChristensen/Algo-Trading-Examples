from datetime import datetime
import backtrader as bt
from backtrader.indicators import SMA
from GetData import getData
import numpy as np
import matplotlib as plt


date = '2022-05-16'
symbol = 'googl'
interval = '1m'
period = '5d'

getdata = getData()
rawData = getdata.getHistoryYfinance(symbol=symbol, interval=interval, period=period, start=date)

class SmaCross(bt.Strategy):
    
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=40,  # period for the fast moving average - Default 10
        pslow=100   # period for the slow moving average - Default 30
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        self.sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.sma = 0 
        
        #self.TA_fastSMA = bt.SMA(self.data.Close,3)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, self.sma2)  # crossover signal            

    def next(self):
        if self.crossover > 0.0 and (self.sma * 1.0001) < self.sma2[0]:  # cross upwards
            if self.position:
                print('CLOSE SHORT , %.2f' % self.data.close[0])
                self.close()

            print('BUY CREATE , %.2f' % self.data.close[0])
            self.buy()

        elif self.crossover < 0.0 and (self.sma) > self.sma2[0]:
            if self.position:
                print('CLOSE LONG , %.2f' % self.data.close[0])
                self.close()

#            if not self.p.onlylong:
            print('SELL CREATE , %.2f' % self.data.close[0])
            self.sell()

        self.sma = self.sma2[0] 


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = bt.feeds.PandasData(dataname=rawData)

cerebro.adddata(data)  # Add the data feed
#cerebro.broker.setcommission(0) 
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