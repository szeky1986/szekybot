import os
import time
import hmac
import hashlib
import requests

# Bitget API info (beállítandó Railway-en env-ként)
API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")

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
    request_path = "/api/v2/account/assets"
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
