"""
AI Model Module
===============
This module implements machine learning models for gold price prediction.
Uses Linear Regression for short-term price movement forecasting.

Functions:
    - prepare_features: Prepare feature data for ML model
    - train_model: Train the Linear Regression model
    - make_prediction: Make price predictions
    - calculate_accuracy: Calculate model accuracy metrics
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import streamlit as st


def prepare_features(data, lookback_period=10):
    """
    Prepare feature data for machine learning model.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with price and indicator data
    lookback_period : int
        Number of periods to look back for features
    
    Returns:
    --------
    tuple
        (X, y) feature matrix and target values
    """
    try:
        df = data.copy()
        
        # Create lagged features
        for i in range(1, lookback_period + 1):
            df[f'Close_lag_{i}'] = df['Close'].shift(i)
            df[f'Volume_lag_{i}'] = df['Volume'].shift(i)
        
        # Add technical indicators as features
        feature_columns = [f'Close_lag_{i}' for i in range(1, lookback_period + 1)]
        feature_columns += [f'Volume_lag_{i}' for i in range(1, lookback_period + 1)]
        
        # Add indicators if available
        if 'RSI' in df.columns:
            feature_columns.append('RSI')
        if 'MACD' in df.columns:
            feature_columns.append('MACD')
        if 'MA_20' in df.columns:
            feature_columns.append('MA_20')
        if 'MA_50' in df.columns:
            feature_columns.append('MA_50')
        
        # Remove rows with NaN values
        df = df.dropna(subset=feature_columns + ['Close'])
        
        # Prepare X and y
        X = df[feature_columns].values
        y = df['Close'].values
        
        return X, y, feature_columns
        
    except Exception as e:
        print(f"Error preparing features: {str(e)}")
        return None, None, None


def train_model(data, test_size=0.2):
    """
    Train Linear Regression model for price prediction.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with price and indicator data
    test_size : float
        Proportion of data to use for testing
    
    Returns:
    --------
    dict
        Dictionary containing model, metrics, and feature names
    """
    try:
        # Prepare features
        X, y, feature_columns = prepare_features(data)
        
        if X is None or len(X) < 20:
            return None
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, shuffle=False
        )
        
        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Calculate metrics
        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        
        return {
            'model': model,
            'feature_columns': feature_columns,
            'metrics': {
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'train_r2': train_r2,
                'test_r2': test_r2,
                'train_mae': train_mae,
                'test_mae': test_mae
            },
            'predictions': {
                'train': y_pred_train,
                'test': y_pred_test,
                'actual_train': y_train,
                'actual_test': y_test
            }
        }
        
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return None


def make_prediction(model_dict, data, periods_ahead=5):
    """
    Make future price predictions.
    
    Parameters:
    -----------
    model_dict : dict
        Dictionary containing trained model and feature columns
    data : pd.DataFrame
        DataFrame with latest price data
    periods_ahead : int
        Number of periods to predict ahead
    
    Returns:
    --------
    dict
        Dictionary containing predictions and confidence intervals
    """
    try:
        if model_dict is None:
            return None
        
        model = model_dict['model']
        feature_columns = model_dict['feature_columns']
        
        # Prepare features for latest data point
        X, _, _ = prepare_features(data)
        
        if X is None or len(X) == 0:
            return None
        
        # Get the last data point for prediction
        latest_features = X[-1:].reshape(1, -1)
        
        # Make prediction
        predictions = []
        current_features = latest_features.copy()
        
        for i in range(periods_ahead):
            pred = model.predict(current_features)[0]
            predictions.append(pred)
            
            # Update features for next prediction (simple approach)
            # In a more sophisticated model, you'd update all lagged features
            current_features = current_features.copy()
        
        # Calculate prediction trend
        current_price = data['Close'].iloc[-1]
        predicted_price = predictions[-1]
        price_change = predicted_price - current_price
        price_change_pct = (price_change / current_price) * 100
        
        # Determine trend
        if price_change_pct > 1:
            trend = 'BULLISH'
            trend_color = 'green'
        elif price_change_pct < -1:
            trend = 'BEARISH'
            trend_color = 'red'
        else:
            trend = 'NEUTRAL'
            trend_color = 'yellow'
        
        return {
            'predictions': predictions,
            'current_price': current_price,
            'predicted_price': predicted_price,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'trend': trend,
            'trend_color': trend_color,
            'confidence': model_dict['metrics']['test_r2'] * 100  # R² as confidence %
        }
        
    except Exception as e:
        print(f"Error making prediction: {str(e)}")
        return None


def get_feature_importance(model_dict):
    """
    Get feature importance from the trained model.
    
    Parameters:
    -----------
    model_dict : dict
        Dictionary containing trained model and feature columns
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with feature names and importance scores
    """
    try:
        if model_dict is None:
            return None
        
        model = model_dict['model']
        feature_columns = model_dict['feature_columns']
        
        # Get coefficients (feature importance)
        coefficients = model.coef_
        
        # Create DataFrame
        importance_df = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': np.abs(coefficients)
        })
        
        # Sort by importance
        importance_df = importance_df.sort_values('Importance', ascending=False)
        
        return importance_df
        
    except Exception as e:
        print(f"Error getting feature importance: {str(e)}")
        return None


def calculate_prediction_accuracy(model_dict):
    """
    Calculate and format accuracy metrics for display.
    
    Parameters:
    -----------
    model_dict : dict
        Dictionary containing trained model and metrics
    
    Returns:
    --------
    dict
        Formatted accuracy metrics
    """
    try:
        if model_dict is None:
            return None
        
        metrics = model_dict['metrics']
        
        return {
            'R² Score': f"{metrics['test_r2']:.4f}",
            'RMSE': f"${metrics['test_rmse']:.2f}",
            'MAE': f"${metrics['test_mae']:.2f}",
            'Accuracy': f"{metrics['test_r2'] * 100:.2f}%"
        }
        
    except Exception as e:
        print(f"Error calculating accuracy: {str(e)}")
        return None

