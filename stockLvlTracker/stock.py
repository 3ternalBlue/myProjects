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

