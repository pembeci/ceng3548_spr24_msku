import requests
import traceback

BASE_URL = "https://api.frankfurter.app"

try: 
    inp_currency = input("Currency: ")
    url = f"{BASE_URL}/latest?from={inp_currency}&to=EUR,USD,GBP"
    r = requests.get(url)
    result =  r.json()
    for cur_name, cur_val in result["rates"].items():
        print(f"{cur_name}: {cur_val}")
    url = f"{BASE_URL}/2020-01-01..2020-02-28?from={inp_currency}&to=USD"
    print(url)
    r = requests.get(url)
    result =  r.json()
    for date_val, dates_dict in result["rates"].items():
        for cur_name, cur_val in dates_dict.items():
            print(f"{date_val} -- {cur_name}: {cur_val}")
except Exception as e:
    print(traceback.format_exc())
    if "message" in result: 
        print(f"API Error: {result['message']}")

