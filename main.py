"""
Smart Gold Trading Dashboard
============================
A comprehensive trading dashboard with real-time gold price analysis,
technical indicators, and AI-powered predictions.

Author: Komail Altaf
GitHub: https://github.com/KomailAltaf
Version: 1.0.0
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import time
from datetime import datetime

# Import custom modules
import data_fetcher
import indicators
import charts
import ai_model
import predictions
import simple_auth

# Import free_data_sources if available
try:
    import free_data_sources
except:
    free_data_sources = None

# Page configuration
st.set_page_config(
    page_title="Smart Gold Trading Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_custom_css():
    """Load custom CSS for dark theme with gold accents."""
    st.markdown("""
    <style>
        /* Main background and theme */
        .main {
            background-color: #0E1117;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e1e1e 0%, #0E1117 100%);
        }
        
        /* Headers with gold color */
        h1, h2, h3 {
            color: #FFD700 !important;
        }
        
        /* Metric containers */
        [data-testid="stMetricValue"] {
            color: #FFD700;
            font-size: 28px;
        }
        
        /* Cards and containers */
        .element-container {
            background-color: #1e1e1e;
            border-radius: 10px;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #000000;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
        }
        
        /* Selectbox and inputs */
        .stSelectbox, .stTextInput {
            color: #FFD700;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #1e1e1e;
            border-radius: 8px 8px 0 0;
            color: #cccccc;
            padding: 10px 20px;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #2d2d2d;
            color: #FFD700;
            border-bottom: 3px solid #FFD700;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #2d2d2d;
            border-radius: 8px;
            color: #FFD700;
        }
        
        /* Info boxes */
        .stAlert {
            background-color: #2d2d2d;
            border-left: 4px solid #FFD700;
        }
        
        /* DataFrame */
        .dataframe {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #FFD700;
        }
        
        /* Gold accent line */
        .gold-line {
            height: 3px;
            background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
            margin: 20px 0;
        }
        
        /* Custom card */
        .custom-card {
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #FFD700;
            margin: 10px 0;
        }
        
        /* Live indicator */
        .live-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background-color: #00FF00;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)


