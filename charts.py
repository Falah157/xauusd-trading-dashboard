"""
Advanced Charts Module
======================
Professional trading charts with advanced Plotly features.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st


def create_advanced_candlestick_chart(data, title="Gold Price Chart"):
    """
    Create an advanced candlestick chart with professional styling.
    """
    try:
        # Create subplots with secondary y-axis for volume
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(title, 'Volume'),
            row_width=[0.7, 0.3]
        )
        
        # Main candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="Gold Price",
                increasing_line_color='#00ff88',
                decreasing_line_color='#ff4444',
                increasing_fillcolor='rgba(0, 255, 136, 0.3)',
                decreasing_fillcolor='rgba(255, 68, 68, 0.3)',
                line=dict(width=1)
            ),
            row=1, col=1
        )
        
        # Volume bars
        colors = ['#00ff88' if close >= open else '#ff4444' 
                 for close, open in zip(data['Close'], data['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=data['Datetime'],
                y=data['Volume'],
                name="Volume",
                marker_color=colors,
                opacity=0.7
            ),
            row=2, col=1
        )
        
        # Add moving averages
        if len(data) >= 20:
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['MA50'] = data['Close'].rolling(window=50).mean()
            
            fig.add_trace(
                go.Scatter(
                    x=data['Datetime'],
                    y=data['MA20'],
                    mode='lines',
                    name='MA 20',
                    line=dict(color='#ffa500', width=2),
                    opacity=0.8
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data['Datetime'],
                    y=data['MA50'],
                    mode='lines',
                    name='MA 50',
                    line=dict(color='#00bfff', width=2),
                    opacity=0.8
                ),
                row=1, col=1
            )
        
        # Update layout with professional styling
        fig.update_layout(
            title={
                'text': f"<b>{title}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#ffd700'}
            },
            xaxis_rangeslider_visible=False,
            height=700,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0.8)',
                font=dict(color='white')
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=50, r=50, t=80, b=50),
            hovermode='x unified',
            dragmode='zoom',
            modebar=dict(
                bgcolor='rgba(0,0,0,0.8)',
                color='white',
                activecolor='#ffd700'
            )
        )
        
        # Update axes styling
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255,255,255,0.1)',
            color='white',
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255,255,255,0.1)',
            color='white',
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating candlestick chart: {str(e)}")
        return None


def create_price_chart_with_indicators(data, title="Gold Price Analysis"):
    """
    Create a comprehensive chart with price and technical indicators.
    """
    try:
        # Create subplots
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,
            subplot_titles=('Price & Moving Averages', 'RSI', 'MACD', 'Volume'),
            row_heights=[0.5, 0.2, 0.2, 0.1]
        )
        
        # Price chart with candlesticks
        fig.add_trace(
            go.Candlestick(
                x=data['Datetime'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="Gold Price",
                increasing_line_color='#00ff88',
                decreasing_line_color='#ff4444',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Moving averages
        if len(data) >= 20:
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['MA50'] = data['Close'].rolling(window=50).mean()
            
            fig.add_trace(
                go.Scatter(x=data['Datetime'], y=data['MA20'], 
                          mode='lines', name='MA 20', line=dict(color='#ffa500', width=2)),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=data['Datetime'], y=data['MA50'], 
                          mode='lines', name='MA 50', line=dict(color='#00bfff', width=2)),
                row=1, col=1
            )
        
        # RSI
        if len(data) >= 14:
            rsi = calculate_rsi(data['Close'])
            fig.add_trace(
                go.Scatter(x=data['Datetime'], y=rsi, mode='lines', 
                          name='RSI', line=dict(color='#ff69b4', width=2)),
                row=2, col=1
            )
            
            # RSI levels
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        if len(data) >= 26:
            macd_line, signal_line, histogram = calculate_macd(data['Close'])
            fig.add_trace(
                go.Scatter(x=data['Datetime'], y=macd_line, mode='lines', 
                          name='MACD', line=dict(color='#00ff88', width=2)),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=data['Datetime'], y=signal_line, mode='lines', 
                          name='Signal', line=dict(color='#ff4444', width=2)),
                row=3, col=1
            )
            fig.add_trace(
                go.Bar(x=data['Datetime'], y=histogram, name='Histogram', 
                      marker_color=['green' if x >= 0 else 'red' for x in histogram]),
                row=3, col=1
            )
        
        # Volume
        colors = ['#00ff88' if close >= open else '#ff4444' 
                 for close, open in zip(data['Close'], data['Open'])]
        fig.add_trace(
            go.Bar(x=data['Datetime'], y=data['Volume'], name='Volume', 
                  marker_color=colors, opacity=0.7),
            row=4, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f"<b>{title}</b>",
            height=900,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0.8)'
            )
        )
        
        # Update axes
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white')
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating indicators chart: {str(e)}")
        return None


def create_price_prediction_chart(data, predictions, title="Gold Price Prediction"):
    """
    Create a chart showing historical data and future predictions.
    """
    try:
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(
            go.Scatter(
                x=data['Datetime'],
                y=data['Close'],
                mode='lines',
                name='Historical Price',
                line=dict(color='#00ff88', width=3)
            )
        )
        
        # Predictions
        if predictions and len(predictions) > 0:
            pred_dates = pd.date_range(start=data['Datetime'].iloc[-1], periods=len(predictions)+1, freq='H')[1:]
            
            fig.add_trace(
                go.Scatter(
                    x=pred_dates,
                    y=predictions,
                    mode='lines+markers',
                    name='AI Predictions',
                    line=dict(color='#ffd700', width=3, dash='dash'),
                    marker=dict(size=6, color='#ffd700')
                )
            )
        
        # Current price marker
        last_price = data['Close'].iloc[-1]
        last_time = data['Datetime'].iloc[-1]
        
        fig.add_trace(
            go.Scatter(
                x=[last_time],
                y=[last_price],
                mode='markers',
                name='Current Price',
                marker=dict(size=12, color='#ff4444', symbol='diamond'),
                showlegend=True
            )
        )
        
        # Update layout
        fig.update_layout(
            title=f"<b>{title}</b>",
            height=600,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(0,0,0,0.8)'
            ),
            hovermode='x unified'
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white')
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating prediction chart: {str(e)}")
        return None


def create_volume_profile_chart(data, title="Volume Profile"):
    """
    Create a volume profile chart showing price vs volume distribution.
    """
    try:
        # Calculate volume profile
        price_bins = np.linspace(data['Low'].min(), data['High'].max(), 20)
        volume_profile = []
        
        for i in range(len(price_bins)-1):
            volume_sum = data[(data['Close'] >= price_bins[i]) & 
                            (data['Close'] < price_bins[i+1])]['Volume'].sum()
            volume_profile.append(volume_sum)
        
        price_centers = [(price_bins[i] + price_bins[i+1]) / 2 for i in range(len(price_bins)-1)]
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=volume_profile,
                y=price_centers,
                orientation='h',
                name='Volume Profile',
                marker=dict(
                    color=volume_profile,
                    colorscale='Viridis',
                    opacity=0.7
                )
            )
        )
        
        fig.update_layout(
            title=f"<b>{title}</b>",
            height=600,
            xaxis_title="Volume",
            yaxis_title="Price",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white')
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating volume profile: {str(e)}")
        return None


# Helper functions for technical indicators
def calculate_rsi(prices, period=14):
    """Calculate RSI indicator."""
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    except:
        return pd.Series([50] * len(prices))


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD indicator."""
    try:
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    except:
        zeros = pd.Series([0] * len(prices))
        return zeros, zeros, zeros


def create_heatmap_chart(data, title="Price Heatmap"):
    """
    Create a heatmap showing price movements over time.
    """
    try:
        # Create hourly price changes
        data['Hour'] = data['Datetime'].dt.hour
        data['Day'] = data['Datetime'].dt.day_name()
        
        pivot_data = data.pivot_table(
            values='Close', 
            index='Day', 
            columns='Hour', 
            aggfunc='mean'
        )
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_data = pivot_data.reindex([day for day in day_order if day in pivot_data.index])
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Price", titlefont=dict(color='white'), tickfont=dict(color='white'))
        ))
        
        fig.update_layout(
            title=f"<b>{title}</b>",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        fig.update_xaxes(color='white')
        fig.update_yaxes(color='white')
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating heatmap: {str(e)}")
        return None