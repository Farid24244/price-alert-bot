import json
import os

import requests

TOKEN = os.environ["BOT_TOKEN"].strip()
CHAT_ID = os.environ["CHAT_ID"].strip()
import re

if not re.fullmatch(r"\d{5,12}:[A-Za-z0-9_-]{30,}", TOKEN):
    print("BOT_TOKEN has the wrong shape. length:", len(TOKEN), "colons:", TOKEN.count(":"))
    raise SystemExit(1)

PAIR = (os.environ.get("PAIR") or "BTC-USD").strip().upper()
HIGH = float(os.environ.get("HIGH") or 69500)
LOW = float(os.environ.get("LOW") or 66500)

STATE_FILE = "state.json"


def load_zone():
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f).get("zone", "mid")
    except (FileNotFoundError, ValueError):
        return "mid"


def save_zone(zone):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"zone": zone}, f)


r = requests.get(f"https://api.coinbase.com/v2/prices/{PAIR}/spot", timeout=20)
r.raise_for_status()
price = float(r.json()["data"]["amount"])
print("pair:", PAIR, "price:", price)

if price >= HIGH:
    zone = "high"
elif price <= LOW:
    zone = "low"
else:
    zone = "mid"

previous = load_zone()
coin = PAIR.split("-")[0]

text = None
if zone != previous:
    if zone == "high":
        text = f"🚀 {coin} بالای {HIGH:g} دلار رفت: {price:g} دلار"
    elif zone == "low":
        text = f"🔻 {coin} زیر {LOW:g} دلار اومد: {price:g} دلار"

if text:
    resp = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
        timeout=20,
    )
    resp.raise_for_status()
    print("alert sent")

save_zone(zone)
