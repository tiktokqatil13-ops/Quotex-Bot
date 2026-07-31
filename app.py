import streamlit as st
import urllib.request
import json
import time
import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Quotex SMC Signals & Live Timer", layout="wide")

st.title("📊 Quotex High-Accuracy SMC Scanner + Live Timer")
st.caption("Live Binance Data | 250 Candles Analysis | Real-Time Candle Countdown")

pairs = st.multiselect(
    "Select Pairs to Scan:",
    ["EURUSDT", "GBPUSDT", "USDJPY", "AUDUSDT", "USDCAD"],
    default=["EURUSDT", "GBPUSDT", "USDJPY", "AUDUSDT", "USDCAD"]
)

# --- 1-MINUTE CANDLE COUNTDOWN TIMER ---
now = datetime.datetime.utcnow()
seconds_left = 60 - now.second

col_timer1, col_timer2 = st.columns([1, 3])
with col_timer1:
    if seconds_left <= 5:
        st.warning(f"⏳ **NEXT CANDLE IN: {seconds_left}s**\n\n🚨 *Get Ready to Place Trade!*")
    else:
        st.metric(label="⏱️ Candle Close In", value=f"{seconds_left}s")

st.divider()

def get_signal_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=250"
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

        ema20_list = calc_ema(closes, 20)
        ema50_list = calc_ema(closes, 50)
        
        ema20 = ema20_list[-1]
        ema50 = ema50_list[-1]
        
        current_price = closes[-1]
        
        last_close = closes[-2]
        last_open = opens[-2]
        last_high = highs[-2]
        last_low = lows[-2]

        candle_range = last_high - last_low
        if candle_range == 0:
            return current_price, "WAITING ⏳", "Zero Volatility", ema20, ema50

        body_size = abs(last_close - last_open)
        lower_wick = min(last_open, last_close) - last_low
        upper_wick = last_high - max(last_open, last_close)

        is_doji = (body_size / candle_range) < 0.25
        is_strong_body = (body_size / candle_range) >= 0.40
        lower_sweep = (lower_wick / candle_range) >= 0.40
        upper_sweep = (upper_wick / candle_range) >= 0.40

        if is_doji:
            return current_price, "WAITING ⏳", "Skipped: Doji Candle", ema20, ema50

        if ema20 > ema50 and lower_sweep and is_strong_body and last_close > last_open:
            return current_price, "CALL (BUY) 🟢", "CONFIRMED: Lower Sweep + Bullish Trend", ema20, ema50
        elif ema20 < ema50 and upper_sweep and is_strong_body and last_close < last_open:
            return current_price, "PUT (SELL) 🔴", "CONFIRMED: Upper Sweep + Bearish Trend", ema20, ema50

        return current_price, "WAITING ⏳", "Searching for Setup...", ema20, ema50

    except Exception:
        return 0.0, "ERROR ⚠️", "Data Fetch Failed", 0.0, 0.0

st.subheader("🎯 Live Signal Status")
cols = st.columns(len(pairs) if pairs else 1)

for idx, pair in enumerate(pairs):
    price, action, reason, e20, e50 = get_signal_data(pair)
    pair_clean = pair.replace("USDT", "")
    
    with cols[idx % len(cols)]:
        if "CALL" in action:
            st.success(f"### 🟢 {pair_clean}\n**{action}**\n\nPrice: `{price:.5f}`\n\n_{reason}_")
        elif "PUT" in action:
            st.error(f"### 🔴 {pair_clean}\n**{action}**\n\nPrice: `{price:.5f}`\n\n_{reason}_")
        else:
            st.info(f"### ⚪ {pair_clean}\n**{action}**\n\nPrice: `{price:.5f}`\n\n_{reason}_")

st.divider()

st.subheader("📈 Live Candlestick Charts")

for pair in pairs:
    tv_symbol = f"BINANCE:{pair}"
    pair_clean = pair.replace("USDT", "")
    
    st.markdown(f"#### 🔹 {pair_clean} 1-Minute Live Chart")
    
    tv_widget = f"""
    <div class="tradingview-widget-container" style="height:400px;width:100%">
      <div id="tradingview_{pair}" style="height:400px;width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "{tv_symbol}",
        "interval": "1",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_{pair}"
      }});
      </script>
    </div>
    """
    components.html(tv_widget, height=410)

# Refresh every 1 second to update countdown smooth
time.sleep(1)
st.rerun()
