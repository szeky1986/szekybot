import time
import hmac
import hashlib
import base64
import requests
from datetime import datetime, timezone

print("Inicializálás...")

API_KEY = "bg_9909f94555b2a1f6bb15c0d2f68d2c07"
API_SECRET = "93dcd38fa3024ae574a74a528b9f749766f8255a1f03e433f55bb04c3063bf28"
API_PASSPHRASE = "Mollyka8631"

BASE_URL = "https://api.bitget.com"
REQUEST_PATH = "/api/spot/v1/account/assets"
METHOD = "GET"
BODY = ""

def get_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")

def generate_signature(timestamp, method, request_path, body):
    print("Aláírás készítése...")
    pre_sign = f"{timestamp}{method.upper()}{request_path}{body}"
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        pre_sign.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()

def get_account_info():
    timestamp = get_timestamp()
    print(f"Időbélyeg: {timestamp}")
    signature = generate_signature(timestamp, METHOD, REQUEST_PATH, BODY)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}{REQUEST_PATH}"
    print(f"URL: {url}")
    print("Kérés elküldése a Bitget API-hoz...")
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    print("Bitget teszt bot indul (Railway optimalizált)...")
    try:
        result = get_account_info()
        print("Kapcsolat sikeres! Fiók információ:")
        print(result)
    except Exception as e:
        print("Hiba történt a kapcsolat során:", e)
