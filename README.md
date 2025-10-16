# 🏆 Smart Gold Trading Dashboard

<div align="center">

![Dashboard Preview](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

*A comprehensive trading dashboard for real-time gold price analysis with advanced technical indicators and AI-powered predictions.*

**Created by [Komail Altaf](https://github.com/KomailAltaf)**

[🚀 Live Demo](https://your-demo-link.streamlit.app) | [📖 Documentation](#features) | [🐛 Report Bug](https://github.com/KomailAltaf/trading/issues)

</div>

## ✨ Features

- 🔴 **Real-time Gold Price Data** - Live XAUUSD data from multiple sources
- 📊 **Professional Trading Charts** - Advanced candlestick charts with volume
- 📈 **Technical Indicators** - RSI, Moving Averages, MACD with professional styling
- 🤖 **AI Predictions** - Machine learning model for price forecasting
- 🌙 **Dark Theme** - Professional dark dashboard with gold accents
- 🔄 **Auto-refresh** - Real-time data updates every minute
- 📱 **Responsive Design** - Works perfectly on all devices
- 🔐 **Authentication** - Secure login system
- 📊 **Volume Analysis** - Volume profile and heatmap charts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KomailAltaf/trading.git
   cd trading
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📸 Screenshots

### Dashboard Overview
![Dashboard Overview](screenshots/dashboard-overview.png)
*Main dashboard with real-time gold prices and advanced candlestick charts*

### Technical Analysis
![Technical Analysis](screenshots/technical-analysis.png)
*Comprehensive technical indicators with RSI, MACD, and volume analysis*

### AI Predictions
![AI Predictions](screenshots/ai-predictions.png)
*Machine learning predictions with confidence intervals and performance metrics*

## 🏗️ Project Structure

```
trading/
├── 📁 screenshots/           # Dashboard screenshots
├── 📄 main.py               # Main Streamlit application
├── 📄 data_fetcher.py       # Real-time data fetching
├── 📄 charts.py             # Advanced Plotly charts
├── 📄 indicators.py         # Technical indicator calculations
├── 📄 ai_model.py           # Machine learning model
├── 📄 predictions.py        # Prediction analysis
├── 📄 simple_auth.py        # Authentication system
├── 📄 gold_api.py           # GoldAPI.io integration
├── 📄 free_data_sources.py  # Alternative data sources
├── 📄 requirements.txt      # Python dependencies
├── 📄 README.md            # This file
├── 📄 LICENSE              # MIT License
└── 📄 .env.example         # Environment variables template
```

## 🔧 Configuration

### API Keys (Optional)
For enhanced data quality, create a `.env` file:

```env
# GoldAPI.io (Recommended for real-time gold data)
GOLDAPI_IO_API_KEY=your_goldapi_key_here

# Alpha Vantage (Alternative data source)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

### Data Sources Priority
1. **GoldAPI.io** - Real-time gold spot prices (requires API key)
2. **Yahoo Finance** - Gold futures and ETFs (free)
3. **Alpha Vantage** - FX data (requires API key)
4. **Demo Data** - Realistic fallback data

## 🎯 Features Overview

### 📊 Market Overview
- Live gold price with change indicators
- Advanced candlestick charts with volume
- Moving averages overlay
- Real-time price alerts

### 📈 Technical Analysis
- **RSI (Relative Strength Index)** - Momentum oscillator with overbought/oversold levels
- **Moving Averages** - 20, 50, and 200-day averages with trend analysis
- **MACD** - Moving Average Convergence Divergence with signal line
- **Volume Profile** - Price-volume distribution analysis
- **Price Heatmap** - Hourly price movements by trading sessions

### 🤖 AI Predictions
- Linear regression model for price forecasting
- Confidence intervals and accuracy metrics
- Historical performance analysis
- Real-time prediction updates

### 🎨 User Interface
- Professional dark theme with gold accents
- Responsive design for all devices
- Interactive charts with zoom and pan
- Real-time updates without page refresh
- Secure authentication system

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your forked repository
5. Deploy!

### Local Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py

# Or use the provided script
chmod +x run.sh
./run.sh
```

### Docker (Optional)
```bash
# Build the image
docker build -t gold-trading-dashboard .

# Run the container
docker run -p 8501:8501 gold-trading-dashboard
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit, Plotly
- **Backend**: Python, Pandas, NumPy
- **Data**: yfinance, requests, GoldAPI.io
- **Machine Learning**: scikit-learn
- **Authentication**: Custom implementation
- **Charts**: Advanced Plotly visualizations

## 📊 Performance Features

- **Smart Caching** - 60-second data cache for optimal performance
- **Efficient Processing** - Optimized data handling and calculations
- **Real-time Updates** - Seamless data refresh without page reload
- **Responsive Design** - Fast loading on all devices

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This dashboard is for **educational and informational purposes only**. It is not intended as financial advice. Always do your own research and consult with financial advisors before making investment decisions.

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/KomailAltaf/trading/issues) page
2. Create a new issue with detailed information
3. Contact: [Komail Altaf](https://github.com/KomailAltaf)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=KomailAltaf/trading&type=Date)](https://star-history.com/#KomailAltaf/trading&Date)

---

<div align="center">

**Made with ❤️ by [Komail Altaf](https://github.com/KomailAltaf)**

[![GitHub](https://img.shields.io/badge/GitHub-KomailAltaf-black?style=for-the-badge&logo=github)](https://github.com/KomailAltaf)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Komail_Altaf-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/komailaltaf)

*For the trading community* 🚀

</div>