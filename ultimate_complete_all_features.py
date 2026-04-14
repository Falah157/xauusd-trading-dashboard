import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="XAUUSD BTCUSD TRADING", layout="wide", page_icon="🏆")

st.markdown('<h1 style="text-align: center;">🏆 XAUUSD & BTCUSD AI Trading Dashboard</h1>', unsafe_allow_html=True)

# ============ CONFIGURATION ============
API_KEY = "96871e27b094425f9ea104fa6eb2be64"

# Symbols
SYMBOLS = {
    "XAUUSD": {"api": "XAU/USD", "name": "Gold", "digits": 2, "color": "#ffd700"},
    "BTCUSD": {"api": "BTC/USD", "name": "Bitcoin", "digits": 0, "color": "#ff8c00"}
}

TIMEFRAMES = {
    "1m": {"api": "1min", "minutes": 1},
    "5m": {"api": "5min", "minutes": 5},
    "15m": {"api": "15min", "minutes": 15},
    "30m": {"api": "30min", "minutes": 30},
    "1h": {"api": "1h", "minutes": 60},
    "4h": {"api": "4h", "minutes": 240},
    "1d": {"api": "1day", "minutes": 1440}
}

# Session state
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = "XAUUSD"
if 'selected_tf' not in st.session_state:
    st.session_state.selected_tf = "1h"
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []

# ============ DATA FUNCTIONS ============
@st.cache_data(ttl=30)
def get_price(symbol):
    try:
        api_symbol = SYMBOLS[symbol]["api"]
        url = f"https://api.twelvedata.com/price?symbol={api_symbol}&apikey={API_KEY}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return float(r.json()['price'])
    except:
        pass
    return None

@st.cache_data(ttl=60)
def get_data(symbol, tf, days=30):
    try:
        api_symbol = SYMBOLS[symbol]["api"]
        api_tf = TIMEFRAMES[tf]["api"]
        minutes = TIMEFRAMES[tf]["minutes"]
        total = min(int((days * 1440) / minutes), 300)
        url = f"https://api.twelvedata.com/time_series?symbol={api_symbol}&interval={api_tf}&outputsize={total}&apikey={API_KEY}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if 'values' in data:
                df = pd.DataFrame(data['values'])
                df['datetime'] = pd.to_datetime(df['datetime'])
                df = df.set_index('datetime')
                df['close'] = df['close'].astype(float)
                df['high'] = df['high'].astype(float)
                df['low'] = df['low'].astype(float)
                df['open'] = df['open'].astype(float)
                return df
    except:
        pass
    return None

def calculate_indicators(df):
    df = df.copy()
    df['sma20'] = df['close'].rolling(20).mean()
    df['sma50'] = df['close'].rolling(50).mean()
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    df['ema12'] = df['close'].ewm(span=12).mean()
    df['ema26'] = df['close'].ewm(span=26).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    
    df['hl'] = df['high'] - df['low']
    df['atr'] = df['hl'].rolling(14).mean()
    
    return df

def get_signal(df):
    if df is None or len(df) < 30:
        return "WAIT", 0
    
    last = df.iloc[-1]
    
    buy_score = 0
    sell_score = 0
    
    if last['close'] > last['sma20']:
        buy_score += 30
    else:
        sell_score += 30
    
    if last['sma20'] > last['sma50']:
        buy_score += 20
    else:
        sell_score += 20
    
    if last['rsi'] < 35:
        buy_score += 25
    elif last['rsi'] > 65:
        sell_score += 25
    
    if last['macd'] > last['macd_signal']:
        buy_score += 25
    else:
        sell_score += 25
    
    confidence = max(buy_score, sell_score)
    
    if buy_score > sell_score and confidence >= 55:
        return "BUY", confidence
    elif sell_score > buy_score and confidence >= 55:
        return "SELL", confidence
    else:
        return "WAIT", confidence

def calculate_levels(price, atr, signal):
    if signal == "BUY":
        entry = price
        sl = entry - (atr * 1.0)
        tp1 = entry + (atr * 1.5)
        tp2 = entry + (atr * 2.0)
        tp3 = entry + (atr * 3.0)
        tp4 = entry + (atr * 4.0)
    else:
        entry = price
        sl = entry + (atr * 1.0)
        tp1 = entry - (atr * 1.5)
        tp2 = entry - (atr * 2.0)
        tp3 = entry - (atr * 3.0)
        tp4 = entry - (atr * 4.0)
    
    risk = abs(entry - sl)
    return entry, sl, tp1, tp2, tp3, tp4, risk

