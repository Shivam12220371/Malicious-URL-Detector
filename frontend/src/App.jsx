import { useMemo, useState } from "react";

const DEFAULT_API = "http://localhost:8000/predict";

const sampleChecks = [
  "https://github.com",
  "https://google.com",
  "http://secure-login-paypal.com",
  "http://malware-download.ru/file.exe"
];

function getRiskLabel(score) {
  if (score >= 80) return "Critical";
  if (score >= 60) return "High";
  if (score >= 35) return "Medium";
  return "Low";
}

export default function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiUrl, setApiUrl] = useState(DEFAULT_API);
  const [error, setError] = useState("");

  const riskLabel = useMemo(() => {
    if (!result) return "";
    return getRiskLabel(result.risk_score);
  }, [result]);

  const scanUrl = async (value) => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: value })
      });

      if (!response.ok) {
        const message = await response.json();
        throw new Error(message.detail || "Prediction failed.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = (event) => {
    event.preventDefault();
    if (!url.trim()) return;
    scanUrl(url.trim());
  };

  return (
    <div className="app">
      <div className="grid" />
      <header className="header">
        <div>
          <p className="kicker">AI-powered security scanner</p>
          <h1>Malicious URL Detector</h1>
          <p className="subtitle">
            NLP + structural URL intelligence with ensemble ML. Results in seconds.
          </p>
        </div>
        <div className="badge">Live</div>
      </header>

      <section className="panel">
        <form onSubmit={onSubmit} className="input-row">
          <input
            type="text"
            placeholder="Paste any URL to scan..."
            value={url}
            onChange={(event) => setUrl(event.target.value)}
          />
          <button type="submit" disabled={loading}>
            {loading ? "Scanning..." : "Scan URL"}
          </button>
        </form>

        <div className="api-row">
          <label>API Endpoint</label>
          <input
            type="text"
            value={apiUrl}
            onChange={(event) => setApiUrl(event.target.value)}
          />
        </div>

        {error && <div className="error">{error}</div>}

        {result && (
          <div className={`result ${result.prediction.toLowerCase()}`}>
            <div>
              <p className="label">Prediction</p>
              <h2>{result.prediction}</h2>
            </div>
            <div>
              <p className="label">Confidence</p>
              <h3>{result.confidence}%</h3>
            </div>
            <div>
              <p className="label">Risk Score</p>
              <h3>
                {result.risk_score}% <span>({riskLabel})</span>
              </h3>
            </div>
          </div>
        )}

        <div className="sample-row">
          <p>Quick samples:</p>
          {sampleChecks.map((item) => (
            <button
              key={item}
              type="button"
              className="ghost"
              onClick={() => {
                setUrl(item);
                scanUrl(item);
              }}
            >
              {item}
            </button>
          ))}
        </div>
      </section>

      <section className="features">
        <div>
          <h3>Instant scanning</h3>
          <p>Cached ML artifacts + char-level TF-IDF for sub-second responses.</p>
        </div>
        <div>
          <h3>Explainable risk</h3>
          <p>Risk score derived from ensemble probability.</p>
        </div>
        <div>
          <h3>Cyber UI</h3>
          <p>Minimal dark interface tuned for security workflows.</p>
        </div>
      </section>
    </div>
  );
}
