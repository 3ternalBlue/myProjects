#!/usr/bin/env python3

# 1. Read stocks in my portfolio along with their marker highs(sell) and lows(buy)
# 2. Find current price of the stock
# 3. Check if it's in range of sell/buy
# 4. Also flag if price has dropped significantly compared to 52wk avg (50%?)
# 5. Autogenerate report for those that have alerts. Keep these reports around for a week and then remove them using a cron

import requests, json
import stock as b
import os
import time

def analyseStock(ticker, hi, lo, cost_basis, exclusions = [], type = 'stock'):
    headers = {}
    company = b.stock(company=ticker)
    company.setHeaders(headers)
    response = company.getQuote()

    if response.status_code != 200:
        raise Exception(response.status_code)

    try :
        resultJson = json.loads(response.text)
    except :
        print("API didn't return any data")
    
    alert = 0
    price = float(resultJson[0]['price'])
    priceAvg50 = float(resultJson[0]['priceAvg50'])
    new_data = {}
    new_data[ticker] = {}

    if ticker not in exclusions :
        # Bounds check
        if (price<lo):
            new_data[ticker]["Indicator"] = "Buy"
            new_data[ticker]["Lo Price"] = lo
            alert = 1
        elif (price>hi):
            new_data[ticker]["Indicator"] = "Sell"
            new_data[ticker]["Hi Price"] = hi
            alert = 1
        # Avg check
        if (price < 0.5 * priceAvg50):
            new_data[ticker]["Below 50"] = 1
            new_data[ticker]["priceAvg50"] = priceAvg50
            alert = 1
    else :
        if (price >= cost_basis) :
            new_data[ticker]["Indicator"] = "Sell Shit Stock"
            alert = 1

    # log data if alert is found
    if alert :
        new_data[ticker]["Price"] = price
        new_data[ticker]["Cost Basis"] = cost_basis
        outfile = time.strftime("%Y%m%d") + '_' + type
        existing_data = {}
        try :
            with open(outfile, "r") as f :
                existing_data = json.load(f)
        except :
            existing_data = {}
        
        existing_data.update(new_data)

        with open(outfile, "w") as f :
            json.dump(existing_data, f, indent=4)

    return alert


if __name__=='__main__':
    with open('portfolio.json') as f:
        portfolio = json.load(f)

    with open('crypto.json') as f:
        crypto = json.load(f)

    with open('exclusion_list') as f:
        exclusions = f.read().splitlines()

    upper_wiggle = 10
    lower_wiggle = 8

    stock_enable = 0
    crypto_enable = 1

    stock_alert = 0
    crypto_alert = 0
    # stocks
    for ticker in portfolio:
        hi = float(portfolio[ticker]['hi'])
        lo = float(portfolio[ticker]['lo'])

        hi_adj = hi - (upper_wiggle/100 * hi)
        lo_adj = lo + (upper_wiggle/100 * lo)

        cost_basis = int(portfolio[ticker]['avg'])
        if (stock_enable):
            stock_alert = stock_alert + analyseStock(ticker,hi,lo,cost_basis,exclusions,type='stock')

    # crypto
    for ticker in crypto:
        hi = float(crypto[ticker]['hi'])
        lo = float(crypto[ticker]['lo'])

        hi_adj = hi - (upper_wiggle/100 * hi)
        lo_adj = lo + (upper_wiggle/100 * lo)

        cost_basis = int(crypto[ticker]['avg'])
        if (crypto_enable):
            crypto_alert = crypto_alert + analyseStock(ticker,hi,lo,cost_basis,type='crypto')


    if (stock_alert):
        os.system(""" osascript -e 'display notification "{}" with title "{}" subtitle "{}"' """.format(stock_alert,"Stock alert found","No of hits"))

    if (crypto_alert):
        os.system(""" osascript -e 'display notification "{}" with title "{}" subtitle "{}"' """.format(crypto_alert,"Crypto alert found","No of hits"))
