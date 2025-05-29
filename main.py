import time
import hmac
import hashlib
import requests

# Bitget API info (beégetve a kódba)
API_KEY = "bg_9909f94555b2a1f6bb15c0d2f68d2c07"
API_SECRET = "93dcd38fa3024ae574a74a528b9f749766f8255a1f03e433f55bb04c3063bf28"
API_PASSPHRASE = "Mollyka8631"

BASE_URL = "https://api.bitget.com"

def get_timestamp():
    return str(int(time.time() * 1000))

def generate_signature(timestamp, method, request_path, body):
    message = f"{timestamp}{method}{request_path}{body}"
    return hmac.new(
        bytes(API_SECRET, "utf-8"),
        msg=bytes(message, "utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()

def get_account_info():
    timestamp = get_timestamp()
    method = "GET"
    request_path = "/api/spot/v1/account/assets"
    body = ""

    signature = generate_signature(timestamp, method, request_path, body)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}{request_path}"
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    print("Bitget teszt bot indul...")
    try:
        result = get_account_info()
        print("Kapcsolat sikeres! Fiók információ:")
        print(result)
    except Exception as e:
        print("Hiba történt a kapcsolat során:", e)
