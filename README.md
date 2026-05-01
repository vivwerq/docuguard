# DocuGuard Document Forensics API

**DocuGuard** is a lightweight, high-performance Document Risk Engine built for Indian Fintechs. It analyzes KYC documents, bank statements, and ID cards (Aadhaar, PAN) to detect digital manipulation, forged data, and WhatsApp-forward compression artifacts—all in under 200ms.

Instead of relying on heavy machine learning models, DocuGuard uses a multi-signal rules engine based on foundational digital forensics to provide an immediate, explainable Risk Score.

## Core Signals
1. **Error Level Analysis (ELA)**: Re-compresses the image to detect anomalous brightness signatures typical in copy-pasted edits.
2. **Metadata Integrity**: Deep EXIF inspection for missing fields, inconsistent timestamps, or software signatures indicating tools like Photoshop or Canva.
3. **Noise Fingerprint**: Analyzes pixel-level sensor noise variance to catch blurred or AI-generated patches.
4. **Layout Consistency**: Validates aspect ratios and edge contours against standard ID templates to catch bad crops or screenshots.
5. **Perceptual Hashing (dHash)**: Computes a difference hash to help you deduplicate uploads or match against known fraudulent documents.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+

### Installation
1. Clone this repository or navigate to the directory:
   ```bash
   cd /path/to/docuguard
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server
Start the FastAPI server using Uvicorn:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
Once the server starts, open **`http://localhost:8000`** in your browser. You will see the interactive **Live Forensic Analyzer** dashboard, which is served natively by the backend.

---

## 💻 API Documentation

**Endpoint:** `POST /v1/analyze`

The API requires an `X-API-Key` header for authentication when deployed to production. (For local development on `127.0.0.1`, the API key check is bypassed).

### Example cURL Request
```bash
curl -X POST http://localhost:8000/v1/analyze \
  -H "X-API-Key: sandbox_sk_12345" \
  -F "file=@your_document.jpg"
```

### Example Python (Requests)
```python
import requests

url = "http://localhost:8000/v1/analyze"
headers = {"X-API-Key": "sandbox_sk_12345"}
files = {"file": open("your_document.jpg", "rb")}

response = requests.post(url, headers=headers, files=files)
print(response.json())
```

### JSON Response Schema
The API responds with a detailed breakdown of the risk score, explanations, and an embedded Base64 Heatmap for visual proof of tampering.

```json
{
  "risk_score": 0.82,
  "risk_level": "high",
  "confidence": 0.92,
  "signals": {
    "ela": 0.90,
    "metadata": 0.80,
    "compression": 0.40,
    "structure": 0.10
  },
  "explanations": [
    "Suspicious editing software detected: Adobe Photoshop CC 2021",
    "High ELA anomaly detected (possible pixel manipulation)"
  ],
  "document_hash": "c08000ff001f3e00",
  "visual_proof": "data:image/jpeg;base64,/9j/4AAQSk..."
}
```

---

## ☁️ Deployment

This project is configured out-of-the-box for cloud deployment.

### Vercel (Serverless)
The repository includes a `vercel.json` file.
1. Push this code to GitHub.
2. Import the repository into Vercel.
3. Vercel will automatically route `/v1/*` requests to the Python Serverless engine and serve the static `index.html` on the root domain.

### Railway (Containerized)
The repository includes a `Procfile` and `runtime.txt`.
1. Connect your GitHub repository to Railway.
2. Railway will automatically detect the Python environment, install `requirements.txt`, and start the Uvicorn server, hosting both the backend API and frontend dashboard as a unified service.
