"""
Predictions Module
==================
This module handles the display and formatting of AI predictions.
Provides functions to show prediction results, confidence scores, and trading signals.

Functions:
    - display_prediction_summary: Show prediction summary
    - get_trading_signal: Generate trading signal from prediction
    - format_prediction_metrics: Format metrics for display
"""

import streamlit as st
import pandas as pd


def display_prediction_summary(predictions_dict, col_width=3):
    """
    Display AI prediction summary in Streamlit columns.
    
    Parameters:
    -----------
    predictions_dict : dict
        Dictionary containing prediction results
    col_width : int
        Number of columns for display
    """
    try:
        if predictions_dict is None:
            st.warning("No predictions available. Please ensure model is trained.")
            return
        
        # Create columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Current Price",
                value=f"${predictions_dict['current_price']:.2f}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="Predicted Price",
                value=f"${predictions_dict['predicted_price']:.2f}",
                delta=f"{predictions_dict['price_change']:.2f} ({predictions_dict['price_change_pct']:.2f}%)"
            )
        
        with col3:
            trend_emoji = "📈" if predictions_dict['trend'] == 'BULLISH' else "📉" if predictions_dict['trend'] == 'BEARISH' else "➡️"
            st.metric(
                label="Trend Prediction",
                value=f"{trend_emoji} {predictions_dict['trend']}"
            )
        
        with col4:
            confidence_pct = predictions_dict.get('confidence', 0)
            st.metric(
                label="Model Confidence",
                value=f"{confidence_pct:.1f}%"
            )
        
    except Exception as e:
        st.error(f"Error displaying prediction summary: {str(e)}")


def get_trading_signal(predictions_dict, signals_dict):
    """
    Generate comprehensive trading signal based on AI prediction and technical indicators.
    
    Parameters:
    -----------
    predictions_dict : dict
        AI prediction results
    signals_dict : dict
        Technical indicator signals
    
    Returns:
    --------
    dict
        Trading signal with recommendation
    """
    try:
        if predictions_dict is None or signals_dict is None:
            return None
        
        # Score system
        bullish_score = 0
        bearish_score = 0
        
        # AI Prediction weight (40%)
        if predictions_dict['trend'] == 'BULLISH':
            bullish_score += 40
        elif predictions_dict['trend'] == 'BEARISH':
            bearish_score += 40
        
        # RSI weight (20%)
        if 'RSI' in signals_dict:
            if signals_dict['RSI']['signal'] == 'OVERSOLD':
                bullish_score += 20
            elif signals_dict['RSI']['signal'] == 'OVERBOUGHT':
                bearish_score += 20
        
        # MACD weight (20%)
        if 'MACD' in signals_dict:
            if signals_dict['MACD']['signal'] == 'BULLISH':
                bullish_score += 20
            elif signals_dict['MACD']['signal'] == 'BEARISH':
                bearish_score += 20
        
        # Moving Average weight (20%)
        if 'MA' in signals_dict:
            if signals_dict['MA']['signal'] == 'BULLISH':
                bullish_score += 20
            elif signals_dict['MA']['signal'] == 'BEARISH':
                bearish_score += 20
        
        # Determine final signal
        if bullish_score > bearish_score + 20:
            signal = 'STRONG BUY'
            color = 'green'
            emoji = '🚀'
        elif bullish_score > bearish_score:
            signal = 'BUY'
            color = 'lightgreen'
            emoji = '📈'
        elif bearish_score > bullish_score + 20:
            signal = 'STRONG SELL'
            color = 'red'
            emoji = '📉'
        elif bearish_score > bullish_score:
            signal = 'SELL'
            color = 'lightcoral'
            emoji = '⬇️'
        else:
            signal = 'HOLD'
            color = 'yellow'
            emoji = '➡️'
        
        return {
            'signal': signal,
            'bullish_score': bullish_score,
            'bearish_score': bearish_score,
            'color': color,
            'emoji': emoji,
            'confidence': abs(bullish_score - bearish_score)
        }
        
    except Exception as e:
        st.error(f"Error generating trading signal: {str(e)}")
        return None


