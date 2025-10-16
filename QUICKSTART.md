# 🚀 Quick Start Guide

Get the Smart Gold Trading Dashboard running in 3 simple steps!

## Method 1: Using Startup Scripts (Recommended)

### On macOS/Linux:
```bash
./run.sh
```

### On Windows:
```bash
run.bat
```

That's it! The script will automatically:
- Create a virtual environment
- Install all dependencies
- Launch the dashboard

## Method 2: Manual Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run main.py
```

### Step 3: Login
Open your browser at `http://localhost:8501` and use:
- **Username**: `demo`
- **Password**: `demo123`

## 📱 What You'll See

After logging in, you'll have access to:

1. **📊 Overview** - Real-time gold prices and candlestick charts
2. **📈 Technical Indicators** - RSI, MACD, Moving Averages
3. **🤖 AI Prediction** - Machine learning price forecasts
4. **ℹ️ About** - Dashboard information

## ⚙️ Settings (Sidebar)

Customize your dashboard:
- **Timeframe**: 1 Day to 1 Year
- **Interval**: 1 Minute to 1 Day  
- **Indicators**: Toggle MA, BB, RSI, MACD
- **Auto-Refresh**: Updates every 1 minute

## 🎯 Quick Tips

1. **First Time?** Start with the Overview section
2. **Want Signals?** Check the AI Prediction section
3. **Customize**: Use sidebar settings to adjust your view
4. **Create Account**: Click "Create New Account" to signup
5. **Auto-Refresh**: Enable for live price updates

## ❓ Troubleshooting

**Dashboard won't start?**
```bash
pip install --upgrade -r requirements.txt
```

**Login issues?**
- Delete `config.yaml` to reset
- Use demo credentials: demo/demo123

**No data showing?**
- Check internet connection
- Try different timeframe/interval

## 📚 More Help

See [README.md](README.md) for complete documentation.

---

**Happy Trading! 📈💰**

