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

def analyseStock(ticker,hi,lo,cost_basis,exclusions):
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
        outfile = time.strftime("%Y%m%d")
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

    with open('exclusion_list') as f:
        exclusions = f.read().splitlines()

    upper_wiggle = 10
    lower_wiggle = 8

    alert = 0
    for ticker in portfolio:
        hi = int(portfolio[ticker]['hi'])
        lo = int(portfolio[ticker]['lo'])

        hi_adj = hi - (upper_wiggle/100 * hi)
        lo_adj = lo + (upper_wiggle/100 * lo)

        print(hi_adj,lo_adj)

        cost_basis = int(portfolio[ticker]['avg'])
        alert = analyseStock(ticker,hi,lo,cost_basis,exclusions)

        if (alert):
            os.system(""" osascript -e 'display notification "{}" with title "{}"' """.format("Alert found", "Stock spike identifier"))
