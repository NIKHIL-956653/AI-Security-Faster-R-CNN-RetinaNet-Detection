# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI Security Management** — a dual-model object detection system that runs Faster R-CNN and RetinaNet simultaneously on uploaded images to compare accuracy and inference speed for security surveillance applications. Detects a filtered subset of COCO classes relevant to security (people, vehicles, bags, etc.).

## Commands

### Install dependencies

```bash
pip install fastapi uvicorn torch torchvision pillow
```

For NVIDIA GPU (CUDA 11.8):

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Run the backend

```bash
python api.py
```

Starts FastAPI on `http://0.0.0.0:8000`. First run downloads ~500 MB of pre-trained weights from torchvision hub.

### Test the vision engine in isolation

```bash
python vision_security.py
```

Generates a dummy `security_test.jpg` and prints detection results from both models to console.

### Frontend

Open `frontend/index.html` directly in a browser — no build step needed.

## Architecture

### Key files

- [api.py](api.py) — FastAPI entry point. Exposes `POST /scan` (upload image → dual-model report) and `GET /health`. Saves uploaded images to `temp/` before processing.
- [vision_security.py](vision_security.py) — `SecurityVisionEngine` class. Loads both models, runs inference, filters detections by `SECURITY_TARGETS` set and confidence threshold (default 0.60).
- [frontend/index.html](frontend/index.html) — Single-page tactical UI. Sends image as multipart form to `/scan`, draws bounding boxes on a `<canvas>`, and displays per-model inference latency.
- [frontend/api.py](frontend/api.py) and [frontend/vision_security.py](frontend/vision_security.py) — Near-duplicate variants with minor differences (extended `SECURITY_TARGETS`, added root endpoint). The root-level files are canonical.

### Data flow

1. Browser uploads image → `POST /scan` (multipart)
2. `api.py` writes file to `temp/`, calls `SecurityVisionEngine.analyze()`
3. Engine runs both models under `torch.no_grad()`, filters by security class + confidence
4. JSON response includes per-model `detections` (class, confidence, box) and `inference_time_ms`
5. Frontend draws Faster R-CNN boxes on canvas and populates telemetry log for both models

### Model details

| Model | Type | Characteristic |
|---|---|---|
| Faster R-CNN ResNet-50 FPN | Two-stage | Higher accuracy, slower (80–200 ms GPU) |
| RetinaNet ResNet-50 FPN | One-stage | Focal loss for class imbalance, faster |

Both load from `torchvision.models.detection` with COCO pre-trained weights. Device is auto-detected (`cuda` if available, else `cpu`). GPU inference is 5–10× faster; CPU runs 800–2000 ms per model.

### Security target filtering

Defined as `SECURITY_TARGETS` in [vision_security.py](vision_security.py) (line ~31). Must match names from the COCO class list in the same file. Confidence threshold is set at `SecurityVisionEngine(threshold=0.60)`.

### CORS

`allow_origins=["*"]` is configured in both `api.py` files — intentional for local development.
