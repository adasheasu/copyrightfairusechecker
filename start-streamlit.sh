#!/bin/bash
# Start Streamlit Web App

echo "========================================"
echo "  Starting Copyright Checker (Streamlit)"
echo "========================================"
echo ""
echo "Opening in your browser..."
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 -m streamlit run app.py
