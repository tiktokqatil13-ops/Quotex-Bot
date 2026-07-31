import streamlit as st
import urllib.request
import json
import time

st.set_page_config(page_title="Quotex SMC Signals", layout="wide")

st.title("📊 Quotex Real-Time SMC Signal Scanner")
st.caption("Live Binance Data | Smart Money Concepts (EMA + Wick Sweeps)")

pairs = st.multiselect(
    "Select Pairs to Scan:",
    ["EURUSDT", "GBPUSDT", "USDJPY", "AUDUSDT", "USDCAD"],
    default=["EURUSDT", "GBPUSDT", "USDJPY", "AUDUSDT", "USDCAD"]
)

def get_signal(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=50"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            res = json.loads(response.read().decode())
            
        closes = [float(k[4]) for k in res]
        highs = [float(k[2]) for k in res]
        lows = [float(k[3]) for k in res]
        opens = [float(k[1]) for k in res]

        def calc_ema(data, period):
            k = 2 / (period + 1)
            ema = [data[0]]
            for val in data[1:]:
                ema.append((val * k) + (ema[-1] * (1 - k)))
            return ema

        ema20 = calc_ema(closes, 20)[-1]
        ema50 = calc_ema(closes, 50)[-1]
        
        last_close = closes[-2]
        last_open = opens[-2]
        last_high = highs[-2]
        last_low = lows[-2]

        candle_range = last_high - last_low
        if candle_range == 0:
            return None, None

        lower_wick = min(last_open, last_close) - last_low
        upper_wick = last_high - max(last_open, last_close)

        if ema20 > ema50 and (lower_wick / candle_range >= 0.5):
            return "CALL (BUY)", f"Lower Wick Sweep ({symbol[:-4]})"
        elif ema20 < ema50 and (upper_wick / candle_range >= 0.5):
            return "PUT (SELL)", f"Upper Wick Sweep ({symbol[:-4]})"

        return None, None
    except Exception:
        return None, None

cols = st.columns(len(pairs) if pairs else 1)

for idx, pair in enumerate(pairs):
    action, reason = get_signal(pair)
    with cols[idx % len(cols)]:
        pair_clean = pair.replace("USDT", "")
        if action:
            if "CALL" in action:
                st.success(f"### 🟢 {pair_clean}\n**{action}**\n\n_{reason}_")
            else:
                st.error(f"### 🔴 {pair_clean}\n**{action}**\n\n_{reason}_")
        else:
            st.info(f"### ⚪ {pair_clean}\nScanning...")

time.sleep(3)
st.rerun()
