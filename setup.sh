#!/bin/bash
echo "🔧 Installing Chromium for Playwright..."
playwright install chromium
echo "🚀 Starting bot..."
python main.py
