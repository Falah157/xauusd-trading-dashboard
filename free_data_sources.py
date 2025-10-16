"""
Free Data Sources Module
========================
Alternative free data sources for gold prices when Yahoo Finance fails.
"""

import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import json


def get_alpha_vantage_data(symbol="XAU", api_key="demo"):
    """
    Fetch data from Alpha Vantage (free tier available).
    Sign up at: https://www.alphavantage.co/support/#api-key
    
    Parameters:
    -----------
    symbol : str
        Stock symbol (GLD for gold ETF)
    api_key : str
        Alpha Vantage API key (use 'demo' for demo data)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with OHLCV data
    """
    try:
        if api_key == "demo":
            # Use demo data if no API key
            st.info("💡 To get real-time data, get a free API key from Alpha Vantage")
            return None
        
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'FX_DAILY',
            'from_symbol': 'XAU',
            'to_symbol': 'USD',
            'apikey': api_key,
            'outputsize': 'compact'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'Time Series (FX)' in data:
            time_series = data['Time Series (FX)']
            
            # Convert to DataFrame
            df_data = []
            for date_str, values in time_series.items():
                df_data.append({
                    'Datetime': pd.to_datetime(date_str),
                    'Open': float(values['1. open']),
                    'High': float(values['2. high']),
                    'Low': float(values['3. low']),
                    'Close': float(values['4. close']),
                    'Volume': 1000000  # Default volume for FX data
                })
            
            df = pd.DataFrame(df_data)
            df = df.sort_values('Datetime')
            return df
        else:
            st.error(f"Alpha Vantage API error: {data.get('Error Message', 'Unknown error')}")
            return None
            
    except Exception as e:
        st.error(f"Error fetching Alpha Vantage data: {str(e)}")
        return None


def get_finnhub_data(symbol="GLD", api_key="demo"):
    """
    Fetch data from Finnhub (free tier available).
    Sign up at: https://finnhub.io/
    
    Parameters:
    -----------
    symbol : str
        Stock symbol (GLD for gold ETF)
    api_key : str
        Finnhub API key
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with OHLCV data
    """
    try:
        if api_key == "demo":
            st.info("💡 To get real-time data, get a free API key from Finnhub")
            return None
        
        # Get current timestamp and 30 days ago
        end_timestamp = int(datetime.now().timestamp())
        start_timestamp = int((datetime.now() - timedelta(days=30)).timestamp())
        
        url = f"https://finnhub.io/api/v1/stock/candle"
        params = {
            'symbol': symbol,
            'resolution': 'D',  # Daily
            'from': start_timestamp,
            'to': end_timestamp,
            'token': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('s') == 'ok':
            # Convert to DataFrame
            timestamps = data['t']
            opens = data['o']
            highs = data['h']
            lows = data['l']
            closes = data['c']
            volumes = data['v']
            
            df_data = []
            for i, timestamp in enumerate(timestamps):
                df_data.append({
                    'Datetime': pd.to_datetime(timestamp, unit='s'),
                    'Open': opens[i],
                    'High': highs[i],
                    'Low': lows[i],
                    'Close': closes[i],
                    'Volume': volumes[i]
                })
            
            df = pd.DataFrame(df_data)
            return df
        else:
            st.error(f"Finnhub API error: {data.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        st.error(f"Error fetching Finnhub data: {str(e)}")
        return None


def get_polygon_data(symbol="GLD", api_key="demo"):
    """
    Fetch data from Polygon.io (free tier available).
    Sign up at: https://polygon.io/
    
    Parameters:
    -----------
    symbol : str
        Stock symbol (GLD for gold ETF)
    api_key : str
        Polygon.io API key
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with OHLCV data
    """
    try:
        if api_key == "demo":
            st.info("💡 To get real-time data, get a free API key from Polygon.io")
            return None
        
        # Get data for last 30 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
        params = {'adjusted': 'true', 'sort': 'asc', 'apikey': api_key}
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == 'OK' and data.get('results'):
            results = data['results']
            
            df_data = []
            for result in results:
                df_data.append({
                    'Datetime': pd.to_datetime(result['t'], unit='ms'),
                    'Open': result['o'],
                    'High': result['h'],
                    'Low': result['l'],
                    'Close': result['c'],
                    'Volume': result['v']
                })
            
            df = pd.DataFrame(df_data)
            return df
        else:
            st.error(f"Polygon.io API error: {data.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        st.error(f"Error fetching Polygon.io data: {str(e)}")
        return None


def get_free_data_sources_info():
    """
    Display information about free data sources.
    """
    st.markdown("""
    ### 📊 Free Data Sources for Real-Time Gold Prices
    
    **Option 1: Yahoo Finance (Currently Used)**
    - ✅ Completely free
    - ✅ No API key required
    - ✅ Gold ETFs: GLD, IAU, SGOL, OUNZ, AAAU
    - ❌ Sometimes unreliable
    
    **Option 2: Alpha Vantage**
    - ✅ Free tier: 5 API calls per minute, 500 calls per day
    - ✅ Very reliable
    - 🔗 Get API key: https://www.alphavantage.co/support/#api-key
    - 💡 Add API key to environment variables
    
    **Option 3: Finnhub**
    - ✅ Free tier: 60 API calls per minute
    - ✅ Good for real-time data
    - 🔗 Get API key: https://finnhub.io/
    
    **Option 4: Polygon.io**
    - ✅ Free tier: 5 API calls per minute
    - ✅ Professional-grade data
    - 🔗 Get API key: https://polygon.io/
    
    **How to Add API Keys:**
    1. Get a free API key from any service above
    2. Create a `.env` file in your project directory
    3. Add: `ALPHA_VANTAGE_API_KEY=your_key_here`
    4. Restart the dashboard
    """)
