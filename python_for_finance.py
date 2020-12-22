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

"""

To run through df.index, id est, its date column and see if the Close price
is lower than the simple moving average or not

for i in df.index:
    #print(df.iloc[:,6][i])
    #print(df[smaString][i])
    if(df["Adj Close"][i] > df[smaString][i]):
        print("The Close is higher with: " + str(df["Adj Close"][i]))
    else:
        print("The Close is lower with: " + str(df["Adj Close"][i]))
"""

emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60]
for x in emasUsed:
	ema=x
	df[f"Ema_{ema}"]=round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)


df=df.iloc[60:]

pos=0
num=0
percentchange=[]

for i in df.index:
	cmin=min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i],)
	cmax=max(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i],)

	close=df["Adj Close"][i]
	
	if(cmin>cmax):
		print("Red White Blue")
		if(pos==0):
			bp=close
			pos=1
			print(f"Buying now at {bp} ")


	elif(cmin<cmax):
		print("Blue White Red")
		if(pos==1):
			pos=0
			sp=close
			print(f"Selling now at {sp} ")
			pc=(sp/bp-1)*100
			percentchange.append(pc)
	if(num==df["Adj Close"].count()-1 and pos==1):
		pos=0
		sp=close
		print(f"Selling now at {sp} ")
		pc=(sp/bp-1)*100
		percentchange.append(pc)

	num+=1

print(percentchange)

gains=0
ng=0
losses=0
nl=0
totalR=1

for i in percentchange:
	if(i>0):
		gains+=i
		ng+=1
	else:
		losses+=i
		nl+=1
	totalR=totalR*((i/100)+1)

totalR=round((totalR-1)*100,2)

if(ng>0):
	avgGain=gains/ng
	maxR=str(max(percentchange))
else:
	avgGain=0
	maxR="undefined"

if(nl>0):
	avgLoss=losses/nl
	maxL=str(min(percentchange))
	ratio=str(-avgGain/avgLoss)
else:
	avgLoss=0
	maxL="undefined"
	ratio="inf"

if(ng>0 or nl>0):
	battingAvg=ng/(ng+nl)
else:
	battingAvg=0

print()
print(f"Results for {stock} going back to {df.index[0]} Sample size: {ng+nl} trades")
print(f"EMAs used: {emasUsed} ")
print(f"Batting Avg: {battingAvg} ")
print(f"Gain/loss ratio: {ratio} ")
print(f"Average Gain: {avgGain} ")
print(f"Average Loss: {avgLoss} ")
print(f"Max Return: {maxR} ")
print(f"Max Loss: {maxL} ")
print(f"Total return over {ng+nl} trades: {totalR}% ")
#print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()