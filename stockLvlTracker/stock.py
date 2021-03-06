#!/usr/bin/env python3

import requests, json

class stock:

    def __init__(self, base_url = 'https://financialmodelingprep.com/api/v3', api_key = '16906824c31780f13849fc005199d3e4', api = 'FMP', company = 'AAPL'):
        self.price = 0
        self.base_url = base_url
        self.api_key = api_key
        self.api = api
        self.company = company

    def setHeaders(self, headers):
        self.headers = headers
        self.createSession()

    def createSession(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        return self.session

    def getDcf(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'discounted-cash-flow'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getQuote(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'quote'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getHistoricalChart(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'historical-chart/1min'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getProfile(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'profile'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    # This is the FMP calculated rating based on dcf, pe and other factors
    def getRating(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'rating'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getEarningsSurprises(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'earnings-surprises'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getAnnualIncomeStatement(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'income-statement'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getBalanceStatement(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'balance-sheet-statement'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getCashFlowStatement(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'cash-flow-statement'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getKeyMetricsTTM(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'key-metrics-ttm'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getFinancialGrowth(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'financial-growth'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response

    def getEnterpriseValues(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'enterprise-values'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)
        return response


