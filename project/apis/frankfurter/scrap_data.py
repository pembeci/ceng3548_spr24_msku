import requests
import traceback
import json

BASE_URL = "https://api.frankfurter.app"

try: 
    inp_currency = "TRY"
    out_currencies = "EUR,USD,GBP"
    years = [2020, 2021, 2022]
    for year in years:
        for out_curreny in out_currencies.split(","):
            url = f"{BASE_URL}/{year}-01-01..{year}-12-31?from={inp_currency}&to={out_curreny}"
            r = requests.get(url)
            result =  r.json()
            filename = f"{out_curreny}_{year}.json"
            outfile = open(filename, "w")
            data = result["rates"]
            outfile.write(json.dumps(data))
            outfile.close()
except Exception as e:
    print(traceback.format_exc())
    if "message" in result: 
        print(f"API Error: {result['message']}")

