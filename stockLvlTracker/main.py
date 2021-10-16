#!/usr/bin/env python3

import requests, json
import stock_base as b
import screener as s

# intention here is to track a list of stocks and indicate in case any of them rises/falls significantly from the 52wk avg 

def getSectorsList():
    sectors = [
            'Basic Materials',
            'Communication Services',
            'Consumer Cyclical',
            'Consumer Defensive',
            'Energy',
            'Financial Services',
            'Healthcare',
            'Industrial Goods',
            'Industrials',
            'Real Estate',
            'Technology',
            'Utilities',
            'Conglomerates'
            ]
    return sectors

def main():
    headers = {}
    company = b.stock(company='VGFC')
    company.setHeaders(headers)
    #response = company.getRating()
    #response = company.getProfile()

    screener = s.screener(sector = 'Technology')
    screener.createSession()
    response = screener.getScreenedValues()

    if response.status_code != 200:
        raise Exception(response.status_code)

    try :
        resultJson = json.loads(response.text)

        #print(json.dumps(resultJson, indent=4, sort_keys=True))
        with open("outfile.json", "w") as outfile:
            json.dump(resultJson, outfile, indent=4, sort_keys=True)
    except :
        print("Company didn't return any data")

def test():
    with open('outfile.json') as f:
        data = json.load(f)

    print(len(data))

if __name__=='__main__':
    main()
    #test()
