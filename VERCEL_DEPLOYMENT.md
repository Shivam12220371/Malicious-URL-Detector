# Vercel Deployment Guide

## Step-by-Step Deployment Instructions

### Step 1: Prepare Your Local Project

Make sure your project has trained models:
```bash
cd backend
python train_model.py --dataset ../dataset/urls.csv
cd ..
```

This creates:
- `backend/model.pkl`
- `backend/vectorizer.pkl`

### Step 2: Initialize Git Repository

```bash
cd /home/shivam-bhardwaj/Desktop/Malicious\ URL\ Detector
git init
git add .
git commit -m "Initial commit - Malicious URL Detector"
```

### Step 3: Push to GitHub

1. Create a new repository on [GitHub.com](https://github.com/new)
2. Copy the repository URL (HTTPS or SSH)
3. Run:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/malicious-url-detector.git
git push -u origin main
```

### Step 4: Deploy on Vercel

**Option A: Using Vercel CLI (Recommended)**

```bash
npm install -g vercel
vercel
```

Follow the prompts:
- Link to GitHub account
- Select your repository
- Choose "Next.js" or "Other" as framework
- Keep default settings
- Deploy!

**Option B: Using Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Log in with GitHub
3. Click "New Project"
4. Click "Import Git Repository"
5. Select your malicious-url-detector repo
6. Configure settings:
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/dist`
   - Root Directory: `.`
7. Click "Deploy"

### Step 5: Update Environment Variables

After deployment, Vercel will give you a URL (e.g., `https://malicious-url-detector-abc123.vercel.app`)

1. Go to Vercel Project Settings → Environment Variables
2. Add: `VITE_API_URL=https://your-deployment.vercel.app`
3. Redeploy

### Step 6: Update CORS (If Needed)

If CORS errors occur, update `backend/main.py`:

```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://your-deployment.vercel.app"  # Add your Vercel URL
]
```

Then push changes:
```bash
git add backend/main.py
git commit -m "Update CORS for Vercel deployment"
git push
```

### Step 7: Test Your Deployment

1. Visit your Vercel URL
2. Test with sample URLs:
   - `https://google.com` (Safe)
   - `https://github.com` (Safe)
   - `http://malware-download.ru/file.exe` (Malicious)
3. Check `/api/health` endpoint for API status

## Troubleshooting

### Models Not Found
- Ensure `model.pkl` and `vectorizer.pkl` are in `backend/`
- Commit and push them to GitHub
- Redeploy on Vercel

### CORS Errors
- Update the `allow_origins` list in `backend/main.py`
- Add your Vercel deployment URL
- Commit and push changes

### Build Fails
- Check build logs in Vercel dashboard
- Ensure `frontend/package.json` has correct dependencies
- Verify `vercel.json` is at project root

## Project Structure

```
.
├── vercel.json                 # Vercel configuration
├── api/                        # Serverless functions
│   ├── predict.py             # API endpoint
│   └── requirements.txt        # Python dependencies
├── backend/
│   ├── main.py                # FastAPI app
│   ├── model.pkl              # Trained model (commit this!)
│   ├── vectorizer.pkl         # TF-IDF vectorizer
│   ├── requirements.txt
│   ├── train_model.py
│   └── feature_engineering.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   └── App.jsx            # React app
│   └── .env.production        # Production env vars
└── dataset/
    └── urls.csv
```

## Important Notes

- Keep `model.pkl` and `vectorizer.pkl` in Git (they're small)
- Frontend auto-deploys on every push to main
- API uses serverless functions (cold starts are normal)
- Monitor usage at [vercel.com/dashboard](https://vercel.com/dashboard)

## Support

For issues:
1. Check Vercel deployment logs
2. Verify all files are committed to Git
3. Ensure backend models are trained before deployment
4. Check CORS settings if API calls fail
