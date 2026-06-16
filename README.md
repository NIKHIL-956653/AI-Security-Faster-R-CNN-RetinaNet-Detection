@'
# AI Security Management

Real-time object detection system comparing **Faster R-CNN** (two-stage) and **RetinaNet** (one-stage with focal loss) for security applications. Detects humans, vehicles, and security-relevant objects in real-time.

## Stack

- **Backend:** FastAPI, PyTorch, torchvision
- **Models:** Faster R-CNN ResNet-50 FPN, RetinaNet ResNet-50 FPN
- **Frontend:** Vanilla JS with tactical-themed UI
- **Hardware:** CUDA GPU support, CPU fallback

## Run

```bash
# Install
pip install -r requirements.txt

# Start backend
python api.py

# Open frontend/index.html in a browser
```

## API

`POST /scan` — Upload image, get dual-model detection report
`GET /health` — Service health check

## Detection Targets

person, backpack, suitcase, laptop, cell phone, car, truck, bus, motorcycle, bicycle
'@ | Out-File -Encoding utf8 README.md