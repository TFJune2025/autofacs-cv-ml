"""Constrained video inference example for AutoFACS CV/ML.

This example is inspired by the project's producer/gatekeeper workflow but is
intentionally simplified for public release. It samples frames from a short
video clip, detects faces, applies staged inference, and writes a CSV summary.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, List, Tuple

import cv2
import face_recognition
from PIL import Image

from infer_image import infer_image


def sample_video_frames(video_path: str | Path, every_n_frames: int = 10) -> Iterable[Tuple[int, float, object]]:
    capture = cv2.VideoCapture(str(video_path))
    fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
    frame_idx = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if frame_idx % every_n_frames == 0:
                timestamp = frame_idx / fps
                yield frame_idx, timestamp, frame
            frame_idx += 1
    finally:
        capture.release()


def extract_face_crops(frame_bgr) -> List[Image.Image]:
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    crops: List[Image.Image] = []
    height, width = rgb.shape[:2]
    for top, right, bottom, left in locations:
        face_h = bottom - top
        face_w = right - left
        v_pad = int(face_h * 0.40)
        h_pad = int(face_w * 0.15)
        top = max(0, top - v_pad)
        bottom = min(height, bottom + int(v_pad * 0.1))
        left = max(0, left - h_pad)
        right = min(width, right + h_pad)
        crop = Image.fromarray(rgb[top:bottom, left:right])
        crops.append(crop)
    return crops


def run_video(
    video_path: str | Path,
    output_csv: str | Path,
    stage1_model_dir: str | Path,
    stage2_model_dir: str | Path,
    *,
    stage2_calibration_json: str | Path | None = None,
    review_threshold: float = 0.85,
    every_n_frames: int = 10,
) -> None:
    rows = []
    for frame_idx, timestamp, frame in sample_video_frames(video_path, every_n_frames=every_n_frames):
        for face_idx, crop in enumerate(extract_face_crops(frame), start=1):
            temp_path = Path(output_csv).with_suffix(f".frame_{frame_idx}_{face_idx}.png")
            crop.save(temp_path)
            result = infer_image(
                image_path=temp_path,
                stage1_model_dir=stage1_model_dir,
                stage2_model_dir=stage2_model_dir,
                stage2_calibration_json=stage2_calibration_json,
                review_threshold=review_threshold,
            )
            temp_path.unlink(missing_ok=True)

            row = {
                "frame_number": frame_idx,
                "timestamp_seconds": round(timestamp, 3),
                "face_index": face_idx,
                "pipeline_status": result["status"],
                "stage1_label": result["stage1"].label,
                "stage1_confidence": round(result["stage1"].confidence, 6),
                "stage2_label": "",
                "stage2_confidence": "",
                "needs_review": "",
            }
            if result["stage2"] is not None:
                row["stage2_label"] = result["stage2"].label
                row["stage2_confidence"] = round(result["stage2"].confidence, 6)
                row["needs_review"] = result["stage2"].needs_review
            rows.append(row)

    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else [
            "frame_number", "timestamp_seconds", "face_index", "pipeline_status",
            "stage1_label", "stage1_confidence", "stage2_label", "stage2_confidence", "needs_review",
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} records to {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run simplified AutoFACS CV/ML video inference.")
    parser.add_argument("video_path")
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--stage1-model", required=True)
    parser.add_argument("--stage2-model", required=True)
    parser.add_argument("--stage2-calibration")
    parser.add_argument("--review-threshold", type=float, default=0.85)
    parser.add_argument("--every-n-frames", type=int, default=10)
    args = parser.parse_args()

    run_video(
        video_path=args.video_path,
        output_csv=args.output_csv,
        stage1_model_dir=args.stage1_model,
        stage2_model_dir=args.stage2_model,
        stage2_calibration_json=args.stage2_calibration,
        review_threshold=args.review_threshold,
        every_n_frames=args.every_n_frames,
    )
