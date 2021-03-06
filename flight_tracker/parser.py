#!/usr/bin/env python3

import requests, datetime, json
import finder as f

headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "b4674fdea6msh61d56bb25d7a501p1a18a2jsn62dfaf8ae622"
    }


outgoingFlight = f.finder()
outgoingFlight.setHeaders(headers)

incomingFlight = f.finder()
incomingFlight.setHeaders(headers)

source_array = ["DTW-sky"]
destination_array = ["SJC-sky"]

date = datetime.datetime(2021,12,24)

#querystring = {"query":"Oakland"}
#outgoingFlight.getPlaces(querystring)

result = outgoingFlight.browseQuotes(source_array[0], destination_array[0],date)
print(json.dumps(result, indent=4, sort_keys=True))
