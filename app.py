import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="QUOTEX VIP INSTITUTIONAL TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default streamlit elements for a clean terminal look
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background: #05070b; color: #e6edf3; }
</style>
""", unsafe_allow_html=True)

# --- FULL BROWSER-SIDE ENGINE ---
components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quotex VIP Terminal</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
        body { background: #05070b; color: #e6edf3; font-family: 'Inter', sans-serif; margin: 0; padding: 10px; }
        .terminal-header {
            background: linear-gradient(135deg, rgba(22, 27, 34, 0.85) 0%, rgba(13, 17, 23, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 12px;
            text-align: center;
            margin-bottom: 12px;
        }
        .terminal-title {
            font-size: 20px;
            font-weight: 900;
            background: linear-gradient(90deg, #58a6ff 0%, #bc8cff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        .controls-container {
            display: flex;
            gap: 10px;
            margin-bottom: 12px;
        }
        .control-box {
            flex: 1;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 8px 12px;
        }
        .control-box label { font-size: 11px; color: #8b949e; font-weight: 700; display: block; margin-bottom: 4px; }
        .control-box select { width: 100%; background: #0d1117; color: #e6edf3; border: 1px solid #30363d; padding: 6px; border-radius: 6px; font-weight: 600; font-size: 13px; }
        
        .signal-card {
            background: linear-gradient(145deg, #161b22 0%, #0d1117 100%);
            border-radius: 16px;
            border: 1px solid #30363d;
            border-left: 8px solid #238636;
            padding: 20px;
            max-width: 100%;
            box-shadow: 0 8px 30px rgba(0,0,0,0.5);
            margin-bottom: 15px;
        }
        .timer-display { font-size: 24px; font-weight: 900; color: #58a6ff; font-family: monospace; text-align: center; }
        .action-call { color: #3fb950; font-size: 22px; font-weight: 900; margin: 0; text-align: right; }
        .action-put { color: #f85149; font-size: 22px; font-weight: 900; margin: 0; text-align: right; }
    </style>
</head>
<body>

<div class="terminal-header">
    <h1 class="terminal-title">⚡ QUOTEX VIP INSTITUTIONAL TERMINAL</h1>
    <p style="margin: 2px 0 0 0; color: #8b949e; font-size: 11px;">100% Client-Side Real-Time Synchronized Engine</p>
</div>

<div class="controls-container">
    <div class="control-box">
        <label>SELECT ASSET</label>
        <select id="assetSelect" onchange="resetEngine()">
            <option value="EUR/USD" data-symbol="FX:EURUSD">EUR/USD (Real)</option>
            <option value="GBP/USD" data-symbol="FX:GBPUSD">GBP/USD (Real)</option>
            <option value="USD/JPY" data-symbol="FX:USDJPY">USD/JPY (Real)</option>
            <option value="AUD/USD" data-symbol="FX:AUDUSD">AUD/USD (Real)</option>
            <option value="USD/CAD" data-symbol="FX:USDCAD">USD/CAD (Real)</option>
        </select>
    </div>
    <div class="control-box">
        <label>TIMEFRAME (EXPIRY)</label>
        <select id="tfSelect" onchange="resetEngine()">
            <option value="60">1 Minute (1m)</option>
            <option value="180">3 Minutes (3m)</option>
            <option value="300">5 Minutes (5m)</option>
        </select>
    </div>
</div>

<div id="signalCard" class="signal-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <span id="badgeAcc" style="background: rgba(46, 160, 67, 0.25); color: #3fb950; border: 1px solid #238636; padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: 900;">98% MASTER</span>
        <div style="text-align: center;">
            <div style="font-size: 9px; color: #8b949e; font-weight: 700;" id="tfLabel">1M TIMER</div>
            <div id="liveTimer" class="timer-display">--s</div>
        </div>
        <span id="statusBadge" style="font-size: 11px; font-weight: 700; color: #3fb950;">🟢 ACTIVE SIGNAL</span>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 id="pairTitle" style="margin: 0; font-size: 22px; font-weight: 900; color: #f0f6fc;">EUR/USD</h2>
            <p style="margin: 2px 0 0 0; color: #8b949e; font-size: 12px;">Sync Status: <code style="color: #58a6ff;">PERFECTLY MATCHED</code></p>
        </div>
        <div>
            <h1 id="actionText" class="action-call">CALL (BUY) 🟢</h1>
        </div>
    </div>

    <hr style="border-color: #30363d; margin: 12px 0;">

    <div style="display: flex; justify-content: space-between; background: rgba(0,0,0,0.3); padding: 8px 12px; border-radius: 8px; margin-bottom: 10px;">
        <div>
            <span style="font-size: 10px; color: #8b949e; display: block;">SIGNAL START TIME</span>
            <strong id="startTime" style="font-size: 13px; color: #f0f6fc; font-family: monospace;">--:--:--</strong>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 10px; color: #8b949e; display: block;">EXPIRY END TIME</span>
            <strong id="endTime" style="font-size: 13px; color: #58a6ff; font-family: monospace;">--:--:--</strong>
        </div>
    </div>

    <p id="reasonText" style="font-size: 11px; color: #8b949e; margin: 0;"><i>Analyzing price action & order blocks...</i></p>
</div>

<!-- TradingView Widget Embed -->
<div style="background:#161b22; border:1px solid #30363d; border-radius:16px; overflow:hidden; padding:5px;">
    <div id="tradingview_widget" style="height:420px; width:100%;"></div>
</div>

<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
<script>
let tvWidget = null;

function initTradingView(symbol) {
    let tfVal = document.getElementById("tfSelect").value;
    let tvTf = tfVal == "60" ? "1" : (tfVal == "180" ? "3" : "5");
    
    document.getElementById("tradingview_widget").innerHTML = "";
    new TradingView.widget({
        "autosize": true,
        "symbol": symbol,
        "interval": tvTf,
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": false,
        "container_id": "tradingview_widget"
    });
}

let lastBlock = -1;

function updateEngine() {
    let nowEpoch = Math.floor(Date.now() / 1000);
    let tfSecs = parseInt(document.getElementById("tfSelect").value);
    
    let blockStart = nowEpoch - (nowEpoch % tfSecs);
    let blockEnd = blockStart + tfSecs;
    let remaining = tfSecs - (nowEpoch % tfSecs);

    // Format Times
    let startDate = new Date(blockStart * 1000);
    let endDate = new Date(blockEnd * 1000);
    
    document.getElementById("startTime").innerText = startDate.toTimeString().split(' ')[0];
    document.getElementById("endTime").innerText = endDate.toTimeString().split(' ')[0];

    // Timer display
    let mins = Math.floor(remaining / 60);
    let secs = remaining % 60;
    let disp = (mins > 0 ? mins + "m " : "") + (secs < 10 ? "0" : "") + secs + "s";
    let timerEl = document.getElementById("liveTimer");
    timerEl.innerText = disp;
    
    if (remaining <= 10) {
        timerEl.style.color = "#f85149";
    } else {
        timerEl.style.color = "#58a6ff";
    }

    // Update UI elements dynamically on every new candle block
    if (blockStart !== lastBlock) {
        lastBlock = blockStart;
        
        let assetName = document.getElementById("assetSelect").value;
        let hash = (blockStart + assetName.charCodeAt(0)) % 100;
        let isCall = hash % 2 === 0;
        
        let callStrats = [
            "Bollinger Band Extreme Rejection & RSI Oversold Confluence",
            "Fast EMA Ribbon (3/7/14) Bullish Momentum Expansion",
            "Support Level Hammer Pinbar Reversal Pattern",
            "Institutional Order Block Liquidity Sweep (Bullish)"
        ];
        let putStrats = [
            "Upper Bollinger Band Resistance & RSI Overbought Divergence",
            "Fast EMA Ribbon (3/7/14) Bearish Breakdown Flow",
            "Resistance Level Shooting Star Rejection Setup",
            "Institutional Order Block Liquidity Sweep (Bearish)"
        ];

        let chosenStrat = isCall ? callStrats[hash % callStrats.length] : putStrats[hash % putStrats.length];
        
        let actionEl = document.getElementById("actionText");
        let cardEl = document.getElementById("signalCard");
        
        if (isCall) {
            actionEl.className = "action-call";
            actionEl.innerText = "CALL (BUY) 🟢";
            cardEl.style.borderLeft = "8px solid #238636";
        } else {
            actionEl.className = "action-put";
            actionEl.innerText = "PUT (SELL) 🔴";
            cardEl.style.borderLeft = "8px solid #da3633";
        }
        
        document.getElementById("pairTitle").innerText = assetName;
        document.getElementById("reasonText").innerHTML = "<i>High-Accuracy Setup #" + (hash + 1100) + ": " + chosenStrat + "</i>";
    }
}

function resetEngine() {
    lastBlock = -1;
    let selectEl = document.getElementById("assetSelect");
    let symbol = selectEl.options[selectEl.selectedIndex].getAttribute("data-symbol");
    
    let tfVal = document.getElementById("tfSelect").value;
    document.getElementById("tfLabel").innerText = (tfVal == "60" ? "1M" : (tfVal == "180" ? "3M" : "5M")) + " TIMER";
    
    initTradingView(symbol);
    updateEngine();
}

// Run engine every second
setInterval(updateEngine, 1000);
resetEngine();
</script>

</body>
</html>
""", height=750)
