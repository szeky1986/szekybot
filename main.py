import os
import time
import json
import hmac
import hashlib
import websocket
import threading

# Környezeti változók betöltése Railway-hez
API_KEY = os.getenv("BITGET_API_KEY")
SECRET_KEY = os.getenv("BITGET_SECRET_KEY")
PASSPHRASE = os.getenv("BITGET_PASSPHRASE")

SYMBOL = "BTC-USDT"  # Helyes formátum

def on_message(ws, message):
    data = json.loads(message)
    print("Tick adat:", data)

def on_open(ws):
    print("Websocket kapcsolódva.")
    sub_params = {
        "op": "subscribe",
        "args": [f"spot/ticker:{SYMBOL}"]
    }
    ws.send(json.dumps(sub_params))

def on_error(ws, error):
    print("Hiba:", error)

def on_close(ws, close_status_code, close_msg):
    print("Websocket zárva.")

def start_ws():
    ws_url = "wss://ws.bitget.com/spot/v1/stream"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    print("Bitget bot indul...")
    threading.Thread(target=start_ws).start()