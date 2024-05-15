from pyfacebook import GraphAPI
import requests
APP_ID = "420558760718042"
APP_SECRET = "89d27ca96585b64d2d45ad63a8b6a175"
TOKEN = "EAAFZBfveKLtoBO7ksFH2Rxns0vn9UaG3eudqLpZBwioFrWN0jVKF0F6GZBwxH3R6sSmxSZBLpPnRS3qxGiJTjEfG8CPP5frSXTharZBPUkDe4DZAx7CIzTNGv68s4xBDMq7mOVYY7ENrwBquNDEGkuMap1pgmIiI2cZAt2rfqO7IS8skiNaJ5vIYapnLgBNLZAhmFrucIlpkSsQz3mfwXuUTuy5S3KEeZCDZCtP1u5xH3h9nYviOzOkyICahuSwR8fbibThi4z90mPxhwZD"

# api = GraphAPI(app_id=APP_ID, app_secret=APP_SECRET, application_only_auth=True)
api = GraphAPI(access_token=TOKEN)
result = api._request("/me?fields=id,name")
print(result.json())
params = "fields=id,name"
url = f"https://graph.facebook.com/v19.0/me?{params}&access_token={TOKEN}"
r = requests.get(url)
print(r.json())