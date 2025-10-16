#!/bin/bash

# Smart Gold Trading Dashboard - Startup Script
# This script sets up and runs the Streamlit dashboard

echo "🏆 Starting Smart Gold Trading Dashboard..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing/updating dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Launching dashboard..."
echo ""
echo "📌 Login credentials:"
echo "   Username: demo"
echo "   Password: demo123"
echo ""

# Run Streamlit
streamlit run main.py

