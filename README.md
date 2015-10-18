# factual2csv
Generate CSV from Factual API places query

## Dependencies

Requires: `factual-api` `json` `csv`

Install: `pip install factual-api json csv`

## Usage

Edit factual2csv.py to your application:

1. Input your Factual API account details. Only change `premium_account` and `result_limit` if you have a fancy premium account.
   ```python
   factual_key     = '[YOUR FACTUAL API KEY]'
   factual_secret  = '[YOUR FACTUAL SECRET KEY]'
   premium_account = False
   result_limit    = 50
   ```

2. Head over to Factual's Website and input the queries you wish to CSV-ify. Then, take note of the query URL and copy that info as you'll use it for the script. Example: `https://www.factual.com/data/t/places#filters={"$and":[{"country":{"$eq":"US"}},{"region":{"$eq":"CA"}}]}&q=McDonalds`

* **Important!** Make sure you replace any +'s in your filter string with spaces when you copy it over to the script! The query parameters should not be URL encoded

3. Edit 'info_desired' to reflect the keys you wish to record and add your queries to the 'places' dictionary. Query and/or filter required; table defaults to 'places'. The dictionary keys will be the filenames for the output csv files.
   ```python
   info_desired = ('name', 'address', 'locality', 'region', 'postcode', 'longitude', 'latitude')

   places = {
       'cali_mcds': {
           "table" : "restaurants-us",
           "query" : "McDonalds",
           "filter": {"$and":[{"country":{"$eq":"US"}},{"region":{"$eq":"CA"}}]}
       }
   }
   ```

4. Run the script! `./factual2csv.py`

## Limitations

* Factual API limits free users to 500 results for any query