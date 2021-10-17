#!/usr/bin/env python3

import requests, json
import stock as b
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

def getStockData(company):
    headers = {}
    company = b.stock(company=company)
    company.setHeaders(headers)
    #response = company.getRating()
    #response = company.getProfile()
    response = company.getEarningsSurprises()
    #response = company.getDcf() # already included in profile

    if response.status_code != 200:
        raise Exception(response.status_code)

    try :
        resultJson = json.loads(response.text)
        with open("stockfile.json", "w") as outfile:
            json.dump(resultJson, outfile, indent=4, sort_keys=True)
    except :
        print("API didn't return any data")

    print(json.dumps(resultJson, indent=4, sort_keys=True))
    return resultJson

def getScreenerData():
    screener = s.screener(sector = 'Healthcare', limit='')
    screener.createSession()
    response = screener.getScreenedValues()

    if response.status_code != 200:
        raise Exception(response.status_code)

    try :
        resultJson = json.loads(response.text)
        with open("screenfile.json", "w") as outfile:
            json.dump(resultJson, outfile, indent=4, sort_keys=True)
    except :
        print("API didn't return any data")

    return resultJson

def getFileData(file):
    with open(file) as f:
        data = json.load(f)

def main():
    responseJson = getStockData('T')
    #responseJson = getScreenerData()


if __name__=='__main__':
    main()
    #test()
