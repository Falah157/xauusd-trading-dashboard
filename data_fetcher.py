"""
Data Fetcher Module - WITH GOLDAPI.IO
=====================================
Uses GoldAPI.io for real gold prices, with yfinance and demo fallbacks.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import numpy as np


@st.cache_data(ttl=60)
def fetch_gold_data(period="1mo", interval="1h"):
    """
    Fetch gold data using GoldAPI.io first, then yfinance as fallback.
    """
    try:
        # Try GoldAPI.io first - this is the best source for real gold prices
        try:
            from gold_api import get_goldapi_data
            data = get_goldapi_data("goldapi-4xdl6smgqq7f3m-io")
            if data is not None and not data.empty:
                return data
        except Exception as e:
            st.warning(f"GoldAPI.io not available: {str(e)}")
        
        # Try gold futures from Yahoo Finance as fallback
        tickers_to_try = ["GC=F", "XAUUSD=X"]
        
        for ticker in tickers_to_try:
            try:
                st.info(f"🔄 Trying Yahoo Finance {ticker}...")
                
                # Use yfinance exactly like their examples
                data = yf.download(ticker, period=period, progress=False)
                
                if data is not None and not data.empty:
                    st.success(f"✅ Got real data from {ticker}")
                    
                    # Reset index to make datetime a column
                    data = data.reset_index()
                    
                    # Rename Date column to Datetime if needed
                    if 'Date' in data.columns:
                        data = data.rename(columns={'Date': 'Datetime'})
                    
                    # Ensure we have all required columns
                    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                    for col in required_cols:
                        if col not in data.columns:
                            if col == 'Volume':
                                data[col] = 100000  # Default volume
                            else:
                                data[col] = data.get('Close', 2650)
                    
                    return data
                    
            except Exception as e:
                st.warning(f"❌ {ticker} failed: {str(e)}")
                continue
        
        # If all fails, create realistic demo data
        st.warning("⚠️ Using realistic demo data (~$2600-2700)")
        return create_realistic_demo_data()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return create_realistic_demo_data()


def create_realistic_demo_data():
    """Create realistic gold price data."""
    try:
        # Create date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        date_range = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # Generate realistic gold prices around $2600-2700
        base_price = 2650
        np.random.seed(42)
        
        prices = []
        for i, date in enumerate(date_range):
            change = np.random.normal(0, 0.01)
            if i == 0:
                price = base_price
            else:
                price = prices[-1] * (1 + change)
            prices.append(price)
        
        # Create OHLC data
        data = []
        for i, (date, close) in enumerate(zip(date_range, prices)):
            volatility = abs(np.random.normal(0, 0.005))
            high = close * (1 + volatility)
            low = close * (1 - volatility)
            open_price = prices[i-1] if i > 0 else close
            
            high = max(high, open_price, close)
            low = min(low, open_price, close)
            
            data.append({
                'Datetime': date,
                'Open': round(open_price, 2),
                'High': round(high, 2),
                'Low': round(low, 2),
                'Close': round(close, 2),
                'Volume': np.random.randint(50000, 200000)
            })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"Error creating demo data: {str(e)}")
        return None


def get_latest_price(data):
    """
    Get latest price in the format main.py expects.
    Returns a dictionary with all required keys.
    """
    try:
        if data is None or data.empty:
            return {
                'price': 2650.0,
                'change': 0.0,
                'change_pct': 0.0,
                'high': 2700.0,
                'low': 2600.0,
                'open': 2650.0,
                'volume': 100000
            }
        
        latest_price = float(data['Close'].iloc[-1])
        high_24h = float(data['High'].tail(24).max()) if len(data) >= 24 else float(data['High'].max())
        low_24h = float(data['Low'].tail(24).min()) if len(data) >= 24 else float(data['Low'].min())
        open_price = float(data['Open'].iloc[-1])
        volume = int(data['Volume'].iloc[-1])
        
        # Calculate change
        if len(data) > 1:
            prev_price = float(data['Close'].iloc[-2])
            change = latest_price - prev_price
            change_pct = (change / prev_price) * 100
        else:
            change = 0.0
            change_pct = 0.0
        
        return {
            'price': latest_price,
            'change': change,
            'change_pct': change_pct,
            'high': high_24h,
            'low': low_24h,
            'open': open_price,
            'volume': volume
        }
        
    except Exception as e:
        st.error(f"Error getting latest price: {str(e)}")
        return {
            'price': 2650.0,
            'change': 0.0,
            'change_pct': 0.0,
            'high': 2700.0,
            'low': 2600.0,
            'open': 2650.0,
            'volume': 100000
        }


def generate_price_summary(data):
    """Generate price summary for the dashboard."""
    try:
        if data is None or data.empty:
            return None
        
        latest_price = data['Close'].iloc[-1]
        high_24h = data['High'].tail(24).max() if len(data) >= 24 else data['High'].max()
        low_24h = data['Low'].tail(24).min() if len(data) >= 24 else data['Low'].min()
        open_price = data['Open'].iloc[-1]
        volume = data['Volume'].iloc[-1]
        
        if len(data) > 1:
            prev_close = data['Close'].iloc[-2]
            price_change = latest_price - prev_close
            price_change_pct = (price_change / prev_close) * 100
        else:
            price_change = 0
            price_change_pct = 0
        
        return {
            'current_price': latest_price,
            'high_24h': high_24h,
            'low_24h': low_24h,
            'open_price': open_price,
            'volume': volume,
            'price_change': price_change,
            'price_change_pct': price_change_pct
        }
        
    except Exception as e:
        st.error(f"Error generating price summary: {str(e)}")
        return None