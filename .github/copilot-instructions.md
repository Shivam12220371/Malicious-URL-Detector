# Malicious URL Detector - Development Guidelines

This document provides custom instructions for GitHub Copilot in this workspace.

## Project Overview

A full-stack malicious URL detection system using machine learning + NLP with a React frontend and FastAPI backend.

## Technology Stack

- **Backend**: FastAPI, scikit-learn, pandas, numpy, joblib
- **Frontend**: React 18, Vite
- **Deployment**: Vercel (Option 1), Railway + Vercel (Option 2)
- **ML**: TF-IDF + Structural Features + Ensemble Classifier

## Key Directories

- `backend/` - FastAPI inference API
- `frontend/` - React + Vite UI
- `dataset/` - Training data and generator
- `api/` - Serverless functions for Vercel

## Development Workflow

1. **Backend**: `cd backend && pip install -r requirements.txt`
2. **Train Model**: `python train_model.py --dataset ../dataset/urls.csv`
3. **Start API**: `uvicorn main:app --reload`
4. **Frontend**: `cd frontend && npm install && npm run dev`

## Important API Endpoints

- Local development: `http://localhost:8000/api/predict`
- Production: `https://your-domain.vercel.app/api/predict`

## Deployment

For Vercel deployment, see VERCEL_DEPLOYMENT.md for detailed instructions.
