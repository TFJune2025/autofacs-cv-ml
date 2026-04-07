"""Prototype Hugging Face Spaces app for AutoFACS CV/ML.

Phase 1: image inference
Phase 2: short constrained video clip inference

This file is intentionally lightweight and is meant to be adapted after the
provisional filing and model-packaging decisions are complete.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import gradio as gr
import pandas as pd

from infer_image import infer_image, format_result
from infer_video_clip import run_video

STAGE1_MODEL_DIR = os.getenv("AUTOFACS_STAGE1_MODEL", "./models/stage1")
STAGE2_MODEL_DIR = os.getenv("AUTOFACS_STAGE2_MODEL", "./models/stage2")
STAGE2_CALIBRATION = os.getenv("AUTOFACS_STAGE2_CALIBRATION", "") or None


def predict_image(image_path: str):
    if not image_path:
        return "No image provided."
    payload = infer_image(
        image_path=image_path,
        stage1_model_dir=STAGE1_MODEL_DIR,
        stage2_model_dir=STAGE2_MODEL_DIR,
        stage2_calibration_json=STAGE2_CALIBRATION,
    )
    return format_result(payload)


def predict_video(video_path: str):
    if not video_path:
        return pd.DataFrame(columns=[
            "frame_number", "timestamp_seconds", "face_index", "pipeline_status",
            "stage1_label", "stage1_confidence", "stage2_label", "stage2_confidence", "needs_review",
        ])

    with tempfile.TemporaryDirectory() as tmpdir:
        out_csv = Path(tmpdir) / "video_summary.csv"
        run_video(
            video_path=video_path,
            output_csv=out_csv,
            stage1_model_dir=STAGE1_MODEL_DIR,
            stage2_model_dir=STAGE2_MODEL_DIR,
            stage2_calibration_json=STAGE2_CALIBRATION,
            every_n_frames=12,
        )
        return pd.read_csv(out_csv)


with gr.Blocks(title="AutoFACS CV/ML Demo") as demo:
    gr.Markdown("# AutoFACS CV/ML Demo")
    gr.Markdown(
        "Image inference is the primary demo surface. Short-video analysis can be added as a constrained second phase."
    )

    with gr.Tab("Image"):
        image_input = gr.Image(type="filepath", label="Upload an image")
        image_output = gr.Textbox(label="Inference summary", lines=16)
        image_button = gr.Button("Run image inference")
        image_button.click(fn=predict_image, inputs=image_input, outputs=image_output)

    with gr.Tab("Short video"):
        video_input = gr.Video(label="Upload a short clip")
        video_output = gr.Dataframe(label="Frame-level summary")
        video_button = gr.Button("Run short-video inference")
        video_button.click(fn=predict_video, inputs=video_input, outputs=video_output)


if __name__ == "__main__":
    demo.launch()
