#!/bin/bash
# Start HTML Web Interface

echo "========================================"
echo "  Starting Copyright Checker (HTML)"
echo "========================================"
echo ""
echo "Open your browser to:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 server.py
