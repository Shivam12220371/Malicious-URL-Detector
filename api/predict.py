from http.server import BaseHTTPRequestHandler
import json
import joblib
import numpy as np
from scipy.sparse import hstack
from pathlib import Path
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Define feature extraction function
def extract_struct_features(url: str) -> list:
    """Extract structural features from URL."""
    import re
    url = url.strip()
    length = len(url)
    digit_count = sum(ch.isdigit() for ch in url)
    has_https = 1.0 if url.lower().startswith("https") else 0.0
    has_ip = 1.0 if re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", url) else 0.0
    has_at = 1.0 if "@" in url else 0.0
    has_exe = 1.0 if ".exe" in url.lower() else 0.0
    has_dash = url.count("-")
    dot_count = url.count(".")
    slash_count = url.count("/")
    query_count = url.count("?") + url.count("=") + url.count("&")
    subdomain_count = max(dot_count - 1, 0)
    
    suspicious_tokens = ["login", "verify", "update", "secure", "account", "password", "bank", "free", "bonus", "confirm"]
    token_hits = sum(1 for token in suspicious_tokens if token in url.lower())
    
    return [
        float(length), float(digit_count), float(has_https), float(has_ip),
        float(has_at), float(has_exe), float(has_dash), float(dot_count),
        float(slash_count), float(query_count), float(subdomain_count), float(token_hits),
    ]

# Load models at startup
MODEL_PATH = Path(__file__).parent.parent / "backend" / "model.pkl"
VECTORIZER_PATH = Path(__file__).parent.parent / "backend" / "vectorizer.pkl"

model = None
vectorizer = None

def load_models():
    global model, vectorizer
    try:
        if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("Models loaded successfully")
    except Exception as e:
        print(f"Error loading models: {e}")

load_models()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/predict":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                payload = json.loads(body.decode())
                url = payload.get('url', '').strip()
                
                if not url:
                    self.send_error(400, "URL is required")
                    return
                
                if model is None or vectorizer is None:
                    self.send_error(500, "Model not loaded")
                    return
                
                text_features = vectorizer.transform([url])
                struct_features = np.array([extract_struct_features(url)])
                features = hstack([text_features, struct_features])
                
                proba = model.predict_proba(features)[0][1]
                prediction = "Malicious" if proba >= 0.5 else "Safe"
                risk_score = round(float(proba) * 100, 2)
                
                response = {
                    "prediction": prediction,
                    "confidence": round(float(max(proba, 1 - proba)) * 100, 2),
                    "risk_score": risk_score,
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
            except Exception as e:
                self.send_error(500, str(e))
        
        elif self.path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "ok", "model_loaded": model is not None}
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
