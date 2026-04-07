# Examples

This folder now contains **public-facing exemplary code** derived from the project materials you shared in this thread. The goal is to make the repository more concrete for technically literate readers without publishing the full private training stack, private storage topology, or private model package.

## Included examples

- `infer_image.py` — two-stage image inference: Stage 1 relevance filtering, Stage 2 expression/state prediction, optional calibration, and review routing.
- `stage1_filter_example.py` — a smaller relevance-only example for readers who want the Stage 1 concept in isolation.
- `infer_video_clip.py` — a constrained frame-sampling and video-inference example inspired by the producer/gatekeeper workflow.
- `hf_space_app.py` — a Hugging Face Spaces prototype that supports image input first and short-video analysis as a second phase.
- `plot_v40_results.py` — rebuilds approved V40 summary visuals from aggregate metrics CSVs rather than raw private arrays.
- `source_ingestion_example.py` — a public-facing API-based sourcing example adapted from the project's open-source image ingestion work.
- `curation_patch_builder_example.py` — a compact patch-builder example showing shortlist generation, corridor prioritization, and validation.
- `model_config.example.json` and `preprocessor_config.example.json` — public-facing configuration examples aligned with the modeling overview in `docs/MODEL_AND_TRAINING.md`.

## Configuration context

The example configuration files in this folder are included for readers, not as private notes to the project owner. Together, `examples/model_config.example.json` and `examples/preprocessor_config.example.json` illustrate the kind of public-facing model and preprocessing contract discussed in `docs/MODEL_AND_TRAINING.md`: a ViT-family image-classification surface, 224×224 image inputs, and a corresponding resize/rescale/normalize flow that is consistent with the inference examples in `examples/infer_image.py` and `examples/stage1_filter_example.py`.

## What these examples demonstrate

Together, these examples show that the public repository is backed by real engineering surfaces:

- staged inference rather than a single flat classifier
- calibration-aware prediction handling
- review routing for uncertain cases
- video/frame analysis as a natural extension of image inference
- API-based source ingestion
- curation and patch-building workflows

## What they do not try to be

These files are **not** a full reproducibility package. They intentionally avoid:

- private data-lake paths
- raw evaluation arrays
- internal checkpoint organization
- secrets and API keys
- full private orchestration logic
