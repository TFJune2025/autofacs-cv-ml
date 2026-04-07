"""Public-facing two-stage image inference example for AutoFACS CV/ML.

This example is intentionally compact. It demonstrates the staged inference
pattern described in the repository without exposing private training code,
private storage topology, or full internal orchestration.

Stage 1:
    Binary relevance filtering (relevant vs irrelevant)
Stage 2:
    Expression/state classification over the public-facing V40 label space
Optional:
    Scalar temperature calibration and confidence-based review routing
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

STAGE2_LABELS: List[str] = [
    "anger",
    "contempt",
    "disgust",
    "fear",
    "happiness",
    "neutral",
    "questioning",
    "sadness",
    "surprise",
    "neutral_speech",
    "speech_action",
]


def pick_device(prefer_mps: bool = True) -> torch.device:
    if prefer_mps and torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


@dataclass
class PredictionResult:
    label: str
    confidence: float
    entropy: float
    probabilities: Dict[str, float]
    needs_review: bool


class ImageClassifier:
    def __init__(self, model_dir: str | Path, device: torch.device):
        self.model_dir = str(model_dir)
        self.device = device
        self.processor = AutoImageProcessor.from_pretrained(self.model_dir)
        self.model = AutoModelForImageClassification.from_pretrained(self.model_dir)
        self.model.to(self.device).eval()

    def predict(self, image: Image.Image, *, temperature: Optional[float] = None) -> PredictionResult:
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = self.model(**inputs).logits.squeeze(0)

        if temperature is not None and temperature > 0:
            logits = logits / temperature

        probabilities = torch.softmax(logits, dim=0)
        confidence, top_index = torch.max(probabilities, dim=0)
        entropy = -torch.sum(probabilities * torch.log(probabilities + 1e-9)).item()

        id2label = self.model.config.id2label
        probs = {id2label[i]: float(probabilities[i].item()) for i in range(probabilities.numel())}
        label = id2label[int(top_index.item())]
        return PredictionResult(
            label=label,
            confidence=float(confidence.item()),
            entropy=float(entropy),
            probabilities=probs,
            needs_review=False,
        )


def load_temperature(calibration_json: Optional[str | Path]) -> Optional[float]:
    if not calibration_json:
        return None
    path = Path(calibration_json)
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    value = payload.get("T")
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def open_rgb_image(path: str | Path) -> Image.Image:
    image = Image.open(path)
    return image.convert("RGB")


def infer_image(
    image_path: str | Path,
    stage1_model_dir: str | Path,
    stage2_model_dir: str | Path,
    *,
    stage2_calibration_json: Optional[str | Path] = None,
    review_threshold: float = 0.85,
    prefer_mps: bool = True,
) -> Dict[str, object]:
    device = pick_device(prefer_mps=prefer_mps)
    image = open_rgb_image(image_path)

    stage1 = ImageClassifier(stage1_model_dir, device)
    stage2 = ImageClassifier(stage2_model_dir, device)

    stage1_result = stage1.predict(image)
    if stage1_result.label != "relevant":
        stage1_result.needs_review = False
        return {
            "device": str(device),
            "stage1": stage1_result,
            "stage2": None,
            "status": "filtered_as_irrelevant",
        }

    temperature = load_temperature(stage2_calibration_json)
    stage2_result = stage2.predict(image, temperature=temperature)
    stage2_result.needs_review = stage2_result.confidence < review_threshold
    status = "review" if stage2_result.needs_review else "accepted"

    return {
        "device": str(device),
        "stage1": stage1_result,
        "stage2": stage2_result,
        "status": status,
        "review_threshold": review_threshold,
        "temperature": temperature,
    }


def format_result(payload: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append(f"Device: {payload['device']}")
    lines.append(f"Pipeline status: {payload['status']}")

    stage1: PredictionResult = payload["stage1"]
    lines.append("")
    lines.append("Stage 1")
    lines.append(f"  label: {stage1.label}")
    lines.append(f"  confidence: {stage1.confidence:.4f}")

    stage2 = payload.get("stage2")
    if stage2 is not None:
        lines.append("")
        lines.append("Stage 2")
        lines.append(f"  label: {stage2.label}")
        lines.append(f"  confidence: {stage2.confidence:.4f}")
        lines.append(f"  entropy: {stage2.entropy:.4f}")
        lines.append(f"  needs_review: {stage2.needs_review}")
        top_items = sorted(stage2.probabilities.items(), key=lambda kv: kv[1], reverse=True)[:5]
        lines.append("  top probabilities:")
        for label, prob in top_items:
            lines.append(f"    - {label}: {prob:.4f}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run public-facing AutoFACS CV/ML image inference.")
    parser.add_argument("image_path")
    parser.add_argument("--stage1-model", required=True, help="Path to the Stage 1 relevance model directory.")
    parser.add_argument("--stage2-model", required=True, help="Path to the Stage 2 classifier model directory.")
    parser.add_argument("--stage2-calibration", help="Optional stage2_calibration.json path.")
    parser.add_argument("--review-threshold", type=float, default=0.85)
    parser.add_argument("--cpu", action="store_true", help="Force CPU execution.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = infer_image(
        image_path=args.image_path,
        stage1_model_dir=args.stage1_model,
        stage2_model_dir=args.stage2_model,
        stage2_calibration_json=args.stage2_calibration,
        review_threshold=args.review_threshold,
        prefer_mps=not args.cpu,
    )
    print(format_result(payload))


if __name__ == "__main__":
    main()
