#!/usr/bin/env python3

import requests, json

class base:

    def __init__(self, base_url = 'https://financialmodelingprep.com/api/v3', api_key = '16906824c31780f13849fc005199d3e4', api = 'FMP', company = 'AAPL'):
        self.price = 0
        self.base_url = base_url
        self.api_key = api_key
        self.company = company
        self.api = api

    def setHeaders(self, headers):
        self.headers = headers
        self.createSession()

    def createSession(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        return self.session

    def getGrade(self):
        search = ''
        fullPath = ''
        if (self.api == 'FMP'):
            search = 'grade'
            fullPath = "{}/{}/{}?apikey={}".format(self.base_url,search,self.company,self.api_key)

        response = self.session.get(fullPath)

        if response.status_code != 200:
            raise Exception(response.status_code)

        resultJson = json.loads(response.text)
        return resultJson

