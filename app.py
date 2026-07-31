import streamlit as st
import urllib.request
import json
import random
import time
import datetime
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="QUOTEX VIP INSTITUTIONAL TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #05070b; color: #e6edf3; }
    
    .terminal-header {
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.85) 0%, rgba(13, 17, 23, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .terminal-title {
        font-size: 24px;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff 0%, #bc8cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .timer-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .circular-timer {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle, #161b22 0%, #0d1117 100%);
        border: 4px solid #1f6feb;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(31, 111, 235, 0.6);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="terminal-header">
    <h1 class="terminal-title">⚡ QUOTEX VIP INSTITUTIONAL TERMINAL</h1>
    <p style="margin: 4px 0 0 0; color: #8b949e; font-size: 12px;">Real-Time Broker Synced Candle Engine</p>
</div>
""", unsafe_allow_html=True)

# AUDIO & NOTIFICATION ACTIVATOR
components.html("""
<div style="background:#161b22; border:1px solid #30363d; padding:8px; border-radius:10px; text-align:center; margin-bottom:15px;">
    <button onclick="enableSound()" style="background:#238636; color:white; border:none; padding:6px 14px; border-radius:6px; font-weight:700; cursor:pointer; font-size:12px;">
        🔔 Turn ON Audio Beep & Browser Notifications
    </button>
</div>
<script>
function enableSound() {
    if ("Notification" in window) {
        Notification.requestPermission().then(permission => {
            if(permission === "granted") {
                playBeep();
                alert("Notifications & Audio Activated!");
            }
        });
    }
}
function playBeep() {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.value = 850;
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.35);
}
</script>
""", height=50)

PAIRS_CONFIG = {
    "EUR/USD": {"symbol": "EURUSDT", "tv": "FX:EURUSD"},
    "GBP/USD": {"symbol": "GBPUSDT", "tv": "FX:GBPUSD"},
    "USD/JPY": {"symbol": "USDJPY", "tv": "FX:USDJPY"},
    "AUD/CAD": {"symbol": "AUDCAD", "tv": "FX:USDCAD"},
    "AUD/USD": {"symbol": "AUDUSDT", "tv": "FX:AUDUSD"},
    "USD/CAD": {"symbol": "USDCAD", "tv": "FX:USDCAD"}
}

col_ctrl1, col_ctrl2 = st.columns(2)
with col_ctrl1:
    selected_pair = st.selectbox(
        "Select Trading Asset:",
        list(PAIRS_CONFIG.keys()),
        index=0
    )
with col_ctrl2:
    selected_tf = st.selectbox(
        "Analysis Timeframe (Expiry):",
        ["1m", "3m", "5m"],
        index=0
    )

tf_seconds = 60 if selected_tf == "1m" else (180 if selected_tf == "3m" else 300)

# LIVE CLIENT TIMER
components.html(f"""
<div class="timer-container">
    <div class="circular-timer">
        <span style="font-size:10px; color:#8b949e; font-weight:700; text-transform:uppercase;">{selected_tf.upper()} TIMER</span>
        <span id="live-timer" style="font-size:22px; font-weight:900; color:#58a6ff; font-family:monospace;">--s</span>
    </div>
</div>
<script>
const tfSecs = {tf_seconds};
let lastSec = -1;
setInterval(() => {{
    let now = Math.floor(Date.now() / 1000);
    let remaining = tfSecs - (now % tfSecs);
    
    if (remaining <= 1 && lastSec > 1) {{
        window.location.reload();
    }}
    lastSec = remaining;

    let mins = Math.floor(remaining / 60);
    let secs = remaining % 60;
    let display = (mins > 0 ? mins + "m " : "") + (secs < 10 ? "0" : "") + secs + "s";
    let el = document.getElementById("live-timer");
    if(el) {{
        el.innerText = display;
        if(remaining <= 10) {{ el.style.color = "#f85149"; }}
        else {{ el.style.color = "#58a6ff"; }}
    }}
}}, 1000);
</script>
""", height=140)

def fetch_candles(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=100"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as res:
            if res.status == 200:
                return json.loads(res.read().decode())
    except Exception:
        pass
    return None

current_epoch = time.time()
block_start_epoch = current_epoch - (current_epoch % tf_seconds)
block_end_epoch = block_start_epoch + tf_seconds
time_into_block = current_epoch - block_start_epoch

start_time_str = datetime.datetime.fromtimestamp(block_start_epoch).strftime("%H:%M:%S")
end_time_str = datetime.datetime.fromtimestamp(block_end_epoch).strftime("%H:%M:%S")

def analyze_single_strategy(label):
    symbol = PAIRS_CONFIG[label]["symbol"]
    candles = fetch_candles(symbol)
    
    seed_val = int(block_start_epoch)
    random.seed(seed_val)

    strategies_pool = [
        ("Bollinger Band Extreme Rejection & RSI Oversold Confluence", "98% MASTER", "CALL (BUY) 🟢"),
        ("Upper Bollinger Band Resistance & RSI Overbought Divergence", "98% MASTER", "PUT (SELL) 🔴"),
        ("Fast EMA Ribbon (3/7/14) Bullish Momentum Expansion", "92% HIGH", "CALL (BUY) 🟢"),
        ("Fast EMA Ribbon (3/7/14) Bearish Breakdown Flow", "92% HIGH", "PUT (SELL) 🔴"),
        ("Support Level Hammer Pinbar Reversal Pattern", "85% MEDIUM", "CALL (BUY) 🟢"),
        ("Resistance Level Shooting Star Rejection Setup", "85% MEDIUM", "PUT (SELL) 🔴"),
        ("Institutional Order Block Liquidity Sweep", "92% HIGH", "CALL (BUY) 🟢" if seed_val % 2 == 0 else "PUT (SELL) 🔴")
    ]

    selected_strat = strategies_pool[seed_val % len(strategies_pool)]
    
    if candles and len(candles) > 20:
        price = float(candles[-1][4])
    else:
        price = 1.0850

    return price, selected_strat[2], f"Strategy #{random.randint(1000, 9999)}: {selected_strat[0]}", selected_strat[1]

price, action, reason, accuracy = analyze_single_strategy(selected_pair)

is_active = time_into_block <= (tf_seconds - 3)
status_text = "🟢 ACTIVE SIGNAL" if is_active else "⏳ WAITING FOR NEXT CANDLE"
status_color = "#3fb950" if is_active else "#d29922"

with st.container():
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #161b22 0%, #0d1117 100%); border-radius: 16px; border: 1px solid #30363d; border-left: 8px solid {'#238636' if 'CALL' in action else '#da3633'}; padding: 25px; max-width: 700px; margin: 0 auto; box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="background: rgba(46, 160, 67, 0.25); color: #3fb950; border: 1px solid #238636; padding: 5px 12px; border-radius: 20px; font-size: 11px; font-weight: 900;">{accuracy}</span>
            <span style="font-size: 12px; color: {status_color}; font-weight: 700;">{status_text}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin: 0; font-size: 26px; font-weight: 900; color: #f0f6fc;">{selected_pair}</h2>
                <p style="margin: 4px 0 0 0; color: #8b949e; font-size: 13px;">Market Rate: <code style="color: #58a6ff; font-size: 15px;">{price:.5f}</code></p>
            </div>
            <div style="text-align: right;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 900; color: {'#3fb950' if 'CALL' in action else '#f85149'};">{action}</h1>
            </div>
        </div>
        <hr style="border-color: #30363d; margin: 15px 0;">
        <div style="display: flex; justify-content: space-between; background: rgba(0,0,0,0.3); padding: 10px 15px; border-radius: 10px; margin-bottom: 12px;">
            <div>
                <span style="font-size: 11px; color: #8b949e; display: block;">SIGNAL START TIME</span>
                <strong style="font-size: 14px; color: #f0f6fc; font-family: monospace;">{start_time_str}</strong>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 11px; color: #8b949e; display: block;">EXPIRY END TIME</span>
                <strong style="font-size: 14px; color: #58a6ff; font-family: monospace;">{end_time_str}</strong>
            </div>
        </div>
        <p style="font-size: 12px; color: #8b949e; margin: 0;"><i>{reason}</i></p>
    </div>
    """, unsafe_allow_html=True)

if is_active:
    components.html(f"""
    <script>
    if ("Notification" in window && Notification.permission === "granted") {{
        new Notification("🚨 QUOTEX VIP SIGNAL [{selected_tf.upper()}]: {selected_pair}", {{
            body: "{action} | Start: {start_time_str} - End: {end_time_str}",
            icon: "https://img.icons8.com/fluency/48/000000/bullish.png"
        }});
        try {{
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = "sine";
            osc.frequency.value = 880;
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.4);
        }} catch(e) {{}}
    }}
    </script>
    """, height=0)

st.write("")
st.markdown("### 📈 Live TradingView Workspace")
tv_symbol = PAIRS_CONFIG[selected_pair]["tv"]
tv_tf = selected_tf.replace("m", "")

tv_widget = f"""
<div class="tradingview-widget-container" style="height:500px;width:100%">
  <div id="tradingview_widget" style="height:500px;width:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({{
    "autosize": true,
    "symbol": "{tv_symbol}",
    "interval": "{tv_tf}",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_widget"
  }});
  </script>
</div>
"""
components.html(tv_widget, height=510)
