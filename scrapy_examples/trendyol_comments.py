import requests 
import json

# product_id = "uzaktan-kumandali-portatif-yurume-ve-kosu-bandi-p-176486497"
product_id = "goz-alti-torba-ve-morluk-koyu-halka-karsiti-yogun-nemlendirici-ile-goz-alti-aydinlatici-krem-50ml-p-809165316"
merchant_id = "951152" # "759017"
# url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/reviews/relax/{product_id}/yorumlar?boutiqueId=61&merchantId={merchant_id}&sav=true&culture=tr-TR&storefrontId=1&RRsocialproofAbTesting=B&logged-in=true&isBuyer=false&channelId=1"
url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/reviews/relax/{product_id}/yorumlar?merchantId={merchant_id}&sav=true&culture=tr-TR&storefrontId=1&RRsocialproofAbTesting=B&logged-in=true&isBuyer=false&channelId=1"
print(url)
r = requests.get(url)
content= r.json() 
script_code = content["result"]["hydrateScript"]
# print(script_code)
index1 = script_code.index("__ =")
index2 = script_code.index("window.TYPageName")
# print(index1, index2, script_code[index1+5:index2-14])
data = json.loads(script_code[index1+5:index2-14])
comments = data["ratingAndReviewResponse"]["ratingAndReview"]["productReviews"]["content"]
for comment in comments:
    print("RATE:", comment["rate"])
    print("COMMENT:", comment["comment"])