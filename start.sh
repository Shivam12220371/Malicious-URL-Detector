#!/bin/bash
# Quick start script for Malicious URL Detector project

echo "🚀 Starting Malicious URL Detector..."

# Start Backend
echo "📡 Starting Backend (FastAPI)..."
source .venv/bin/activate
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start Frontend
echo "🎨 Starting Frontend (React + Vite)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both services started!"
echo ""
echo "🌐 Frontend: http://127.0.0.1:5173"
echo "🔌 Backend:  http://127.0.0.1:8000"
echo "📖 API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "💡 To stop services:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Or just press Ctrl+C in this terminal"

# Keep script running
wait
