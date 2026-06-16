@'
"""
Module: api.py
Description: FastAPI backend to serve the Security Vision Engine.
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from vision_security import SecurityVisionEngine
import shutil
import os

app = FastAPI(title="Tactical Vision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Booting Vision Engine...")
engine = SecurityVisionEngine(threshold=0.60)
os.makedirs("temp", exist_ok=True)


@app.get("/")
def root():
    return {"status": "online", "service": "Tactical Vision API"}


@app.get("/health")
def health():
    return {"status": "healthy", "device": str(engine.device)}


@app.post("/scan")
async def scan_image(file: UploadFile = File(...)):
    temp_path = f"temp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    report = engine.run_security_scan(temp_path)
    os.remove(temp_path)
    return {"status": "success", "report": report}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'@ | Out-File -Encoding utf8 api.py