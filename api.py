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

# Allow the frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the engine once when the server starts
print("Booting Vision Engine...")
engine = SecurityVisionEngine(threshold=0.60)
os.makedirs("temp", exist_ok=True)

@app.post("/scan")
async def scan_image(file: UploadFile = File(...)):
    """Receives an image, saves it temporarily, and runs the dual-model scan."""
    temp_path = f"temp/{file.filename}"
    
    # Save the incoming image
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Run the security scan using your existing module
    report = engine.run_security_scan(temp_path)
    
    # Clean up
    os.remove(temp_path)
    
    return {"status": "success", "report": report}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)