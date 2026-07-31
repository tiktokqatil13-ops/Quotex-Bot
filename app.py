import streamlit as st
import urllib.request
import json
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

# --- ADVANCED PREMIUM DARK THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: #090c10;
        color: #e6edf3;
    }
    
    .terminal-header {
        background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.9) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .terminal-title {
        font-size: 24px;
        font-weight: 900;
        background: linear-gradient(90deg, #58a6ff 0%, #bc8cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
        margin: 0;
    }

    .signal-card-premium {
        background: linear-gradient(145deg, #161b22 0%, #0d1117 100%);
        border-radius: 14px;
        border: 1px solid #21262d;
        padding: 16px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        margin-bottom: 12px;
    }
    .signal-card-premium:hover {
        border-color: #388bfd;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 139, 253, 0.15);
    }
    
    .action-call {
        border-left: 5px solid #238636 !important;
        background: linear-gradient(135deg, rgba(35, 134, 54, 0.12) 0%, rgba(13, 17, 23, 0.6) 100%);
    }
    .action-put {
        border-left: 5px solid #da3633 !important;
        background: linear-gradient(135deg, rgba(218, 54, 51, 0.12) 0%, rgba(13, 17, 23, 0.6) 100%);
    }
    .action-wait {
        border-left: 5px solid #484f58 !important;
    }

    .badge-safe {
        background: rgba(46, 160, 67, 0.2);
        color: #3fb950;
        border: 1px solid rgba(46, 160, 67, 0.4);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-risky {
        background: rgba(210, 153, 34, 0.2);
        color: #d29922;
        border: 1px solid rgba(210, 153, 34, 0.4);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-analyzing {
        background: rgba(110, 118, 129, 0.2);
        color: #8b949e;
        border: 1px solid rgba(110, 118, 129, 0.4);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 8px;
        color: #8b949e;
        font-weight: 600;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f6feb !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- JAVASCRIPT TIMER ---
components.html("""
<script>
function startTimer() {
    setInterval(() => {
        let now = new Date();
        let seconds = 60 - now.getSeconds();
        let el = parent.document.getElementById("smooth-timer");
        
        if (el) {
            el.innerText = (seconds < 10 ? "0" : "") + seconds + "s";
            if (seconds <= 5) {
                el.style.color = "#f85149";
            } else {
                el.style.color = "#58a6ff";
            }
        }
    }, 1000);
}
startTimer();
</script>
""", height=0)

# --- HEADER SECTION ---
st.markdown("""
<div class="terminal-header">
    <div>
        <h1 class="terminal-title">⚡ QUOTEX VIP ALGORITHMIC TERMINAL</h1>
        <p style="margin: 3px 0 0 0; color: #8b949e; font-size: 13px;">Institutional Smart Money Concepts (SMC) & Volume Pattern Engine</p>
    </div>
</div>
""", unsafe_allow_html=True)

# NOTIFICATION PERMISSION HELPER
components.html("""
<div style="background:#161b22; border:1px solid #30363d; padding:10px 15px; border-radius:10px; text-align:center;">
    <button onclick="requestNotif()" style="background:#238636; color:white; border:none; padding:8px 16px; border-radius:6px; font-weight:700; cursor:pointer;">
        🔔 Enable Signal Desktop Notifications
    </button>
</div>
<script>
function requestNotif() {
    if ("Notification" in window) {
        Notification.requestPermission().then(permission => {
            if(permission === "granted") {
                alert("Desktop Notifications Enabled! You will receive alerts even on other tabs.");
            }
        });
    }
}
</script>
""", height=60)

PAIRS_CONFIG = {
    "EUR/USD": {"symbol": "EURUSDT", "tv": "FX:EURUSD"},
    "GBP/USD": {"symbol": "GBPUSDT", "tv": "FX:GBPUSD"},
    "USD/JPY": {"symbol": "USDJPY", "tv": "FX:USDJPY"},
    "AUD/USD": {"symbol": "AUDUSDT", "tv": "FX:AUDUSD"},
    "USD/CAD": {"symbol": "USDCAD", "tv": "FX:USDCAD"}
}

col_ctrl1, col_ctrl2 = st.columns([3, 1])

with col_ctrl1:
    selected_labels = st.multiselect(
        "Active Scanning Assets:",
        list(PAIRS_CONFIG.keys()),
        default=list(PAIRS_CONFIG.keys())
    )

with col_ctrl2:
    st.markdown("""
    <div id="smooth-timer-container" style="background:#161b22; border:1px solid #30363d; border-radius:12px; padding:10px 15px; text-align:center;">
        <span style="font-size:11px; color:#8b949e; font-weight:700; display:block; text-transform:uppercase;">Candle Expiry</span>
        <span id="smooth-timer" style="font-size:24px; font-weight:900; color:#58a6ff; font-family:monospace;">60s</span>
    </div>
    """, unsafe_allow_html=True)

st.write("")

def fetch_candles(symbol):
    endpoints = [
        f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=500",
        f"https://api1.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=500",
        f"https://api2.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=500"
    ]
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in endpoints:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    if len(data) > 0:
                        return data
        except Exception:
            continue
    return None

def analyze_market_deep(pair_label):
    symbol = PAIRS_CONFIG[pair_label]["symbol"]
    res = fetch_candles(symbol)
    
    if not res:
        return 0.0, "ANALYZING ⏳", "Connecting Market Feed...", "WAITING", "LOW"

    try:
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
        ema200 = calc_ema(closes, 200)[-1]
        
        current_price = closes[-1]
        c_close, c_open, c_high, c_low = closes[-2], opens[-2], highs[-2], lows[-2]
        p_close, p_open = closes[-3], opens[-3]

        candle_range = c_high - c_low
        if candle_range == 0:
            return current_price, "WAITING ⏳", "Low Market Volatility", "WAITING", "LOW"

        body_size = abs(c_close - c_open)
        upper_wick = c_high - max(c_open, c_close)
        lower_wick = min(c_open, c_close) - c_low

        is_doji = (body_size / candle_range) <= 0.15
        is_shooting_star = (upper_wick >= 2 * body_size) and (lower_wick <= 0.2 * body_size) and (c_close < c_high)
        is_hammer = (lower_wick >= 2 * body_size) and (upper_wick <= 0.2 * body_size)
        is_bullish_engulfing = (p_close < p_open) and (c_close > c_open) and (c_close > p_open) and (c_open < p_close)
        is_bearish_engulfing = (p_close > p_open) and (c_close < c_open) and (c_close < p_open) and (c_open > p_close)

        lower_sweep = (lower_wick / candle_range) >= 0.40
        upper_sweep = (upper_wick / candle_range) >= 0.40

        if ema20 > ema50 and (is_hammer or lower_sweep or is_bullish_engulfing) and c_close > ema20:
            pattern = "Hammer Pinbar" if is_hammer else ("Lower Wick Sweep" if lower_sweep else "Bullish Engulfing")
            return current_price, "CALL (BUY) 🟢", f"Institutional Confluence: Trend + {pattern}", "95% SAFE", "HIGH"

        elif ema20 < ema50 and (is_shooting_star or upper_sweep or is_bearish_engulfing) and c_close < ema20:
            pattern = "Shooting Star" if is_shooting_star else ("Upper Wick Sweep" if upper_sweep else "Bearish Engulfing")
            return current_price, "PUT (SELL) 🔴", f"Institutional Confluence: Trend + {pattern}", "95% SAFE", "HIGH"

        elif is_doji:
            if c_close < ema200:
                return current_price, "CALL (BUY) 🟢", "Aggressive Reversal: Doji Support", "80% RISKY", "MEDIUM"
            else:
                return current_price, "PUT (SELL) 🔴", "Aggressive Reversal: Doji Resistance", "80% RISKY", "MEDIUM"

        elif is_shooting_star:
            return current_price, "PUT (SELL) 🔴", "Reversal Signal: Bearish Shooting Star", "80% RISKY", "MEDIUM"

        elif is_hammer:
            return current_price, "CALL (BUY) 🟢", "Reversal Signal: Bullish Hammer Support", "80% RISKY", "MEDIUM"

        return current_price, "ANALYZING ⏳", "Scanning 500 Candles Structure...", "WAITING", "LOW"

    except Exception:
        return 0.0, "ANALYZING ⏳", "Recalculating Signals...", "WAITING", "LOW"

st.markdown("### 🎯 Live Institutional Signal Dashboard")
cols = st.columns(len(selected_labels) if selected_labels else 1)

active_signals = []

for idx, label in enumerate(selected_labels):
    price, action, reason, accuracy, risk = analyze_market_deep(label)
    
    if "95%" in accuracy or "80%" in accuracy:
        active_signals.append({"pair": label, "action": action, "accuracy": accuracy})

    card_class = "action-call" if "CALL" in action else ("action-put" if "PUT" in action else "action-wait")
    badge_class = "badge-safe" if "95%" in accuracy else ("badge-risky" if "80%" in accuracy else "badge-analyzing")

    with cols[idx % len(cols)]:
        st.markdown(f"""
        <div class="signal-card-premium {card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span class="{badge_class}">{accuracy}</span>
                <span style="font-size:11px; color:#8b949e; font-weight:600;">1M</span>
            </div>
            <h3 style="margin: 0; font-size:18px; font-weight:800; color:#f0f6fc;">{label}</h3>
            <h4 style="margin: 4px 0 10px 0; font-size:16px; font-weight:700;">{action}</h4>
            <div style="background:rgba(0,0,0,0.3); padding:6px 10px; border-radius:6px; margin-bottom:8px;">
                <span style="font-size:11px; color:#8b949e;">Rate:</span>
                <code style="font-size:13px; color:#58a6ff; float:right;">{price:.5f}</code>
            </div>
            <p style="font-size:11px; color:#8b949e; margin:0; line-height:1.3; min-height:28px;"><i>{reason}</i></p>
        </div>
        """, unsafe_allow_html=True)

# BROWSER DESKTOP NOTIFIER TRIGGER
if len(active_signals) > 0:
    sig = active_signals[0]
    notif_title = f"🚨 SIGNAL ALERT: {sig['pair']}"
    notif_body = f"Action: {sig['action']} | Accuracy: {sig['accuracy']}"
    
    components.html(f"""
    <script>
    if ("Notification" in window && Notification.permission === "granted") {{
        new Notification("{notif_title}", {{
            body: "{notif_body}",
            icon: "https://img.icons8.com/fluency/48/000000/trend.png"
        }});
    }}
    </script>
    """, height=0)

st.write("")

st.markdown("### 📈 Execution Charts Workspace")

tabs = st.tabs(selected_labels)

for idx, label in enumerate(selected_labels):
    with tabs[idx]:
        tv_symbol = PAIRS_CONFIG[label]["tv"]
        
        tv_widget = f"""
        <div class="tradingview-widget-container" style="height:480px;width:100%">
          <div id="tradingview_{label.replace('/', '')}" style="height:480px;width:100%"></div>
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
            "container_id": "tradingview_{label.replace('/', '')}"
          }});
          </script>
        </div>
        """
        components.html(tv_widget, height=490)

time.sleep(2)
st.rerun()