def run_backtest(df, symbol, tf, risk_percent):
    if df is None or len(df) < 100:
        return None
    
    df = calculate_indicators(df)
    trades = []
    balance = 10000
    balance_history = [balance]
    
    for i in range(50, len(df) - 4):
        current_data = df.iloc[:i+1]
        signal, confidence = get_signal(current_data)
        
        if signal != "WAIT" and confidence >= 55:
            current_price = df.iloc[i]['close']
            atr = df.iloc[i]['atr'] if not pd.isna(df.iloc[i]['atr']) else current_price * 0.005
            
            entry, sl, tp1, tp2, tp3, tp4, risk = calculate_levels(current_price, atr, signal)
            
            risk_amount = balance * (risk_percent / 100)
            pos_size = risk_amount / risk if risk > 0 else 0
            
            future_prices = df['close'].iloc[i+1:i+5].values
            hit_sl = any(future_prices <= sl if signal == "BUY" else future_prices >= sl)
            hit_tp = any(future_prices >= tp2 if signal == "BUY" else future_prices <= tp2)
            
            if hit_tp and not hit_sl:
                profit = pos_size * abs(tp2 - current_price)
                balance += profit
                trades.append({'result': 'WIN', 'pnl': profit})
            elif hit_sl:
                balance -= risk_amount
                trades.append({'result': 'LOSS', 'pnl': -risk_amount})
            
            balance_history.append(balance)
    
    if trades:
        wins = len([t for t in trades if t['result'] == 'WIN'])
        win_rate = wins / len(trades) * 100
        total_pnl = sum([t['pnl'] for t in trades])
        gross_profit = sum([t['pnl'] for t in trades if t['result'] == 'WIN'])
        gross_loss = abs(sum([t['pnl'] for t in trades if t['result'] == 'LOSS']))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        return {
            'trades': len(trades),
            'wins': wins,
            'losses': len(trades) - wins,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'profit_factor': profit_factor,
            'balance_history': balance_history
        }
    return None

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("## ⚙️ SETTINGS")
    
    symbol = st.selectbox("Select Symbol", ["XAUUSD", "BTCUSD"], index=0)
    if symbol != st.session_state.selected_symbol:
        st.session_state.selected_symbol = symbol
        st.cache_data.clear()
        st.rerun()
    
    tf = st.selectbox("Timeframe", ["1m", "5m", "15m", "30m", "1h", "4h", "1d"], index=4)
    if tf != st.session_state.selected_tf:
        st.session_state.selected_tf = tf
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    account_balance = st.number_input("Balance ($)", value=10000, step=1000)
    risk_percent = st.slider("Risk %", 0.5, 2.0, 1.0)
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 BACKTEST")
    bt_period = st.selectbox("Period", ["30d", "60d", "90d"], index=1)
    if st.button("🚀 Run Backtest", use_container_width=True):
        days = {"30d": 30, "60d": 60, "90d": 90}[bt_period]
        with st.spinner(f"Backtesting {tf}..."):
            bt_df = get_data(symbol, tf, days)
            result = run_backtest(bt_df, symbol, tf, risk_percent)
            if result:
                st.session_state.backtest_results = result
                st.success(f"Win Rate: {result['win_rate']:.1f}% | P&L: ${result['total_pnl']:.2f}")
            else:
                st.warning("No trades generated")

# ============ MAIN CONTENT ============
# Load data
with st.spinner(f"Loading {st.session_state.selected_symbol} {st.session_state.selected_tf} data..."):
    df = get_data(st.session_state.selected_symbol, st.session_state.selected_tf, 30)
    current_price = get_price(st.session_state.selected_symbol)

# Display metrics (with safe None handling)
col1, col2, col3, col4 = st.columns(4)

with col1:
    if current_price:
        st.metric(f"{st.session_state.selected_symbol}", f"${current_price:,.{SYMBOLS[st.session_state.selected_symbol]['digits']}f}")
    else:
        st.metric(f"{st.session_state.selected_symbol}", "Loading...")

