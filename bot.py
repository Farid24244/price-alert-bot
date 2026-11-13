import os
import requests

token = os.environ["BOT_TOKEN"]
chat_id = os.environ["CHAT_ID"]

r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=20)
price = r.json()["data"]["amount"]

text = f"قیمت بیت‌کوین الان: {price} دلار"
requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data={"chat_id": chat_id, "text": text},
    timeout=20,
)
