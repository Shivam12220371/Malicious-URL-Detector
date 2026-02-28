# Malicious URL Detector

A full-stack malicious URL detection system using machine learning + NLP and a modern frontend.

## What is included

- `backend/` FastAPI inference API
- `backend/train_model.py` training pipeline (TF-IDF + structural URL features + ensemble)
- `backend/feature_engineering.py` handcrafted URL risk features
- `frontend/` React + Vite UI with cyber-themed design and risk meter
- `dataset/urls.csv` starter labeled dataset
- `dataset/build_dataset.py` generator for large synthetic datasets

## ML approach

The model combines:

1. **Character-level TF-IDF** (`3-5` grams) on raw URLs
2. **Structural URL features** (length, dots, special chars, suspicious tokens, `.exe`, IP-host usage, etc.)
3. **Ensemble classifier** using:
   - `LogisticRegression`
   - `RandomForestClassifier`
   - `MultinomialNB`

Final prediction uses soft voting with probability output.

## Backend setup

From project root:

1. Install dependencies:

   - `cd backend`
   - `pip install -r requirements.txt`

2. Train model:

   - `python train_model.py --dataset ../dataset/urls.csv`

   This creates:
   - `backend/model.pkl`
   - `backend/vectorizer.pkl`

3. Start API:

   - `uvicorn main:app --reload`

4. Open API docs:

   - `http://localhost:8000/docs`

## Frontend setup

From project root:

1. Install dependencies:

   - `cd frontend`
   - `npm install`

2. Run dev server:

   - `npm run dev`

3. Open:

   - `http://localhost:5173`

The frontend targets `http://localhost:8000/predict` by default and lets you edit the endpoint in UI.

## API contract

### POST `/predict`

Request JSON:

```json
{
  "url": "http://example.com/login"
}
```

Response JSON:

```json
{
  "prediction": "Malicious",
  "confidence": 93.2,
  "risk_score": 93.2
}
```

## Accuracy expectations

- Accuracy depends on dataset quality and balance.
- With larger, clean, balanced datasets (`urls_large.csv` or external real feeds), this setup generally performs strongly while keeping prediction latency low.

## Make it stronger (optional)

- Merge with public phishing feeds and benign top-domain lists
- Add model calibration and threshold tuning to reduce false negatives
- Add caching and request logging
- Add explainability (feature contribution) for SOC workflows
