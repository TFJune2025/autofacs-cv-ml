"""Minimal Stage 1 relevance filter example.

This file exists to explain the Stage 1 concept in the public repository:
AutoFACS first decides whether a face crop should proceed to the finer-grained
expression/state classifier.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from infer_image import ImageClassifier, pick_device


def run_stage1(image_path: str | Path, model_dir: str | Path, *, prefer_mps: bool = True) -> None:
    device = pick_device(prefer_mps=prefer_mps)
    classifier = ImageClassifier(model_dir, device)
    image = Image.open(image_path).convert("RGB")
    result = classifier.predict(image)

    print(f"Device: {device}")
    print("Stage 1 relevance result")
    print(f"  label: {result.label}")
    print(f"  confidence: {result.confidence:.4f}")
    print(f"  entropy: {result.entropy:.4f}")
    print("  probabilities:")
    for label, prob in sorted(result.probabilities.items(), key=lambda kv: kv[1], reverse=True):
        print(f"    - {label}: {prob:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Stage 1 relevance-only inference.")
    parser.add_argument("image_path")
    parser.add_argument("--model", required=True, help="Path to the Stage 1 relevance model directory.")
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()
    run_stage1(args.image_path, args.model, prefer_mps=not args.cpu)