def format_prediction_metrics(model_dict):
    """
    Format model performance metrics for display.
    
    Parameters:
    -----------
    model_dict : dict
        Dictionary containing model and metrics
    
    Returns:
    --------
    pd.DataFrame
        Formatted metrics DataFrame
    """
    try:
        if model_dict is None:
            return None
        
        metrics = model_dict['metrics']
        
        data = {
            'Metric': ['R² Score (Test)', 'RMSE (Test)', 'MAE (Test)', 'R² Score (Train)', 'RMSE (Train)', 'MAE (Train)'],
            'Value': [
                f"{metrics['test_r2']:.4f}",
                f"${metrics['test_rmse']:.2f}",
                f"${metrics['test_mae']:.2f}",
                f"{metrics['train_r2']:.4f}",
                f"${metrics['train_rmse']:.2f}",
                f"${metrics['train_mae']:.2f}"
            ],
            'Description': [
                'Model accuracy on test data (0-1, higher is better)',
                'Root Mean Squared Error on test data',
                'Mean Absolute Error on test data',
                'Model accuracy on training data (0-1, higher is better)',
                'Root Mean Squared Error on training data',
                'Mean Absolute Error on training data'
            ]
        }
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"Error formatting metrics: {str(e)}")
        return None


def display_trading_recommendation(trading_signal):
    """
    Display trading recommendation with visual styling.
    
    Parameters:
    -----------
    trading_signal : dict
        Trading signal dictionary
    """
    try:
        if trading_signal is None:
            st.warning("Unable to generate trading recommendation.")
            return
        
        # Display signal with custom styling
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            border-left: 5px solid {trading_signal['color']};
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        ">
            <h2 style="color: {trading_signal['color']}; margin: 0;">
                {trading_signal['emoji']} Trading Signal: {trading_signal['signal']}
            </h2>
            <p style="color: #cccccc; margin-top: 10px;">
                Bullish Score: {trading_signal['bullish_score']}% | 
                Bearish Score: {trading_signal['bearish_score']}% | 
                Signal Strength: {trading_signal['confidence']}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add disclaimer
        st.caption("⚠️ This is an AI-generated signal for educational purposes only. Always do your own research and consult with a financial advisor before trading.")
        
    except Exception as e:
        st.error(f"Error displaying trading recommendation: {str(e)}")


def display_signal_breakdown(signals_dict):
    """
    Display detailed breakdown of all technical signals.
    
    Parameters:
    -----------
    signals_dict : dict
        Technical indicator signals
    """
    try:
        if not signals_dict:
            st.info("No signal data available.")
            return
        
        st.subheader("📊 Technical Indicator Signals")
        
        # Create columns for each indicator
        num_signals = len(signals_dict)
        cols = st.columns(min(num_signals, 4))
        
        for idx, (indicator, signal_data) in enumerate(signals_dict.items()):
            col_idx = idx % 4
            with cols[col_idx]:
                signal_text = signal_data.get('signal', 'N/A')
                color = signal_data.get('color', 'gray')
                
                # Color mapping for display
                color_map = {
                    'green': '🟢',
                    'red': '🔴',
                    'yellow': '🟡',
                    'gray': '⚪'
                }
                
                emoji = color_map.get(color, '⚪')
                
                st.markdown(f"""
                <div style="
                    background-color: #2d2d2d;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    margin: 5px 0;
                ">
                    <h4 style="color: #FFD700; margin: 0;">{indicator}</h4>
                    <p style="color: white; font-size: 18px; margin: 10px 0;">
                        {emoji} {signal_text}
                    </p>
                    <p style="color: #cccccc; font-size: 12px; margin: 0;">
                        {signal_data.get('description', signal_data.get('value', ''))}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error displaying signal breakdown: {str(e)}")


def display_prediction_disclaimer():
    """
    Display disclaimer about AI predictions.
    """
    st.markdown("""
    ---
    ### ⚠️ Important Disclaimer
    
    **This dashboard is for educational and informational purposes only.**
    
    - The AI predictions are based on historical data and technical indicators
    - Past performance does not guarantee future results
    - Gold trading involves substantial risk of loss
    - Always consult with a licensed financial advisor before making investment decisions
    - This tool should not be used as the sole basis for any trading decisions
    
    **Use at your own risk. The creators of this dashboard are not responsible for any trading losses.**
    """)

