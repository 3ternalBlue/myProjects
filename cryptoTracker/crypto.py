#!/usr/bin/env python3

import requests, json
import os
import pandas as pd


'''
Currently tracking :
1.  Coinbase (buy/sell)
2.  Celsius (rewards)
3.  Binance (buy/sell)

4.  Blockfi (sends their 1099 MISC and only have stable coin there)

Intention is to be able to parse the csvs generated from each platform to calculate the net gain/loss for a given year
1. Need to combine multiple statements
2. Only care about buy/sell/rewards (transfers shouldn't matter as long as I just have the list of buys/sells)
3. Need to be able to pair up transactions in FIFO manner (for long/short term gain/loss calculation)

Combine info from different csvs into a single dataframe
Split it up according to the crypto (I'm not doing swaps so I don't have to track that)
Need to calculate each time from the beginning of time to know the running amounts that are still left (eg. when reporting for 2022, still need to calculate for 2020/21 since I need to know how much of the oldest buys I can still use)
NOTE : Promo code rewards are taxable
'''

csv_path =  '/Users/sagnikdam/Downloads/Crypto/Codification/'

#def celsius():

#def binance():

def coinbase():
    df = pd.read_csv(csv_path + 'coinbase.csv')
    print(df.head(10))

if __name__=='__main__':
    coinbase()
