import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

print("Bitget Top20 Futures Email Bot - Loop verzió indul...")

API_URL = "https://api.bitget.com"
SYMBOLS = ["ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "AVAXUSDT",
           "DOTUSDT", "SHIBUSDT", "LINKUSDT", "MATICUSDT", "UNIUSDT", "LTCUSDT", "BCHUSDT",
           "NEARUSDT", "APTUSDT", "ATOMUSDT", "XLMUSDT", "IMXUSDT", "INJUSDT"]
TIMEFRAMES = ["30m", "1h"]

EMAIL_SENDER = "szekyke11@gmail.com"
EMAIL_PASSWORD = "brava123456789"
EMAIL_RECEIVER = "szek_l@hotmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email elküldve: {subject}")
    except Exception as e:
        print("Hiba történt email küldés közben:", e)

def get_kline(symbol, interval):
    url = f"{API_URL}/api/mix/v1/market/candles?symbol={symbol}&granularity={interval}&productType=umcbl"
    response = requests.get(url)
    return response.json()["data"]

def calculate_rsi(closes, period=14):
    gains, losses = [], []
    for i in range(1, period + 1):
        delta = float(closes[i - 1]) - float(closes[i])
        if delta > 0:
            gains.append(delta)
        else:
            losses.append(abs(delta))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_ema(closes, period=50):
    closes = list(map(float, closes[:period]))
    k = 2 / (period + 1)
    ema = closes[0]
    for price in closes[1:]:
        ema = price * k + ema * (1 - k)
    return ema

def check_entry(symbol, tf):
    candles = get_kline(symbol, tf)
    if not candles or len(candles) < 60:
        return

    closes = [c[4] for c in candles]
    last_close = float(closes[0])
    rsi = calculate_rsi(closes[:15])
    ema = calculate_ema(closes[:50])

    direction = None
    if rsi < 30 and last_close > ema:
        direction = "LONG"
    elif rsi > 70 and last_close < ema:
        direction = "SHORT"

    if direction:
        sl = round(last_close * (0.985 if direction == "LONG" else 1.015), 4)
        tp = round(last_close * (1.03 if direction == "LONG" else 0.97), 4)
        subject = f"Bitget Jelzés - {direction} {symbol}"
        body = f"""
Idő: {datetime.utcnow().isoformat()} UTC
Pár: {symbol}
Irány: {direction}
Timeframe: {tf}
Belépő: {last_close}
SL: {sl}
TP: {tp}
RSI: {round(rsi,2)}
EMA: {round(ema,2)}
        """.strip()
        send_email(subject, body)

def run_bot():
    print(f"Futtatás: {datetime.utcnow().isoformat()} UTC")
    for tf in TIMEFRAMES:
        print(f"--- {tf} vizsgálat ---")
        for sym in SYMBOLS:
            try:
                check_entry(sym, tf)
                time.sleep(0.5)
            except Exception as e:
                print(f"Hiba {sym}/{tf}: {e}")

if __name__ == "__main__":
    while True:
        run_bot()
        print("Várakozás 30 percig...
")
        time.sleep(1800)
