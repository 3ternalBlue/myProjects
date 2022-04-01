#!/usr/bin/env python3

import requests, json
import os
import time

import stock as b
from finvizfinance.quote import finvizfinance

'''
Parts of DCF
1. Calculate free cash flow
    a. Sales
    b. Cost of goods sold
    c. Operating expenses
    d. Depreciation
    e. Amortization

2. Calculate WACC
    a. Cost of equity using CAPM (Re = Rf + β(Rm-Rf))
    b. Cost of debt
    c. Corp tax rate

3. Calculate terminal value
    FCFF[n](1 + g)/(WACC - g)

'''

def ulFCF(ebit,tax_rate,non_cash_charges,cwc,cap_ex):
    return ebit * (1-tax_rate) + non_cash_charges + cwc + cap_ex

def wacc(beta):
    return 0.1

def calculateFCF(income_statement, balance_statement, cash_flow_statement, growth_rate):
    periods = 5

    ebit = income_statement[0]['netIncome'] + income_statement[0]['incomeTaxExpense'] + income_statement[0]['interestExpense'] # equivalent to ebitda - d&a
    tax_rate = income_statement[0]['incomeTaxExpense']/income_statement[0]['incomeBeforeTax']
    capex = cash_flow_statement[0]['capitalExpenditure']
    non_cash_charges = cash_flow_statement[0]['depreciationAndAmortization']
    cwc = cash_flow_statement[0]['changeInWorkingCapital']


if __name__=='__main__':

    ticker = 'PLTR'
    log_en = 1

    ## FMP
    headers = {}
    company = b.stock(company=ticker)
    company.setHeaders(headers)

    statement_name = ['income_statement', 'balance_statement', 'cash_flow_statement', 'key_metrics_ttm', 'finviz_fundamentals']
    statement_endpoint = ['getAnnualIncomeStatement', 'getBalanceStatement', 'getCashFlowStatement', 'getKeyMetricsTTM', 'ticker_fundament']
    statement_no = 0
    statement_json = {}

    finviz_stock = finvizfinance(ticker)

    for statement in statement_name:
        if 'finviz' in statement:
            statement_json[statement] = finviz_stock.ticker_fundament()
        else :
            endpoint = 'company.' + statement_endpoint[statement_no] + '()'
            response = eval(endpoint)
            if response.status_code != 200:
                raise Exception(response.status_code)
            try :
                statement_json[statement] = json.loads(response.text)
            except :
                print("API didn't return any data")

        statement_no+= 1
        time.sleep(1)


    ## FINVIZ
    beta = statement_json['finviz_fundamentals']['Beta']
    if not beta.isnumeric() :
        beta = 2

    growth_rate = statement_json['finviz_fundamentals']['EPS next 5Y']
    if not growth_rate.isnumeric() :
        growth_rate = statement_json['finviz_fundamentals']['EPS next Y']

    capex_growth_rate = 0.6 # company specific

    ## Logging
    if log_en:
        outdir = 'company_stats/' + ticker
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        tgt_dir = os.getcwd() + '/' + outdir + '/'

        for filename in statement_name:
            outfile = os.path.join(tgt_dir,filename)

            with open(outfile, "w") as f :
                json.dump(statement_json[filename], f, indent=4)

    #calculateFCF(income_statement = statement_json['income_statement'], balance_statement = statement_json['balance_statement'], cash_flow_statement = statement_json['cash_flow_statement'], growth_rate = growth_rate)
