# Malicious URL Detector - Quick Start Commands

## ⚡ Fastest Way (Automatic)

Open VS Code terminal and run:

```bash
bash start.sh
```

This starts both backend and frontend automatically.

---

## 🔧 Manual Way (Step by Step)

### Option 1: Two Separate Terminals

**Terminal 1 - Backend:**
```bash
source .venv/bin/activate
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 2: Single Terminal (Background Processes)

```bash
# Start backend in background
source .venv/bin/activate && cd backend && uvicorn main:app --host 127.0.0.1 --port 8000 &

# Start frontend in background
cd frontend && npm run dev &
```

---

## 🌐 Access URLs

After starting:

| Service | URL |
|---------|-----|
| **Frontend** | http://127.0.0.1:5173 |
| **Backend API** | http://127.0.0.1:8000 |
| **API Docs** | http://127.0.0.1:8000/docs |

---

## 🛑 Stop Services

### If running in foreground:
Press `Ctrl + C` in each terminal

### If running in background:
```bash
# Stop all
pkill -f "uvicorn main:app"
pkill -f "vite"

# Or find process IDs
ps aux | grep -E "(uvicorn|vite)" | grep -v grep
kill <PID>
```

---

## ✅ Verify Services Running

```bash
# Check if backend is responding
curl http://127.0.0.1:8000/docs

# Check if frontend is up
curl http://127.0.0.1:5173
```

---

## 🔍 Troubleshooting

**Port already in use?**
```bash
# Check what's using ports
lsof -i :8000
lsof -i :5173

# Kill process on port
kill -9 $(lsof -t -i:8000)
kill -9 $(lsof -t -i:5173)
```

**Backend shows "model not found"?**
```bash
# Retrain model
source .venv/bin/activate
cd backend
python train_model.py --dataset ../dataset/urls.csv
```

**Dependencies missing?**
```bash
# Reinstall backend
source .venv/bin/activate
pip install -r backend/requirements.txt

# Reinstall frontend
cd frontend
npm install
```
