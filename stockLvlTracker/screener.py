#!/usr/bin/env python3

import requests, json

class screener:

    def __init__(self, base_url = 'https://financialmodelingprep.com/api/v3', api_key = '16906824c31780f13849fc005199d3e4', marketCapMoreThan = 10000000000, marketCapLowerThan = None, betaMoreThan = 1, volumeMoreThan = 10000, sector = 'Technology', limit = 100):
        self.base_url = base_url
        self.api_key = api_key
        self.marketCapMoreThan = str(marketCapMoreThan)
        self.marketCapLowerThan = str(marketCapLowerThan)

        self.priceMoreThan = None
        self.priceLowerThan = None

        self.betaMoreThan = str(betaMoreThan)
        self.betaLowerThan = None

        self.volumeMoreThan = str(volumeMoreThan)
        self.volumeLowerThan = None

        self.dividendMoreThan = None
        self.dividendLowerThan = None

        self.isEtf = str(False)
        self.isActivelyTrading = str(True)

        self.sector = sector

        self.Industry = None
        #Autos | Banks | Banks Diversified | Software | Banks Regional | Beverages Alcoholic | Beverages Brewers | Beverages Non-Alcoholic
    
        self.Country = 'US'

        self.exchange = None
        #nyse | nasdaq | amex | euronext | tsx | etf | mutual_fund

        self.limit = str(limit)


    def createSession(self, headers = {}):
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        return self.session

    def getScreenedValues(self):
        search_base = 'stock-screener'

        search_modifier = ''

        if (self.marketCapMoreThan):
            search_modifier += 'marketCapMoreThan=' + self.marketCapMoreThan + '&'
        elif (self.marketCapLowerThan):
            search_modifier += 'marketCapLowerThan=' + self.marketCapLowerThan + '&'

        if (self.betaMoreThan):
            search_modifier += 'betaMoreThan=' + self.betaMoreThan + '&'
        elif (self.betaLowerThan):
            search_modifier += 'betaLowerThan=' + self.betaLowerThan + '&'

        if (self.volumeMoreThan):
            search_modifier += 'volumeMoreThan=' + self.volumeMoreThan + '&'
        elif (self.volumeLowerThan):
            search_modifier += 'volumeLowerThan=' + self.volumeLowerThan + '&'

        if (self.dividendMoreThan):
            search_modifier += 'dividendMoreThan=' + self.dividendMoreThan + '&'
        elif (self.dividendLowerThan):
            search_modifier += 'dividendLowerThan=' + self.dividendLowerThan + '&'

        if (self.priceMoreThan):
            search_modifier += 'priceMoreThan=' + self.priceMoreThan + '&'
        elif (self.priceLowerThan):
            search_modifier += 'priceLowerThan=' + self.priceLowerThan + '&'


        if (self.isEtf):
            search_modifier += 'isEtf=' + self.isEtf + '&'

        if (self.isActivelyTrading):
            search_modifier += 'isActivelyTrading=' + self.isActivelyTrading + '&'

        if (self.sector):
            search_modifier += 'sector=' + self.sector + '&'

        if (self.limit):
            search_modifier += 'limit=' + self.limit + '&'

        if (self.Country):
            search_modifier += 'Country=' + self.Country + '&'

        if (self.Industry):
            search_modifier += 'Industry=' + self.Industry + '&'

        if (self.exchange):
            search_modifier += 'exchange=' + self.exchange + '&'

        if (search_modifier):
            search_modifier.strip('&')

        fullPath = "{url}/{search_base}?{search_modifier}apikey={apikey}".format(url = self.base_url,search_base = search_base, search_modifier = search_modifier,apikey = self.api_key)

        response = self.session.get(fullPath)
        return response