def create_header():
    """Create dashboard header with live price."""
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 48px; margin: 0;">
            🏆 Smart Gold Trading Dashboard
        </h1>
        <p style="color: #cccccc; font-size: 18px; margin-top: 10px;">
            Real-time Gold Analysis with AI-Powered Predictions
        </p>
    </div>
    <div class="gold-line"></div>
    """, unsafe_allow_html=True)


def sidebar_settings():
    """Create sidebar with user settings."""
    with st.sidebar:
        st.markdown("## ⚙️ Dashboard Settings")
        
        # Timeframe selection
        timeframe = st.selectbox(
            "📊 Timeframe",
            options=["1 Day", "5 Days", "1 Month", "3 Months", "6 Months", "1 Year"],
            index=2
        )
        
        # Interval selection
        interval = st.selectbox(
            "⏱️ Data Interval",
            options=["1 Minute", "5 Minutes", "15 Minutes", "30 Minutes", "1 Hour", "1 Day"],
            index=4
        )
        
        # Indicator toggles
        st.markdown("### 📈 Technical Indicators")
        show_ma = st.checkbox("Moving Averages", value=True)
        show_bb = st.checkbox("Bollinger Bands", value=False)
        show_rsi = st.checkbox("RSI", value=True)
        show_macd = st.checkbox("MACD", value=True)
        
        # Auto-refresh toggle
        st.markdown("### 🔄 Auto Refresh")
        auto_refresh = st.checkbox("Enable Auto-Refresh (1 min)", value=True)
        
        # Theme toggle (visual only)
        st.markdown("### 🎨 Theme")
        theme = st.radio("Color Accent", ["Gold", "Silver", "Bronze"], index=0)
        
        return {
            'timeframe': timeframe,
            'interval': interval,
            'show_ma': show_ma,
            'show_bb': show_bb,
            'show_rsi': show_rsi,
            'show_macd': show_macd,
            'auto_refresh': auto_refresh,
            'theme': theme
        }


def convert_timeframe(timeframe):
    """Convert user-friendly timeframe to yfinance format."""
    mapping = {
        "1 Day": "1d",
        "5 Days": "5d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y"
    }
    return mapping.get(timeframe, "1mo")


def convert_interval(interval):
    """Convert user-friendly interval to yfinance format."""
    mapping = {
        "1 Minute": "1m",
        "5 Minutes": "5m",
        "15 Minutes": "15m",
        "30 Minutes": "30m",
        "1 Hour": "1h",
        "1 Day": "1d"
    }
    return mapping.get(interval, "1h")


def overview_section(data, latest_price, settings):
    """Display overview section with key metrics and charts."""
    st.header("📊 Market Overview")
    
    # Display live indicator
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="live-indicator"></span>
        <span style="color: #00FF00; margin-left: 10px; font-size: 14px;">LIVE</span>
        <span style="color: #cccccc; margin-left: 10px;">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    if latest_price:
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="💰 Current Price",
                value=f"${latest_price['price']:.2f}",
                delta=f"{latest_price['change']:.2f} ({latest_price['change_pct']:.2f}%)"
            )
        
        with col2:
            st.metric(
                label="📈 24h High",
                value=f"${latest_price['high']:.2f}"
            )
        
        with col3:
            st.metric(
                label="📉 24h Low",
                value=f"${latest_price['low']:.2f}"
            )
        
        with col4:
            st.metric(
                label="🔓 Open",
                value=f"${latest_price['open']:.2f}"
            )
        
        with col5:
            st.metric(
                label="📊 Volume",
                value=f"{latest_price['volume']:,}"
            )
        
        st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
    
    # Advanced candlestick chart with volume
    if data is not None and not data.empty:
        fig = charts.create_advanced_candlestick_chart(data, "Gold Price Chart")
        if fig:
            st.plotly_chart(fig, use_container_width=True)


def technical_indicators_section(data, settings):
    """Display technical indicators section."""
    st.header("📈 Technical Indicators")
    
    if data is None or data.empty:
        st.warning("No data available for technical indicators.")
        return
    
    # Get signal interpretations
    signals = indicators.get_signal_interpretation(data)
    
    # Display signal breakdown
    predictions.display_signal_breakdown(signals)
    
    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
    
    # Advanced comprehensive chart with all indicators
    fig = charts.create_price_chart_with_indicators(data, "Gold Price Analysis with Technical Indicators")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional charts in tabs
    tab1, tab2, tab3 = st.tabs(["Volume Profile", "Price Heatmap", "Indicator Analysis"])
    
    with tab1:
        fig_volume = charts.create_volume_profile_chart(data, "Volume Profile Analysis")
        if fig_volume:
            st.plotly_chart(fig_volume, use_container_width=True)
    
    with tab2:
        fig_heatmap = charts.create_heatmap_chart(data, "Price Movement Heatmap")
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab3:
        st.subheader("📊 Technical Analysis Summary")
        
        # Calculate basic indicators for summary
        if len(data) >= 20:
            ma20 = data['Close'].rolling(window=20).mean().iloc[-1]
            ma50 = data['Close'].rolling(window=50).mean().iloc[-1] if len(data) >= 50 else None
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("MA 20", f"${ma20:.2f}")
            
            with col2:
                if ma50:
                    st.metric("MA 50", f"${ma50:.2f}")
            
            with col3:
                current_price = data['Close'].iloc[-1]
                if ma20:
                    if current_price > ma20:
                        st.success("✅ Above MA 20 (Bullish)")
                    else:
                        st.warning("⚠️ Below MA 20 (Bearish)")
            st.subheader("Moving Averages Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            if 'MA_20' in data.columns:
                with col1:
                    ma20_value = data['MA_20'].iloc[-1]
                    current_price = data['Close'].iloc[-1]
                    st.metric("MA 20", f"${ma20_value:.2f}", 
                             delta=f"{current_price - ma20_value:.2f}")
            
            if 'MA_50' in data.columns:
                with col2:
                    ma50_value = data['MA_50'].iloc[-1]
                    current_price = data['Close'].iloc[-1]
                    st.metric("MA 50", f"${ma50_value:.2f}",
                             delta=f"{current_price - ma50_value:.2f}")
            
            if 'MA_200' in data.columns and data['MA_200'].notna().any():
                with col3:
                    ma200_value = data['MA_200'].iloc[-1]
                    current_price = data['Close'].iloc[-1]
                    st.metric("MA 200", f"${ma200_value:.2f}",
                             delta=f"{current_price - ma200_value:.2f}")


def ai_prediction_section(data):
    """Display AI prediction section."""
    st.header("🤖 AI Price Prediction")
    
    if data is None or data.empty:
        st.warning("No data available for predictions.")
        return
    
    with st.spinner("Training AI model and generating predictions..."):
        # Train model
        model_dict = ai_model.train_model(data)
        
        if model_dict is None:
            st.error("Unable to train prediction model. Insufficient data.")
            return
        
        # Make predictions
        prediction_dict = ai_model.make_prediction(model_dict, data, periods_ahead=5)
        
        if prediction_dict is None:
            st.error("Unable to generate predictions.")
            return
        
        # Display prediction summary
        predictions.display_prediction_summary(prediction_dict)
        
        st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
        
        # Create two columns for chart and metrics
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Advanced prediction chart
            predictions_list = prediction_dict.get('predictions', [])
            fig_pred = charts.create_price_prediction_chart(data, predictions_list, "Gold Price Prediction")
            if fig_pred:
                st.plotly_chart(fig_pred, use_container_width=True)
        
        with col2:
            # Model metrics
            st.subheader("📊 Model Performance")
            metrics_df = predictions.format_prediction_metrics(model_dict)
            if metrics_df is not None:
                st.dataframe(metrics_df, hide_index=True, use_container_width=True)
        
        st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
        
        # Trading signal
        signals = indicators.get_signal_interpretation(data)
        trading_signal = predictions.get_trading_signal(prediction_dict, signals)
        predictions.display_trading_recommendation(trading_signal)
        
        # Disclaimer
        predictions.display_prediction_disclaimer()


def about_section():
    """Display about section."""
    st.header("ℹ️ About This Dashboard")
    
    st.markdown("""
    ### 🏆 Smart Gold Trading Dashboard
    
    Welcome to the **Smart Gold Trading Dashboard** - your comprehensive tool for gold (XAUUSD) market analysis!
    
    #### 🌟 Features
    
    - **Real-Time Data**: Live gold prices from Yahoo Finance, updated every minute
    - **Technical Indicators**: 
      - RSI (Relative Strength Index)
      - Moving Averages (20, 50, 200-day)
      - MACD (Moving Average Convergence Divergence)
      - Bollinger Bands
    - **AI Predictions**: Linear Regression model for short-term price forecasting
    - **Interactive Charts**: Beautiful Plotly visualizations with candlestick charts
    - **Trading Signals**: Combined analysis from technical indicators and AI predictions
    
    #### 📊 How to Use
    
    1. **Overview**: View current gold prices and market trends
    2. **Technical Indicators**: Analyze RSI, MACD, and Moving Averages
    3. **AI Prediction**: Get AI-powered price forecasts and trading signals
    4. **Settings**: Customize timeframe, intervals, and displayed indicators
    
    #### ⚠️ Disclaimer
    
    This dashboard is for **educational and informational purposes only**. 
    - Trading gold involves substantial risk
    - Past performance does not guarantee future results
    - Always consult with a licensed financial advisor
    - Do your own research before making any investment decisions
    
    #### 🛠️ Technologies Used
    
    - **Frontend**: Streamlit
    - **Data**: Yahoo Finance API (yfinance)
    - **Charts**: Plotly
    - **Indicators**: TA-Lib, pandas-ta
    - **Machine Learning**: scikit-learn
    - **Authentication**: streamlit-authenticator
    
    #### 📝 Version
    
    **Version 1.0.0** - Initial Release
    
    ---
    
    #### 📧 Support
    
    For questions or support, please visit our GitHub repository.
    
    #### ⭐ Feedback
    
    We appreciate your feedback! Please star our repository if you find this dashboard useful.
    
    ---
    
    <div style="text-align: center; margin-top: 30px; padding: 20px; background-color: #2d2d2d; border-radius: 10px;">
        <p style="color: #FFD700; font-size: 18px; margin: 0;">
            Happy Trading! 📈💰
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application logic."""
    # Load custom CSS
    load_custom_css()
    
    # Check authentication
    is_authenticated, username, name = simple_auth.check_authentication()
    
    if not is_authenticated:
        st.stop()
    
    # Display logout button
    simple_auth.display_logout_button()
    
    # Create header
    create_header()
    
    # Sidebar settings
    settings = sidebar_settings()
    
    # Convert settings to API format
    period = convert_timeframe(settings['timeframe'])
    interval = convert_interval(settings['interval'])
    
    # Navigation menu
    with st.sidebar:
        st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
        selected = option_menu(
            menu_title="Navigation",
            options=["Overview", "Technical Indicators", "AI Prediction", "Data Sources", "About"],
            icons=["graph-up", "bar-chart-line", "robot", "database", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#1e1e1e"},
                "icon": {"color": "#FFD700", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "#cccccc"
                },
                "nav-link-selected": {"background-color": "#2d2d2d", "color": "#FFD700"},
            }
        )
    
    # Fetch data
    with st.spinner("Fetching gold price data..."):
        data = data_fetcher.fetch_gold_data(period=period, interval=interval)
        
        if data is not None and not data.empty:
            # Add indicators
            data = indicators.add_all_indicators(data)
            
            # Get latest price
            latest_price = data_fetcher.get_latest_price(data)
        else:
            latest_price = None
    
    # Display selected section
    if selected == "Overview":
        overview_section(data, latest_price, settings)
    elif selected == "Technical Indicators":
        technical_indicators_section(data, settings)
    elif selected == "AI Prediction":
        ai_prediction_section(data)
    elif selected == "Data Sources":
        if free_data_sources:
            free_data_sources.get_free_data_sources_info()
        else:
            st.info("Data Sources module not available. Check the Data Sources section in About for more information.")
    elif selected == "About":
        about_section()
    
    # Auto-refresh
    if settings['auto_refresh']:
        time.sleep(60)  # Wait 1 minute
        st.rerun()


if __name__ == "__main__":
    main()