# Calculate signal if data available
if df is not None and len(df) > 30:
    df = calculate_indicators(df)
    current_price = current_price if current_price else float(df['close'].iloc[-1])
    atr = float(df['atr'].iloc[-1]) if not pd.isna(df['atr'].iloc[-1]) else current_price * 0.005
    
    signal, confidence = get_signal(df)
    
    with col2:
        st.metric("ATR", f"${atr:.{SYMBOLS[st.session_state.selected_symbol]['digits']}f}")
    with col3:
        st.metric("RSI", f"{df['rsi'].iloc[-1]:.1f}")
    with col4:
        st.metric("Signal", signal)
    
    # Display Signal
    if signal == "BUY":
        st.success(f"📈 BUY SIGNAL - Confidence: {confidence:.0f}%")
        entry, sl, tp1, tp2, tp3, tp4, risk = calculate_levels(current_price, atr, "BUY")
    elif signal == "SELL":
        st.error(f"📉 SELL SIGNAL - Confidence: {confidence:.0f}%")
        entry, sl, tp1, tp2, tp3, tp4, risk = calculate_levels(current_price, atr, "SELL")
    else:
        st.warning(f"⏸️ WAIT - Confidence: {confidence:.0f}%")
        entry, sl, tp1, tp2, tp3, tp4, risk = current_price, current_price, current_price, current_price, current_price, current_price, 0
    
    # Trading Levels
    if signal != "WAIT":
        st.markdown("---")
        st.subheader("🎯 TRADING LEVELS")
        
        level_cols = st.columns(6)
        level_cols[0].metric("📍 ENTRY", f"${entry:.{SYMBOLS[st.session_state.selected_symbol]['digits']}f}")
        level_cols[1].metric("🛑 SL", f"${sl:.{SYMBOLS[st.session_state.selected_symbol]['digits']}f}", f"Risk: ${risk:.2f}")
        level_cols[2].metric("🎯 TP1", f"${tp1:.{SYMBOLS[st.session_state.selected_symbol]['digits']}f}")
        level_cols[3].metric("🎯 TP2", f"${tp2:.{SYMBOLS[st.session_state.selected_symbol]['digits']}f}")
        level_cols[4].metric("🎯 TP3", f"${tp3:.{SYMBOLS[st.session_state.selected_symbol]['digits']}f}")
        level_cols[5].metric("🎯 TP4", f"${tp4:.{SYMBOLS[st.session_state.selected_symbol]['digits']}f}")
        
        position_size = (account_balance * (risk_percent / 100)) / risk if risk > 0 else 0
        st.info(f"📊 Position Size: {position_size:.4f} lots | Risk Amount: ${account_balance * (risk_percent / 100):.2f}")
        
        if st.button("✅ RECORD TRADE", type="primary"):
            st.session_state.trade_history.append({
                'time': datetime.now(),
                'symbol': st.session_state.selected_symbol,
                'signal': signal,
                'entry': entry,
                'tp2': tp2,
                'confidence': confidence
            })
            st.success(f"Trade recorded at ${entry:.2f}")
            st.balloons()
    
    # Chart
    st.markdown("---")
    st.subheader(f"📈 {st.session_state.selected_tf.upper()} CHART")
    
    fig = go.Figure()
    chart_df = df.tail(100)
    fig.add_trace(go.Candlestick(x=chart_df.index, open=chart_df['open'], high=chart_df['high'],
                                  low=chart_df['low'], close=chart_df['close'], name=st.session_state.selected_symbol))
    
    if signal != "WAIT":
        fig.add_hline(y=entry, line_color="#ffd700", line_width=2, annotation_text="ENTRY")
        fig.add_hline(y=sl, line_color="#ff4444", line_dash="dash", annotation_text="SL")
    
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Trade History
    if st.session_state.trade_history:
        st.markdown("---")
        st.subheader("📋 RECENT TRADES")
        for trade in st.session_state.trade_history[-5:]:
            st.info(f"🎯 {trade['time'].strftime('%Y-%m-%d %H:%M:%S')} | {trade['symbol']} | {trade['signal']} | Entry: ${trade['entry']:.2f} | Conf: {trade['confidence']:.0f}%")
    
    # Backtest Results
    if st.session_state.get('backtest_results'):
        st.markdown("---")
        st.subheader("📊 BACKTEST RESULTS")
        res = st.session_state.backtest_results
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Trades", res['trades'])
        c2.metric("Win Rate", f"{res['win_rate']:.1f}%")
        c3.metric("Profit Factor", f"{res['profit_factor']:.2f}")
        c4.metric("Total P&L", f"${res['total_pnl']:.2f}")
        
        if 'balance_history' in res and res['balance_history']:
            fig_eq = go.Figure()
            fig_eq.add_trace(go.Scatter(y=res['balance_history'], mode='lines', name='Balance', line=dict(color='#00ff88')))
            fig_eq.add_hline(y=10000, line_dash="dash", line_color="gray")
            fig_eq.update_layout(title="Equity Curve", template='plotly_dark', height=300)
            st.plotly_chart(fig_eq, use_container_width=True)
else:
    st.warning("Loading market data... Please wait or refresh the page.")

# Footer
st.markdown("---")
st.caption("⚠️ EDUCATIONAL ONLY - Not financial advice")
