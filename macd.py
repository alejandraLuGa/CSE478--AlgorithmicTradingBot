import yfinance as yf 
import numpy
import pandas 
import matplotlib.pyplot as plt
import mplfinance as mpf

spy = yf.download('SPY')
#print (spy)
spy.head()

#calculating MACD for 12 ans 26 day EMA line 
spy['EMA12'] = spy['Close'].ewm(span=12).mean()
spy['EMA26'] = spy['Close'].ewm(span=26).mean()
spy['MACD'] = spy['EMA26'] - spy['EMA12']

#9 day exponential moving average of the macd
spy['MACDSignalLine'] = spy['MACD'].ewm(span=9).mean()
spy['Histogram'] = spy['MACD'] - spy['MACDSignalLine']


#make plot 
apds = [mpf.make_addplot(spy['EMA12'][-100:], color='yellow'),
        mpf.make_addplot(spy['EMA26'][-100:], color='c'),
        mpf.make_addplot(spy['MACD'][-100:], panel=1, secondary_y=True, color='orange'),
        mpf.make_addplot(spy['MACDSignalLine'][-100:], panel=1, secondary_y=True, color='blue'),
        mpf.make_addplot(spy['Histogram'][-100:], panel=1, type='bar', color='purple', secondary_y=False)]


# Create my own `marketcolors` to use with the `nightclouds` style:
mc = mpf.make_marketcolors(up='#00ff00',down='#ff2e2e',inherit=True)

# Create a new style based on `nightclouds` but with my own `marketcolors`:
s  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=mc)

fig, axes = mpf.plot(spy[-100:], 
                     volume_panel = 2,
                     figratio=(1.5,1),
                     figscale=1, 
                     type='candle', 
                     style=s,
                     addplot=apds,
                     returnfig=True)

labels = ['EMA12', 'EMA26']

axes[0].legend(labels, loc='upper left')
axes[2].legend(['MACD - Signal'], fontsize=6, loc='upper right')
axes[3].legend(['MACD', 'Signal Line'], fontsize=6, loc='lower left')

axes[0].set_title('SPY Technical Analysis')

