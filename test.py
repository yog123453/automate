#import config
from binance.client import Client
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from time import sleep
import os
from datetime import datetime
import time
import buysell

def DEMA(data,time_period,column):
  EMA = data[column].ewm(span=time_period, adjust=False).mean()


  DEMA= 2* EMA - EMA.ewm(span=time_period,adjust = False).mean()
  return DEMA

client = Client('JhX5uaDGBqtbSBtCTSEW1ogotlC1gr4IarS1m9mkIp6xzGUXt38D7esv1SKCuMj9', 'XPxwmafAN5NPs04NAdY0YqkesEZFV24xqGsqAyvQeTORLeXCyUVdGX0coVfKELtU')


def generate_csv(data):
 columns={'Date':['Date'],'Open':['Open'],'High':['High'],'Low':['Low'],'Close':['Close'],'Adj Close':['Adj Close'],'Volume':['Volume']}
 dfcl = pd.DataFrame(columns)
 dfcl.to_csv('GFG.csv', mode='a', index=False, header=False)
 for candlestick in data[:-1]:
  s=str(candlestick[0])
  can = {
  'Date':[time.strftime('%Y-%m-%d', time.localtime(int(s[:-3])))],
  'Open':[candlestick[1]],
  'High':[candlestick[2]],
  'Low':[candlestick[3]],
  'Close':[candlestick[4]],
  'Adj Close':[candlestick[5]],
  'Volume':[candlestick[6]]
  }
  print(can)
  df = pd.DataFrame(can)
  df.to_csv('GFG.csv', mode='a', index=False, header=False)


def Dema_strategy():
	  recent_candle=client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE,"1 day ago UTC")
	  recent_candle1=0
	  for candle in recent_candle:
	  	prev_candle=recent_candle1
	  	recent_candle1=candle	  	
	  s=str(prev_candle[0])
	  print('prev_candle ....'+str(prev_candle))
	  can = {'Date':[time.strftime('%Y-%m-%d', time.localtime(int(s[:-3])))],'Open':[prev_candle[1]],'High':[prev_candle[2]],'Low':[prev_candle[3]],'Close':[prev_candle[4]],'Adj Close':[prev_candle[5]],'Volume':[prev_candle[6]]}
	  df = pd.DataFrame(can)
	  df.to_csv('GFG.csv', mode='a', index=False, header=False)
	  df['DEMA_short'] = DEMA(df,10,'Close')
	  df['DEMA_long'] = DEMA(df,50,'Close')
	  if(df['DEMA_long'][:-1] < df['DEMA_short'][:-1]):
	  	buy()
	  else:
	  	sell()

    
 
# candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE)

# 
# 




# 
# candlestick_writer.writerow(headers)

# for candlestick in candles:
# 	print(candlestick)

# 	candlestick_writer.writerow(candlestick)


# print(len(candles))

#klines=client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE,"24 Apr 2022","04 May 2022")


#klines=client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY,"365 days ago UTC")
#print(klines)


def run():
    while datetime.now().minute not in {0, 15, 30, 45}:  # Wait 1 second until we are synced up with the 'every 15 minutes' clock
        sleep(1)

    def task():
        # Your task goes here
        # Functionised because we need to call it twice
        temperature_store()
    
    Dema_strategy()

    while True:
    	sleep(60*15)
    	Dema_strategy()


def main():
 if os.stat("GFG.csv").st_size != 0:
  print('must delete')
  os.remove('GFG.csv')
 klines=client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE,"200 days ago UTC")
 generate_csv(klines)
 print('finished')
 run()

 


if __name__ == '__main__':
	main()


