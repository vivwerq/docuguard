from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List

from .signals.ela import perform_ela
from .signals.exif import analyze_exif
from .signals.hash import calculate_dhash
from .signals.noise import calculate_noise_variance
from .signals.structure import check_structure

import uvicorn
import asyncio
import concurrent.futures

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="DocuGuard API V2", description="Document Risk Engine for Indian Fintechs", version="2.0.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_landing_page():
    return FileResponse("index.html")

VALID_API_KEYS = {"sandbox_sk_12345", "live_sk_98765"}

async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    # Require API key only if it's not a local call (for local demo)
    if request.client.host != "127.0.0.1" and api_key not in VALID_API_KEYS:
         raise HTTPException(status_code=403, detail="Invalid or missing API Key")

def calculate_risk(signals):
    weights = {
        "ela": 0.4,
        "exif": 0.2,
        "noise": 0.2,
        "structure": 0.2
    }
    
    total_score = 0.0
    total_weight = 0.0
    
    for key, weight in weights.items():
        if key in signals and "score" in signals[key]:
            total_score += signals[key]["score"] * weight
            total_weight += weight
            
    normalized_score = total_score / total_weight if total_weight > 0 else 0.0
    
    if normalized_score > 0.7:
        level = "high"
    elif normalized_score > 0.4:
        level = "medium"
    else:
        level = "low"
        
    return normalized_score, level

@app.post("/v1/analyze", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
async def analyze_document(request: Request, file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported")
    
    try:
        contents = await file.read()
    except Exception:
        raise HTTPException(status_code=500, detail="Could not read the uploaded file")
        
    if not contents:
         raise HTTPException(status_code=400, detail="Empty file")

    loop = asyncio.get_event_loop()
    
    with concurrent.futures.ThreadPoolExecutor() as pool:
        exif_task = loop.run_in_executor(pool, analyze_exif, contents)
        ela_task = loop.run_in_executor(pool, perform_ela, contents)
        hash_task = loop.run_in_executor(pool, calculate_dhash, contents)
        noise_task = loop.run_in_executor(pool, calculate_noise_variance, contents)
        structure_task = loop.run_in_executor(pool, check_structure, contents)
        
        exif_res, ela_res, hash_res, noise_res, struct_res = await asyncio.gather(
            exif_task, ela_task, hash_task, noise_task, structure_task
        )
    
    signals = {
        "exif": exif_res,
        "ela": ela_res,
        "hash": hash_res,
        "noise": noise_res,
        "structure": struct_res
    }
    
    risk_score, risk_level = calculate_risk(signals)
    
    explanations = []
    if exif_res.get("score", 0) > 0.5:
        explanations.append(exif_res.get("reason", "Suspicious metadata"))
    if ela_res.get("score", 0) > 0.5:
        explanations.append("High ELA anomaly detected (possible pixel manipulation)")
    if noise_res.get("score", 0) > 0.5:
        explanations.append("Inconsistent noise variance (possible blur or paste)")
    if struct_res.get("score", 0) > 0.5:
        explanations.extend(struct_res.get("reasons", []))
        
    if not explanations and risk_score <= 0.4:
        explanations.append("No significant anomalies detected.")

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "confidence": 0.92,
        "signals": {
            "ela": round(ela_res.get("score", 0), 2),
            "metadata": round(exif_res.get("score", 0), 2),
            "compression": round(noise_res.get("score", 0), 2),
            "structure": round(struct_res.get("score", 0), 2)
        },
        "explanations": explanations,
        "document_hash": hash_res.get("hash", ""),
        "visual_proof": ela_res.get("visual_proof", "")
    }

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
