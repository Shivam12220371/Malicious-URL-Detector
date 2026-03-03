#!/bin/bash
# Stop all running services

echo "🛑 Stopping Malicious URL Detector services..."

# Kill backend
pkill -f "uvicorn main:app"
echo "✓ Backend stopped"

# Kill frontend
pkill -f "vite"
echo "✓ Frontend stopped"

echo ""
echo "✅ All services stopped"
