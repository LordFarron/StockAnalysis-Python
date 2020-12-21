import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

stock = input("Enter a stock ticker simbol: ")


startYear = 2019
startMonth = 1
startday = 1

start = dt.datetime(startYear, startMonth, startday)

now = dt.datetime.now()

df = pdr.get_data_yahoo(stock, start, now)
#print(df)

ma = 50

smaString = f"Sma_{ma}"

df[smaString] = df.iloc[:,4].rolling(window = ma).mean()
#print(df)

df = df.iloc[ma:]
#print(df)

for i in df.index:
    #print(df.iloc[:,6][i])
    #print(df[smaString][i])
    if(df["Adj Close"][i] > df[smaString][i]):
        print("The Close is higher with: " + str(df["Adj Close"][i]))
    else:
        print("The Close is lower with: " + str(df["Adj Close"][i]))