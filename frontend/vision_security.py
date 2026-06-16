@'
"""
Module: vision_security.py
Description: AI Security Object Detection pipeline.
             Compares Faster R-CNN (Two-Stage) and RetinaNet (One-Stage/Focal Loss)
             for real-time threat/anomaly detection in visual feeds.
"""

import torch
import torchvision
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights, RetinaNet_ResNet50_FPN_Weights
from torchvision.transforms import functional as F
from PIL import Image, ImageDraw
import time

COCO_CLASSES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

SECURITY_TARGETS = {'person', 'backpack', 'suitcase', 'laptop', 'cell phone', 'car', 'truck', 'bus', 'motorcycle', 'bicycle'}


class SecurityVisionEngine:
    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Initializing Security Vision Engine on: {self.device}")

        print("Loading Faster R-CNN weights...")
        self.faster_rcnn = torchvision.models.detection.fasterrcnn_resnet50_fpn(
            weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        ).to(self.device)
        self.faster_rcnn.eval()

        print("Loading RetinaNet weights...")
        self.retinanet = torchvision.models.detection.retinanet_resnet50_fpn(
            weights=RetinaNet_ResNet50_FPN_Weights.DEFAULT
        ).to(self.device)
        self.retinanet.eval()

    def process_image(self, image_path: str):
        try:
            img = Image.open(image_path).convert("RGB")
            img_tensor = F.to_tensor(img).unsqueeze(0).to(self.device)
            return img, img_tensor
        except Exception as e:
            raise RuntimeError(f"Failed to load image at {image_path}: {e}")

    def _parse_predictions(self, predictions, run_time: float, model_name: str):
        boxes = predictions[0]['boxes'].cpu().detach().numpy()
        labels = predictions[0]['labels'].cpu().detach().numpy()
        scores = predictions[0]['scores'].cpu().detach().numpy()

        results = []
        for i in range(len(scores)):
            if scores[i] >= self.threshold:
                class_name = COCO_CLASSES[labels[i]]
                if class_name in SECURITY_TARGETS:
                    results.append({
                        "class": class_name,
                        "confidence": round(float(scores[i]) * 100, 2),
                        "box": [round(coord, 1) for coord in boxes[i]]
                    })

        return {
            "model": model_name,
            "inference_time_ms": round(run_time * 1000, 2),
            "detections": results
        }

    def run_security_scan(self, image_path: str):
        print(f"\n--- Running Security Scan on {image_path} ---")
        _, img_tensor = self.process_image(image_path)

        start_time = time.time()
        with torch.no_grad():
            faster_preds = self.faster_rcnn(img_tensor)
        faster_time = time.time() - start_time
        faster_results = self._parse_predictions(faster_preds, faster_time, "Faster R-CNN")

        start_time = time.time()
        with torch.no_grad():
            retina_preds = self.retinanet(img_tensor)
        retina_time = time.time() - start_time
        retina_results = self._parse_predictions(retina_preds, retina_time, "RetinaNet")

        return {"faster_rcnn": faster_results, "retinanet": retina_results}


if __name__ == "__main__":
    import os
    test_image_path = "security_test.jpg"
    if not os.path.exists(test_image_path):
        print(f"Creating dummy image '{test_image_path}'...")
        img = Image.new('RGB', (800, 600), color=(73, 109, 137))
        img.save(test_image_path)

    engine = SecurityVisionEngine(threshold=0.60)
    report = engine.run_security_scan(test_image_path)
    print("\n[FASTER R-CNN]:", report['faster_rcnn'])
    print("\n[RETINANET]:", report['retinanet'])
'@ | Out-File -Encoding utf8 vision_security.py