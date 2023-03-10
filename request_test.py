import requests,json
import paypayopa
import time
from local_settings import *

#policyの指定
policyLocator = '100003300'

#policyの取得
response = requests.get(
    'http://api.sandbox.socotra.com/policy/'+ policyLocator,
    headers = {
        "Authorization": SOCOTRA_BEARER
    },
)
print(response)

#policy情報の取り出し
found_policy = response.json()
policy_id = found_policy['displayId']
policy_info = found_policy['characteristics']

#保険料の取り出し
grossPremium = int(policy_info[0]["grossPremium"])
print(grossPremium)

#payapyでの支払い
client = paypayopa.Client(auth=(API_KEY, API_SECRET), production_mode=False)
client.set_assume_merchant("618078603656470528")

# requestの送信情報について
# => https://www.paypay.ne.jp/opa/doc/jp/v1.0/preauth_capture#operation/createAuth
request = {
    "merchantPaymentId": round(time.time()), # => 加盟店発番のユニークな決済取引ID
    "codeType": "ORDER_QR",
    "redirectUrl": "http://shojiro_test.com", # => ここを任意のフロントのアプリにしてあげれば良さそう
    "redirectType": "WEB_LINK",
    "orderDescription":"Moonshot - shojiro_insurance",
    "orderItems": [{
        "name": "Moon cake",
        "category": "pasteries",
        "quantity": 1,
        "productId": "67678",
        "unitPrice": {
            "amount": grossPremium,
            "currency": "JPY"
        }
    }],
    "amount": {
        "amount": grossPremium,
        "currency": "JPY"
    },
}

response = client.Code.create_qr_code(request)
print(response['data']['url'])
