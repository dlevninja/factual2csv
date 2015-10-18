#! /usr/bin/env python

from factual import Factual
import json
import csv

# ----------------------------------------------------------
# Factual account params
# ----------------------------------------------------------

factual_key     = '[YOUR FACTUAL API KEY]'
factual_secret  = '[YOUR FACTUAL SECRET KEY]'
premium_account = False
result_limit    = 50

# ----------------------------------------------------------
# Search parameters
# ----------------------------------------------------------

info_desired = ('name', 'address', 'locality', 'region', 'postcode', 'longitude', 'latitude')

places = {
    'cali_mcds': {
        "table" : "restaurants-us",
        "query" : "McDonalds",
        "filter": {"$and":[{"country":{"$eq":"US"}},{"region":{"$eq":"CA"}}]}
    }
}

# ----------------------------------------------------------
# Begin script
# ----------------------------------------------------------

factual      = Factual(factual_key, factual_secret)
places_info  = {}

# ----------------------------------------------------------
# loop thru each specified place type and filter

for place_name, place_params in places.iteritems():

    offset = 0

    # ----------------------------------------------------------
    # build api request for filter (table defaults to 'places')

    place_table = "places" if ("table" not in place_params) else place_params["table"]
    place_req = factual.table(place_table)

    if "query" in place_params:
        place_req = place_req.search(place_params["query"])

    if "filter" in place_params:
        place_req = place_req.filters(place_params["filter"])

    places_info[place_name] = []

    # ----------------------------------------------------------
    # make request

    while 1:
        place_data = place_req.offset(offset).limit(result_limit).data()

        # loop thru the places that were returned
        for result in place_data:

            result_data = {}

            # loop thru the values of info we want (ex. name, address...) and if the info exists, record it
            for info in info_desired:
                if info in result:
                    result_data[info] = result[info]
                else:
                    result_data[info] = None

            places_info[place_name].append(result_data)


        # ----------------------------------------------------------
	# if we get ${result_limit} results, keep requesting cause there might be more
        # if no premium account, max results offset is 500

        if ( len(place_data) == result_limit ):
            offset = offset + result_limit

            if ( premium_account ) or ( not(premium_account) and (offset < 500) ):
                continue
        
        break

# loop thru data that's been collected and dump it to a csv
for place_name, place_info in places_info.iteritems():

    with open(place_name + ".csv", "w") as file:
        csv_w = csv.DictWriter(file, info_desired)
        csv_w.writeheader()
        csv_w.writerows(place_info)
    
    print "wrote " + place_name + ".csv"
