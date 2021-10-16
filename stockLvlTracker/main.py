#!/usr/bin/env python3

import requests, json
import stock_base as b

# intention here is to track a list of stocks and indicate in case any of them rises/falls significantly from the 52wk avg 


def main():
    headers = {}
    aapl = b.base()
    aapl.setHeaders(headers)
    result = aapl.getGrade()
    print(json.dumps(result, indent=4, sort_keys=True))


if __name__=='__main__':
    main()
