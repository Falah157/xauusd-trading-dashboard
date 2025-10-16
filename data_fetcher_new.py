"""
Data Fetcher Module
===================
This module handles fetching real-time gold (XAUUSD) price data from Yahoo Finance.
Uses proper yfinance approach based on their documentation.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import numpy as np
import os

# Load environment variables (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass  # Continue without .env file if there are permission issues


@st.cache_data(ttl=60)  # Cache for 60 seconds (1 minute refresh)
def fetch_gold_data(period="1mo", interval="1h"):
    """
    Fetch historical gold price data using proper yfinance approach.
    
    Parameters:
    -----------
    period : str
        Time period to fetch data for (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, max)
    interval : str
        Data interval (1m, 2m, 5m, 15m, 30m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing OHLCV data with columns: Open, High, Low, Close, Volume
    """
    try:
        # Try gold futures first (most accurate for real gold price)
        gold_tickers = ["GC=F", "XAUUSD=X"]  # Gold futures/spot
        
        for ticker in gold_tickers:
            try:
                st.info(f"🔄 Trying to fetch data from {ticker}...")
                
                # Use yfinance download function like in their examples
                data = yf.download(
                    ticker,
                    period=period,
                    interval=interval,
                    progress=False,
                    auto_adjust=True,
                    threads=False,  # Disable threading to avoid issues
                    timeout=15,
                    repair=True,  # Repair missing data
                    keepna=False
                )
                
                if data is not None and not data.empty and len(data) > 0:
                    st.success(f"✅ Successfully loaded real gold data from {ticker}")
                    
                    # Reset index to make datetime a column
                    data = data.reset_index()
                    
                    # Ensure required columns exist
                    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    for col in required_columns:
                        if col not in data.columns:
                            if col == 'Volume':
                                data[col] = 100000  # Default volume for futures
                            else:
                                data[col] = data.get('Close', 2650)  # Default gold price
                    
                    # Rename Datetime column if needed
                    if 'Datetime' not in data.columns and 'Date' in data.columns:
                        data = data.rename(columns={'Date': 'Datetime'})
                    
                    return data
                else:
                    st.warning(f"❌ No data returned for {ticker}")
                    
            except Exception as e:
                st.warning(f"❌ Failed to fetch {ticker}: {str(e)}")
                continue
        
        # If futures fail, try Alpha Vantage
        st.warning("Gold futures unavailable. Trying Alpha Vantage...")
        alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if alpha_key and alpha_key != "demo":
            try:
                from free_data_sources import get_alpha_vantage_data
                data = get_alpha_vantage_data("XAU", alpha_key)
                if data is not None and not data.empty:
                    st.success("✅ Successfully loaded real gold data from Alpha Vantage")
                    return data
            except Exception as e:
                st.warning(f"Alpha Vantage failed: {str(e)}")
        
        # Fallback to realistic demo data
        st.warning("⚠️ Using realistic demo data (real gold prices ~$2600-2700)")
        st.info("💡 For live data, ensure stable internet connection or get Alpha Vantage API key")
        return create_realistic_gold_data()
        
    except Exception as e:
        st.error(f"❌ Critical error in data fetching: {str(e)}")
        st.warning("Using demo data due to critical error")
        return create_realistic_gold_data()


def create_realistic_gold_data():
    """
    Create realistic gold price data around current market levels (~$2600-2700).
    
    Returns:
    --------
    pd.DataFrame
        Realistic gold price DataFrame with OHLCV data
    """
    try:
        # Create date range for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        date_range = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # Generate realistic gold price data around $2600-2700 (current levels)
        base_price = 2650  # Realistic gold price
        np.random.seed(42)  # For consistent data
        
        # Create price series with some trend and volatility
        price_changes = np.random.normal(0, 0.015, len(date_range))  # 1.5% volatility
        prices = [base_price]
        
        # Add some realistic trend
        trend = 0.0001  # Slight upward trend
        
        for i, change in enumerate(price_changes[1:], 1):
            # Add trend component
            trend_component = trend * i
            new_price = prices[-1] * (1 + change + trend_component)
            prices.append(new_price)
        
        # Create OHLC data
        data = []
        for i, (date, close) in enumerate(zip(date_range, prices)):
            # Add some intraday volatility
            volatility = abs(np.random.normal(0, 0.008))
            high = close * (1 + volatility)
            low = close * (1 - volatility)
            open_price = prices[i-1] if i > 0 else close
            
            # Ensure OHLC logic is maintained
            high = max(high, open_price, close)
            low = min(low, open_price, close)
            
            # Realistic volume for gold (much higher than ETFs)
            volume = np.random.randint(50000, 500000)
            
            data.append({
                'Datetime': date,
                'Open': round(open_price, 2),
                'High': round(high, 2),
                'Low': round(low, 2),
                'Close': round(close, 2),
                'Volume': volume
            })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"Error creating realistic gold data: {str(e)}")
        return None


def create_demo_data():
    """
    Create demo gold price data for demonstration purposes.
    (Legacy function - now uses realistic gold data)
    
    Returns:
    --------
    pd.DataFrame
        Demo DataFrame with OHLCV data
    """
    return create_realistic_gold_data()


def get_latest_price(data):
    """
    Get the latest gold price from the data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing gold price data
    
    Returns:
    --------
    float
        Latest gold price
    """
    try:
        if data is not None and not data.empty:
            latest_price = data['Close'].iloc[-1]
            return float(latest_price)
        else:
            return 2650.0  # Default realistic gold price
    except Exception as e:
        st.error(f"Error getting latest price: {str(e)}")
        return 2650.0


def generate_price_summary(data):
    """
    Generate a summary of price statistics.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing gold price data
    
    Returns:
    --------
    dict
        Dictionary containing price statistics
    """
    try:
        if data is None or data.empty:
            return None
        
        latest_price = data['Close'].iloc[-1]
        high_24h = data['High'].tail(24).max() if len(data) >= 24 else data['High'].max()
        low_24h = data['Low'].tail(24).min() if len(data) >= 24 else data['Low'].min()
        open_price = data['Open'].iloc[-1]
        volume = data['Volume'].iloc[-1]
        
        # Calculate change
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
