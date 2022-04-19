#!/usr/bin/env python3

import requests, json
import os
import time

import stock as b
from finvizfinance.quote import finvizfinance
import yfinance as yf

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

def generateWeights(length): # for weighted growth rate over the last few years
    total = (length * (length + 1))/2
    weight_list = []
    for i in range(1,length+1):
        weight_list.append(i/total)
    return weight_list

def growthRate(statement_json):
    growth_list = []
    for statement in statement_json['financial_growth'] :
        if (statement['revenueGrowth']!=0): # can also use freeCashFlowGrowth; but those numbers were huge in some cases
            growth_list.append(statement['revenueGrowth'])

    items = (len(growth_list))
    weight_list = generateWeights(items)
    weight_list.reverse()

    weighted_growth = [weight_list[i] * growth_list[i] for i in range(items)]
    effective_growth_rate = sum(weighted_growth)

    return effective_growth_rate

def FCF(ebit,tax_rate,non_cash_charges,cwc,capex):
    return ebit * (1-tax_rate) + non_cash_charges + cwc + capex

def calculateFCF(statement_json, beta, rfr = 0.019, terminal_rate = 0.025):
    periods = 5

    income_statement = statement_json['income_statement']
    cash_flow_statement = statement_json['cash_flow_statement']
    balance_statement = statement_json['balance_statement']

    ebit = income_statement[0]['netIncome'] + income_statement[0]['incomeTaxExpense'] + income_statement[0]['interestExpense'] # equivalent to ebitda - d&a
    tax_rate = income_statement[0]['incomeTaxExpense']/income_statement[0]['incomeBeforeTax']
    capex = cash_flow_statement[0]['capitalExpenditure']
    non_cash_charges = cash_flow_statement[0]['depreciationAndAmortization']
    cwc = cash_flow_statement[0]['changeInWorkingCapital']

    growth = growthRate(statement_json)
    if growth<0 :
        growth = terminal_rate # FLAG : giving it leniancy that it at least keeps up with the economy



    fcff = []
    #fcff.append(FCF(ebit, tax_rate, non_cash_charges, cwc, capex)) # current value
    fcff.append(cash_flow_statement[0]['freeCashFlow'])

    for period in range(1,periods+1):
        if fcff[period-1]<0:
            fcff.append(fcff[period-1] * (1-growth))
        else :
            fcff.append(fcff[period-1] * (1+growth))

    wacc = WACC(statement_json, tax_rate, rfr, beta)

    TV = terminalValue(fcff[-1], wacc, terminal_rate)
    fcff[-1] = fcff[-1] + TV

    fcff = fcff[1:] # removing yr 0 value

    discounted_fcff = []
    for period in range(len(fcff)):
        discounted_fcff.append(fcff[period]/((1+wacc)**(period+1)))

    EV = sum(discounted_fcff)
    PV = EV - balance_statement[0]['netDebt']

    shares = income_statement[0]['weightedAverageShsOutDil']
    dcf_value = PV/shares

    print("----Effective Tax Rate----")
    print(tax_rate)
    print("----Effective Growth Rate----")
    print(growth)
    print("----WACC----")
    print(wacc)
    print("----FCFF----")
    print(fcff)
    print("----Discounted FCFF----")
    print(discounted_fcff)

    print("----Enterprise value calculated----")
    print(EV)
    print("----Present value calculated----")
    print(PV)
    print("----DCF value----")
    print(dcf_value)

def costOfDebt(statement_json, tax_rate):
    # interest_expense/total_debt * (1 - tax_rate)

    income_statement = statement_json['income_statement']
    balance_statement = statement_json['balance_statement']

    interest_expense = income_statement[0]['interestExpense']
    total_debt = balance_statement[0]['totalDebt']

    cost_of_debt = interest_expense/total_debt * (1 - tax_rate)

    return cost_of_debt

def costOfEquity(rfr, beta):
    # market_risk_premium = (required_return - risk_free_rate) # can be conservative and keep this at 5%
    # risk_free_rate + beta * (market_risk_premium)

    market_risk_premium = 0.08 - rfr
    return rfr + beta*market_risk_premium

def WACC(statement_json, tax_rate, rfr, beta):
    # E = shares_outstanding * share_price (market cap)
    # D = total_debt
    # EV = E + D

    # wacc = D/EV * costOfDebt + E/EV * costOfEquity

    cost_of_debt = costOfDebt(statement_json, tax_rate)
    if cost_of_debt<0 :
        cost_of_debt = 0 # FLAG : it's possible that the company is making more from interests than it's losing

    cost_of_equity = costOfEquity(rfr, beta)

    balance_statement = statement_json['balance_statement']
    D = balance_statement[0]['totalDebt']

    enterprise_values = statement_json['enterprise_values']
    income_statement = statement_json['income_statement']
    E = enterprise_values[0]['stockPrice'] * income_statement[0]['weightedAverageShsOutDil']

    print("----Beta----")
    print(beta)
    print("----Enterprise Value based on stock price on date----")
    print(enterprise_values[0]['date'])
    print(E)
    print("----Cost of debt----")
    print(cost_of_debt)
    print("----Cost of equity----")
    print(cost_of_equity)

    return (D/(D + E) * cost_of_debt) + (E/(E + D) * cost_of_equity)

def terminalValue(fcfn, wacc, terminal_rate):
    if fcfn<0:
        return (fcfn * (1 - terminal_rate)) / (wacc - terminal_rate)
    else :
        return (fcfn * (1 + terminal_rate)) / (wacc - terminal_rate)

if __name__=='__main__':

    ticker = 'OKTA'
    log_en = 1
    fmp_en = 1
    yfi_en = 1

    yfi_en1 = 0

    ## FMP
    if fmp_en:
        headers = {}
        company = b.stock(company=ticker)
        company.setHeaders(headers)

        statement_name = ['income_statement', 'balance_statement', 'cash_flow_statement', 'key_metrics_ttm', 'financial_growth', 'enterprise_values']# 'finviz_fundamentals']
        statement_endpoint =    {'income_statement'     : 'getAnnualIncomeStatement',
                                'balance_statement'     : 'getBalanceStatement',
                                'cash_flow_statement'   : 'getCashFlowStatement',
                                'key_metrics_ttm'       : 'getKeyMetricsTTM',
                                'financial_growth'      : 'getFinancialGrowth',
                                'enterprise_values'     : 'getEnterpriseValues',
                                'finviz_fundamentals'   : 'ticker_fundament'}
        statement_json = {}

        finviz_stock = finvizfinance(ticker)

        for statement in statement_name:
            if 'finviz' in statement:
                continue # finviz API seems to be broken
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


        ## FINVIZ
        #beta = statement_json['finviz_fundamentals']['Beta']
        #if not beta.isnumeric() :
        #    beta = 2

        #growth_rate = statement_json['finviz_fundamentals']['EPS next 5Y']
        #if not growth_rate.isnumeric() :
        #    growth_rate = statement_json['finviz_fundamentals']['EPS next Y']

    ## Yahoo Finance
    if yfi_en1:
        url = "https://yfapi.net/v6/finance/quote"
        querystring = {"symbols":"AAPL"}
        headers = {
        'x-api-key': "VJTSOAMkfW81zs8O1IAox6hHXIWCtvSm7sJuaGT0"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        yfi_json = json.loads(response.text)
        print(json.dumps(yfi_json, indent=4))

    if yfi_en:
        yf_stock = yf.Ticker(ticker)
        beta = yf_stock.info['beta']
        if beta is None :
            beta = 2

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

    calculateFCF(statement_json, beta)
