#!/usr/bin/env python3
import requests, json
import time
import os
import sys
sys.path.insert(0,'/Users/sagnikdam/myProjects/stockLvlTracker')

import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

import stock as b
from finvizfinance.quote import finvizfinance

def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.1f%s' % (num, ['', 'K', 'M', 'B', 'T'][magnitude])

def plot_stats(statement_json, ticker, stat = 'revenue'):

    ## Income statement stats ##
    date_list = []
    value_list = []
    statement_set = statement_json['income_statement']
    for statement in reversed(statement_set) : # parse the list
        value_list.append(statement[stat])
        date_list.append(statement['calendarYear'])

    col = []
    for val in value_list:
        if val >= 0:
            col.append('green')
        else:
            col.append('red')

    plt.figure()
    plt.bar(date_list, value_list, color=col)

    plt.xlabel('Year')
    plt.ylabel(stat)
    plt.title(ticker)

    formatter = FuncFormatter(human_format)
    plt.gcf().axes[0].yaxis.set_major_formatter(formatter)
    #plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    #plt.yticks(np.arange(min(value_list), max(value_list)+1, 1000000000))
    #plt.show()

    outdir = ticker + '/plots'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    tgt_dir = os.getcwd() + '/' + outdir + '/'
    tgt_file = tgt_dir + stat
    plt.savefig(tgt_file)


if __name__=='__main__':

    ticker = 'OKTA'

    ## FMP
    headers = {}
    company = b.stock(company=ticker)
    company.setHeaders(headers)

    statement_name = ['income_statement']
    statement_endpoint = {'income_statement'    : 'getAnnualIncomeStatement'}
    statement_json = {}

    finviz_stock = finvizfinance(ticker)

    for statement in statement_name:
        if os.path.exists(ticker + '/' + statement):
            f = open(ticker + '/' + statement)
            statement_json[statement] = json.load(f)
            f.close()
        else :
            continue
            if 'finviz' in statement:
                statement_json[statement] = finviz_stock.ticker_fundament()
            else :
                endpoint = 'company.' + statement_endpoint[statement] + '()'
                response = eval(endpoint)
                if response.status_code != 200:
                    raise Exception(response.status_code)
                try :
                    statement_json[statement] = json.loads(response.text)
                except :
                    print("API didn't return any data")

            time.sleep(1)

    key_stats = {}
    key_stats['income_statement'] = ['revenue', 'costOfRevenue', 'operatingExpenses', 'netIncome', 'weightedAverageShsOut']

    for key in key_stats:
        for stat in key_stats[key]:
            plot_stats(statement_json, ticker, stat)
