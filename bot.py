import os
import requests

token = os.environ["BOT_TOKEN"]
chat_id = os.environ["CHAT_ID"]

HIGH = 69500
LOW = 68000

r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=20)
price = float(r.json()["data"]["amount"])
print("price:", price)

text = None
if price >= HIGH:
    text = f"🚀 بیت‌کوین بالای {HIGH} رفت: {price} دلار"
elif price <= LOW:
    text = f"🔻 بیت‌کوین زیر {LOW} اومد: {price} دلار"

if text:
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": text},
        timeout=20,
    )
