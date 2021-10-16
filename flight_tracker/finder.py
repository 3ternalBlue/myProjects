#!/usr/bin/env python3

import requests, datetime, json

class finder:

    def __init__(self, originCountry = "US", currency = "USD", locale = "en-US", rootURL="https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"):
        self.currency = currency
        self.locale =  locale
        self.rootURL = rootURL
        self.originCountry = originCountry
        self.airports = {}
        self.quotes = []
        self.places = []
        self.carriers = []

    def setHeaders(self, headers):
        self.headers = headers
        self.createSession()

    def getHeaders(self):
        print(self.headers)

    def createSession(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        return self.session

    def browseQuotes(self, source, destination, date, print=False):
        quoteRequestPath = "/apiservices/browsequotes/v1.0/"
        browseQuotesUrl = self.rootURL + quoteRequestPath + self.originCountry + "/" + self.currency + "/" + self.locale + "/" + source + "/" + destination + "/" + date.strftime("%Y-%m-%d")

        response = self.session.get(browseQuotesUrl)
        resultJson = json.loads(response.text)
        return resultJson

    def getPlaces(self,params):
        placeRequestPath = "/apiservices/autosuggest/v1.0/"
        getPlaceUrl = self.rootURL + placeRequestPath + self.originCountry + "/" + self.currency + "/" + self.locale + "/"
        response = self.session.get(getPlaceUrl,params=params)
        resultJson = json.loads(response.text)
        print(json.dumps(resultJson, indent=4, sort_keys=True))

    def getQuotes(self):
        return self.quotes

    def getAirports(self):
        return self.airports
