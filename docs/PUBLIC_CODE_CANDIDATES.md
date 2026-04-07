# Public Code Included in This Repository

This repository now includes a **small exemplary code layer**. The examples are intentionally compact and disclosure-conscious: they are meant to help readers understand the architecture, not to publish the full private system.

## Included files

1. **`examples/infer_image.py`**  
   A two-stage inference example that demonstrates:
   - Stage 1 relevance filtering
   - Stage 2 expression/state prediction
   - optional scalar-temperature calibration
   - confidence-based review routing

2. **`examples/stage1_filter_example.py`**  
   A smaller Stage 1-only example that isolates the relevance gate.

3. **`examples/infer_video_clip.py`**  
   A constrained video example that samples frames from a short clip, extracts face crops, applies staged inference, and writes a frame-level CSV summary.

4. **`examples/hf_space_app.py`**  
   A prototype Hugging Face Spaces app showing the most natural public demo path:
   - image input first
   - short-video analysis second

5. **`examples/plot_v40_results.py`**  
   A plotting script that rebuilds approved V40 visuals from aggregate metrics CSVs.

6. **`examples/source_ingestion_example.py`**  
   A public-facing ingestion example adapted from the project’s API-based open-source image sourcing workflow.

7. **`examples/curation_patch_builder_example.py`**  
   A compact curation example showing low-confidence shortlist creation, corridor prioritization, and patch validation.

## Why this is enough for a public repo

These files make the project more legible for engineers and technical reviewers without exposing:
- private datasets
- raw logits/labels arrays
- private checkpoint packaging
- full internal orchestration
- absolute local paths and storage topology

## Relationship to the private project

The private project remains broader and deeper than these examples. The public examples are meant to map to the repo's documented architecture and workflow surfaces while staying appropriate for a public-facing repository.
