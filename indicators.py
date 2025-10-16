"""
Technical Indicators Module
============================
This module computes various technical indicators for gold price analysis.
Includes RSI, Moving Averages, MACD, Bollinger Bands, and more.

Functions:
    - calculate_rsi: Relative Strength Index
    - calculate_moving_averages: SMA and EMA
    - calculate_macd: Moving Average Convergence Divergence
    - calculate_bollinger_bands: Bollinger Bands
    - add_all_indicators: Compute all indicators at once
"""

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volatility import BollingerBands


def calculate_rsi(data, period=14):
    """
    Calculate Relative Strength Index (RSI).
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with 'Close' column
    period : int
        RSI period (default: 14)
    
    Returns:
    --------
    pd.Series
        RSI values
    """
    try:
        rsi_indicator = RSIIndicator(close=data['Close'], window=period)
        return rsi_indicator.rsi()
    except Exception as e:
        print(f"Error calculating RSI: {str(e)}")
        return pd.Series([np.nan] * len(data))


def calculate_moving_averages(data):
    """
    Calculate Simple Moving Averages (SMA) for 20, 50, and 200 periods.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with 'Close' column
    
    Returns:
    --------
    dict
        Dictionary containing MA_20, MA_50, MA_200 as pandas Series
    """
    try:
        ma_dict = {}
        
        # SMA 20
        sma_20 = SMAIndicator(close=data['Close'], window=20)
        ma_dict['MA_20'] = sma_20.sma_indicator()
        
        # SMA 50
        sma_50 = SMAIndicator(close=data['Close'], window=50)
        ma_dict['MA_50'] = sma_50.sma_indicator()
        
        # SMA 200
        if len(data) >= 200:
            sma_200 = SMAIndicator(close=data['Close'], window=200)
            ma_dict['MA_200'] = sma_200.sma_indicator()
        else:
            ma_dict['MA_200'] = pd.Series([np.nan] * len(data))
        
        return ma_dict
        
    except Exception as e:
        print(f"Error calculating Moving Averages: {str(e)}")
        return {
            'MA_20': pd.Series([np.nan] * len(data)),
            'MA_50': pd.Series([np.nan] * len(data)),
            'MA_200': pd.Series([np.nan] * len(data))
        }


def calculate_ema(data, period=12):
    """
    Calculate Exponential Moving Average (EMA).
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with 'Close' column
    period : int
        EMA period
    
    Returns:
    --------
    pd.Series
        EMA values
    """
    try:
        ema_indicator = EMAIndicator(close=data['Close'], window=period)
        return ema_indicator.ema_indicator()
    except Exception as e:
        print(f"Error calculating EMA: {str(e)}")
        return pd.Series([np.nan] * len(data))


