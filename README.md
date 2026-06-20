# AI Security — Faster R-CNN vs RetinaNet Detection
### Dual-Model Real-Time Object Detection for Security Surveillance

A production-architecture security monitoring system that runs **two
state-of-the-art object detection models simultaneously** to compare
accuracy and inference speed — built for real-time human and vehicle
tracking in high-traffic security zones.

## Why Two Models?
Faster R-CNN (Two-stage detector)

→ Region proposal network first

→ Then classifies each region

→ Higher accuracy, slower
RetinaNet (One-stage detector)

→ Single pass detection

→ Focal loss handles class imbalance

→ Faster, near-equal accuracy
Running both = best of both worlds!

Compare in real-time, choose per use case!

## Features

- 🎯 Dual-model inference (Faster R-CNN + RetinaNet)
- 🚨 Security-relevant class filtering (person, vehicles, bags, laptops)
- ⚡ GPU auto-detection with CPU fallback
- 📊 Real-time inference latency comparison
- 🖥️ Tactical-themed canvas UI with bounding box visualization
- 🔌 REST API (FastAPI) for easy integration

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **ML Framework:** PyTorch + torchvision
- **Models:** Faster R-CNN ResNet-50 FPN, RetinaNet ResNet-50 FPN
- **Pre-trained on:** COCO dataset (90 classes, filtered to 10 security-relevant)
- **Frontend:** Vanilla JavaScript + HTML5 Canvas
- **Image processing:** Pillow

## Architecture
Browser uploads image

↓

POST /scan (multipart/form-data)

↓

SecurityVisionEngine.analyze()

↓

┌────────────┬────────────┐

↓                         ↓

Faster R-CNN              RetinaNet

(torch.no_grad())      (torch.no_grad())

↓                         ↓

Filter by SECURITY_TARGETS + confidence ≥ 0.60

↓                         ↓

└────────────┬────────────┘

↓

JSON response: detections + inference_time_ms

↓

Frontend draws bounding boxes on canvas

## Security Target Classes
person, backpack, suitcase, laptop,

cell phone, car, truck, bus,

motorcycle, bicycle

Filtered from the full 90-class COCO dataset to focus on
security-relevant objects only.

## Setup

### 1. Clone
```bash
git clone https://github.com/NIKHIL-956653/AI-Security-Faster-R-CNN-RetinaNet-Detection.git
cd AI-Security-Faster-R-CNN-RetinaNet-Detection
```

### 2. Virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

For GPU support (CUDA 11.8):
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Run

### Test the vision engine standalone
```bash
python vision_security.py
```
Creates a dummy test image and prints detection results from both
models to console — verifies models load correctly.

### Start the API server
```bash
python api.py
```
Server starts at `http://0.0.0.0:8000`. First run downloads ~500MB
of pre-trained COCO weights from torchvision hub.

### Open the frontend
```bash
cd frontend
start index.html
```
Upload any image with people/vehicles to see dual-model detection
in action!

## API Reference

### `POST /scan`
Upload an image, receive detection results from both models.

**Response:**
```json
{
  "status": "success",
  "report": {
    "faster_rcnn": {
      "model": "Faster R-CNN",
      "inference_time_ms": 125.45,
      "detections": [
        {"class": "person", "confidence": 98.2, "box": [x1, y1, x2, y2]}
      ]
    },
    "retinanet": {
      "model": "RetinaNet",
      "inference_time_ms": 89.32,
      "detections": [...]
    }
  }
}
```

### `GET /health`
Returns service status and device info (CPU/GPU).

## Performance

| Model | Type | CPU Inference | GPU Inference |
|-------|------|---------------|----------------|
| Faster R-CNN ResNet-50 FPN | Two-stage | ~1000-2000ms | ~80-200ms |
| RetinaNet ResNet-50 FPN | One-stage (Focal Loss) | ~800-1500ms | ~80-150ms |

*Tested on standard images with multiple detected objects.*

## Design Decisions

- **Confidence threshold:** 0.60 default — configurable via
  `SecurityVisionEngine(threshold=X)`
- **Parallel model execution:** Both models run independently per
  image, enabling ensemble-like decision-making for security contexts
- **CORS open for development:** `allow_origins=["*"]` — should be
  restricted to specific domains in production
- **No build step on frontend:** Vanilla JS keeps the demo lightweight
  and dependency-free

## Known Limitations (Roadmap)

- [ ] No persistent detection history/logging
- [ ] No live webcam stream support (currently single-image upload)
- [ ] No authentication/rate limiting on API
- [ ] Frontend currently visualizes Faster R-CNN boxes only

## Interview Answer

"I built a dual-model security detection system comparing Faster
R-CNN and RetinaNet — a two-stage vs one-stage detector — running
both in parallel via PyTorch under `torch.no_grad()` for inference
efficiency. The system filters COCO's 90 classes down to 10
security-relevant targets like person, vehicle, and bag detection,
with a configurable confidence threshold. This achieved high
detection accuracy for human and vehicle tracking in high-traffic
zones, with GPU acceleration providing 5-10x speedup over CPU
inference for real-time deployment scenarios."

## Author

**Nikhil Chandra Sairam Tokala**
AI/ML Engineer | GenAI Engineer | DevOps
Dubai, UAE
[LinkedIn](https://linkedin.com/in/nikhil-chandra-133ncsr200233) |
[GitHub](https://github.com/NIKHIL-956653)