def calculate_macd(data):
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with 'Close' column
    
    Returns:
    --------
    dict
        Dictionary containing MACD line, Signal line, and Histogram
    """
    try:
        macd_indicator = MACD(
            close=data['Close'],
            window_slow=26,
            window_fast=12,
            window_sign=9
        )
        
        return {
            'MACD': macd_indicator.macd(),
            'MACD_Signal': macd_indicator.macd_signal(),
            'MACD_Histogram': macd_indicator.macd_diff()
        }
        
    except Exception as e:
        print(f"Error calculating MACD: {str(e)}")
        return {
            'MACD': pd.Series([np.nan] * len(data)),
            'MACD_Signal': pd.Series([np.nan] * len(data)),
            'MACD_Histogram': pd.Series([np.nan] * len(data))
        }


def calculate_bollinger_bands(data, period=20, std_dev=2):
    """
    Calculate Bollinger Bands.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with 'Close' column
    period : int
        Period for moving average (default: 20)
    std_dev : int
        Number of standard deviations (default: 2)
    
    Returns:
    --------
    dict
        Dictionary containing Upper Band, Middle Band, Lower Band
    """
    try:
        bb_indicator = BollingerBands(
            close=data['Close'],
            window=period,
            window_dev=std_dev
        )
        
        return {
            'BB_Upper': bb_indicator.bollinger_hband(),
            'BB_Middle': bb_indicator.bollinger_mavg(),
            'BB_Lower': bb_indicator.bollinger_lband()
        }
        
    except Exception as e:
        print(f"Error calculating Bollinger Bands: {str(e)}")
        return {
            'BB_Upper': pd.Series([np.nan] * len(data)),
            'BB_Middle': pd.Series([np.nan] * len(data)),
            'BB_Lower': pd.Series([np.nan] * len(data))
        }


def add_all_indicators(data):
    """
    Add all technical indicators to the DataFrame.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with OHLCV data
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with all indicators added as new columns
    """
    try:
        # Make a copy to avoid modifying original data
        df = data.copy()
        
        # Calculate RSI
        df['RSI'] = calculate_rsi(df)
        
        # Calculate Moving Averages
        ma_dict = calculate_moving_averages(df)
        df['MA_20'] = ma_dict['MA_20']
        df['MA_50'] = ma_dict['MA_50']
        df['MA_200'] = ma_dict['MA_200']
        
        # Calculate MACD
        macd_dict = calculate_macd(df)
        df['MACD'] = macd_dict['MACD']
        df['MACD_Signal'] = macd_dict['MACD_Signal']
        df['MACD_Histogram'] = macd_dict['MACD_Histogram']
        
        # Calculate Bollinger Bands
        bb_dict = calculate_bollinger_bands(df)
        df['BB_Upper'] = bb_dict['BB_Upper']
        df['BB_Middle'] = bb_dict['BB_Middle']
        df['BB_Lower'] = bb_dict['BB_Lower']
        
        return df
        
    except Exception as e:
        print(f"Error adding all indicators: {str(e)}")
        return data


def get_signal_interpretation(data):
    """
    Interpret technical indicators and generate trading signals.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with technical indicators
    
    Returns:
    --------
    dict
        Dictionary containing signal interpretations
    """
    try:
        latest = data.iloc[-1]
        signals = {}
        
        # RSI Signal
        if pd.notna(latest['RSI']):
            if latest['RSI'] > 70:
                signals['RSI'] = {'signal': 'OVERBOUGHT', 'value': latest['RSI'], 'color': 'red'}
            elif latest['RSI'] < 30:
                signals['RSI'] = {'signal': 'OVERSOLD', 'value': latest['RSI'], 'color': 'green'}
            else:
                signals['RSI'] = {'signal': 'NEUTRAL', 'value': latest['RSI'], 'color': 'yellow'}
        
        # Moving Average Signal
        if pd.notna(latest['MA_20']) and pd.notna(latest['MA_50']):
            if latest['MA_20'] > latest['MA_50']:
                signals['MA'] = {'signal': 'BULLISH', 'description': 'MA20 > MA50', 'color': 'green'}
            else:
                signals['MA'] = {'signal': 'BEARISH', 'description': 'MA20 < MA50', 'color': 'red'}
        
        # MACD Signal
        if pd.notna(latest['MACD']) and pd.notna(latest['MACD_Signal']):
            if latest['MACD'] > latest['MACD_Signal']:
                signals['MACD'] = {'signal': 'BULLISH', 'description': 'MACD > Signal', 'color': 'green'}
            else:
                signals['MACD'] = {'signal': 'BEARISH', 'description': 'MACD < Signal', 'color': 'red'}
        
        # Bollinger Bands Signal
        if pd.notna(latest['BB_Upper']) and pd.notna(latest['BB_Lower']):
            price = latest['Close']
            if price > latest['BB_Upper']:
                signals['BB'] = {'signal': 'OVERBOUGHT', 'description': 'Price > Upper Band', 'color': 'red'}
            elif price < latest['BB_Lower']:
                signals['BB'] = {'signal': 'OVERSOLD', 'description': 'Price < Lower Band', 'color': 'green'}
            else:
                signals['BB'] = {'signal': 'NEUTRAL', 'description': 'Price within bands', 'color': 'yellow'}
        
        return signals
        
    except Exception as e:
        print(f"Error interpreting signals: {str(e)}")
        return {}


